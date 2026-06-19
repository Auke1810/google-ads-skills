#!/usr/bin/env python3
"""
analyze_account.py — deterministic analysis layer for a Google Ads account audit.

Design: fetching account data (credentials, OAuth, developer token, or a future
MCP) is brittle and environment-specific. Analysis doesn't have to be. This
script consumes the JSON results of a fixed set of GAQL queries (see
references/gaql-queries.md) and computes the high-volume, objective findings a
human shouldn't be eyeballing across hundreds of keywords and thousands of
search terms — above all the real wasted-spend figure the audit report needs.

It does NOT fetch anything. Run the GAQL queries however you obtain account
access, drop the rows into one JSON file, and point this script at it.

Input JSON (any dataset may be omitted — checks that need it are skipped):
    {
      "account": "Example NV",
      "currency": "EUR",
      "date_range": "LAST_30_DAYS",
      "campaigns":           [ <gaql rows> ],
      "keywords":            [ <gaql rows> ],
      "search_terms":        [ <gaql rows> ],
      "ads":                 [ <gaql rows> ],
      "conversion_actions":  [ <gaql rows> ]
    }

Rows are the raw GAQL result objects (REST camelCase, nested). Money is in
micros and converted automatically (1,000,000 micros = 1 unit of currency).

Usage:
    python3 analyze_account.py <account.json> [--out DIR] [--min-spend N] [--top N]

Outputs <name>.audit.json (full findings) + a stdout summary. Stdlib only.
"""

import argparse
import json
import os
import sys
from collections import Counter, defaultdict


def g(obj, path, default=None):
    """Nested getter: g(row, 'metrics.costMicros')."""
    cur = obj
    for part in path.split("."):
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            return default
    return cur


def micros(v):
    try:
        return int(v) / 1_000_000
    except (TypeError, ValueError):
        return 0.0


def num(v, default=0.0):
    try:
        return float(v)
    except (TypeError, ValueError):
        return default


def money(x, cur):
    return f"{cur} {x:,.0f}" if x >= 100 else f"{cur} {x:,.2f}"


# ---------------------------------------------------------------------------
# Checks. Each appends dicts to `findings` and may contribute to `summary`.
# ---------------------------------------------------------------------------
def analyze(data, min_spend):
    cur = data.get("currency", "")
    findings = []
    ran = []  # which checks actually had data to run

    campaigns = data.get("campaigns") or []
    keywords = data.get("keywords") or []
    search_terms = data.get("search_terms") or []
    ads = data.get("ads") or []
    conv_actions = data.get("conversion_actions") or []

    def add(sev, code, msg, detail=None):
        findings.append({"severity": sev, "code": code, "message": msg,
                         "detail": detail or {}})

    total_spend = sum(micros(g(c, "metrics.costMicros")) for c in campaigns)
    if not total_spend:
        total_spend = sum(micros(g(k, "metrics.costMicros")) for k in keywords)
    total_conv = sum(num(g(c, "metrics.conversions")) for c in campaigns)

    # --- Conversion tracking (audit this FIRST: it poisons everything else) ---
    if conv_actions:
        ran.append("conversion_tracking")
        enabled = [a for a in conv_actions
                   if g(a, "conversionAction.status") == "ENABLED"]
        if not enabled:
            add("critical", "no_active_conversions",
                "No ENABLED conversion actions — the account is optimizing blind")
        primaries = [a for a in enabled if g(a, "conversionAction.primaryForGoal")]
        if enabled and not primaries:
            add("high", "no_primary_conversion",
                "Conversion actions exist but none are primary for a goal")
        no_value = [g(a, "conversionAction.name") for a in enabled
                    if not num(g(a, "conversionAction.valueSettings.defaultValue"))]
        if no_value and len(no_value) == len(enabled):
            add("high", "conversions_no_value",
                "No conversion value is set — value-based bidding (tROAS) can't work",
                {"actions": no_value[:10]})
    elif total_spend:
        # Spending with no conversion-action data at all is a red flag.
        add("critical", "no_conversion_data",
            "Account has spend but no conversion-tracking data was provided/found")

    # --- Wasted spend: search terms are the most granular signal ---
    waste_amount = 0.0
    neg_candidates = []
    if search_terms:
        ran.append("search_term_waste")
        for st in search_terms:
            cost = micros(g(st, "metrics.costMicros"))
            conv = num(g(st, "metrics.conversions"))
            term = g(st, "searchTermView.searchTerm") or g(st, "searchTerm") or "(unknown)"
            if conv == 0 and cost >= min_spend:
                waste_amount += cost
                neg_candidates.append({"term": term, "cost": round(cost, 2),
                                       "clicks": int(num(g(st, "metrics.clicks")))})
        neg_candidates.sort(key=lambda x: -x["cost"])
        if waste_amount:
            pct = (waste_amount / total_spend * 100) if total_spend else 0
            add("critical", "search_term_waste",
                f"{money(waste_amount, cur)} spent on {len(neg_candidates)} "
                f"converting-zero search terms ({pct:.0f}% of spend) — negative-keyword opportunity",
                {"top_terms": neg_candidates[:25]})

    # --- Zero-conversion keywords (pause/rework candidates) ---
    kw_waste = 0.0
    if keywords:
        ran.append("keyword_waste")
        zero = []
        for k in keywords:
            cost = micros(g(k, "metrics.costMicros"))
            conv = num(g(k, "metrics.conversions"))
            if conv == 0 and cost >= min_spend:
                kw_waste += cost
                zero.append({
                    "keyword": g(k, "adGroupCriterion.keyword.text"),
                    "match": g(k, "adGroupCriterion.keyword.matchType"),
                    "ad_group": g(k, "adGroup.name"),
                    "cost": round(cost, 2),
                })
        zero.sort(key=lambda x: -x["cost"])
        if kw_waste:
            add("high", "zero_conversion_keywords",
                f"{money(kw_waste, cur)} on {len(zero)} keywords with zero conversions",
                {"top": zero[:25]})

        # --- Low Quality Score keywords with spend ---
        ran.append("quality_score")
        low_qs = []
        for k in keywords:
            qs = g(k, "adGroupCriterion.qualityInfo.qualityScore")
            cost = micros(g(k, "metrics.costMicros"))
            if qs is not None and qs <= 4 and cost >= min_spend:
                low_qs.append({"keyword": g(k, "adGroupCriterion.keyword.text"),
                               "qs": qs, "cost": round(cost, 2)})
        low_qs.sort(key=lambda x: -x["cost"])
        if low_qs:
            add("high", "low_quality_score",
                f"{len(low_qs)} keywords with Quality Score ≤4 are taking spend — "
                f"you pay a click premium and lose impression share",
                {"top": low_qs[:25]})

        # --- Duplicate keywords across ad groups (self-competition) ---
        ran.append("duplicate_keywords")
        seen = defaultdict(set)
        for k in keywords:
            text = (g(k, "adGroupCriterion.keyword.text") or "").lower()
            mt = g(k, "adGroupCriterion.keyword.matchType")
            ag = g(k, "adGroup.name")
            if text:
                seen[(text, mt)].add(ag)
        dupes = [{"keyword": t, "match": mt, "ad_groups": sorted(ags)}
                 for (t, mt), ags in seen.items() if len(ags) > 1]
        if dupes:
            add("medium", "duplicate_keywords",
                f"{len(dupes)} keyword/match-type combos appear in multiple ad groups "
                f"(they compete in the same auction and split data)",
                {"examples": dupes[:15]})

    # --- Campaign settings + budget/bidding ---
    if campaigns:
        ran.append("campaign_settings")
        budget_limited, content_on, thin_smart = [], [], []
        for c in campaigns:
            name = g(c, "campaign.name")
            channel = g(c, "campaign.advertisingChannelType")
            cost = micros(g(c, "metrics.costMicros"))
            conv = num(g(c, "metrics.conversions"))

            lost_budget = num(g(c, "metrics.searchBudgetLostImpressionShare"))
            if lost_budget >= 0.10 and conv > 0:
                budget_limited.append({"campaign": name,
                                       "lost_is_budget": round(lost_budget, 2),
                                       "conversions": conv})

            if channel == "SEARCH" and g(c, "campaign.networkSettings.targetContentNetwork"):
                content_on.append(name)

            bid = g(c, "campaign.biddingStrategyType") or ""
            if bid in ("MAXIMIZE_CONVERSIONS", "TARGET_CPA",
                       "MAXIMIZE_CONVERSION_VALUE", "TARGET_ROAS") and conv < 30 and cost >= min_spend:
                thin_smart.append({"campaign": name, "strategy": bid,
                                   "conversions": conv})

            if cost >= max(min_spend * 5, 50) and conv == 0:
                add("critical", "campaign_spend_no_conv",
                    f"Campaign '{name}' spent {money(cost, cur)} with 0 conversions",
                    {"campaign": name, "cost": round(cost, 2)})

        if budget_limited:
            add("high", "budget_limited",
                f"{len(budget_limited)} profitable campaigns are losing impression share "
                f"to budget — you're capping winners",
                {"campaigns": sorted(budget_limited,
                                     key=lambda x: -x["lost_is_budget"])[:15]})
        if content_on:
            add("medium", "content_network_on",
                f"{len(content_on)} Search campaigns have the Display/Content network ON "
                f"(usually dilutes Search intent and spend)",
                {"campaigns": content_on[:15]})
        if thin_smart:
            add("high", "insufficient_smart_bidding_data",
                f"{len(thin_smart)} campaigns run smart bidding on <30 conversions — "
                f"too little data for the algorithm to optimize reliably",
                {"campaigns": thin_smart[:15]})

    # --- Ads: strength + RSA coverage per ad group ---
    if ads:
        ran.append("ad_copy")
        poor = []
        by_group = defaultdict(int)
        for a in ads:
            if g(a, "adGroupAd.status") != "ENABLED":
                continue
            strength = g(a, "adGroupAd.adStrength")
            ag = g(a, "adGroup.name") or g(a, "adGroup.id")
            by_group[ag] += 1
            if strength in ("POOR", "AVERAGE"):
                poor.append({"ad_group": ag, "strength": strength})
        single_rsa = [ag for ag, n in by_group.items() if n == 1]
        if poor:
            add("high", "weak_ad_strength",
                f"{len(poor)} enabled ads are POOR/AVERAGE ad strength — "
                f"weaker auction eligibility and CTR",
                {"examples": poor[:15]})
        if single_rsa:
            add("medium", "single_ad_per_group",
                f"{len(single_rsa)} ad groups run a single ad — nothing to test against",
                {"ad_groups": single_rsa[:15]})

    # --- Score: weighted toward the things that actually move money ---
    waste_pct = (max(waste_amount, kw_waste) / total_spend * 100) if total_spend else 0
    codes = Counter(f["code"] for f in findings)
    score = 100.0
    score -= min(50, waste_pct * 1.5)  # waste is the biggest lever
    if any(c in codes for c in ("no_active_conversions", "no_conversion_data")):
        score -= 20  # broken tracking poisons every other decision
    if codes.get("low_quality_score"):
        score -= 8
    if codes.get("budget_limited"):
        score -= 6
    if codes.get("weak_ad_strength"):
        score -= 5
    score -= min(8, codes.get("campaign_spend_no_conv", 0) * 4)
    score = max(0, round(score))

    sev_counts = Counter(f["severity"] for f in findings)
    summary = {
        "account": data.get("account"),
        "currency": cur,
        "date_range": data.get("date_range"),
        "total_spend": round(total_spend, 2),
        "total_conversions": round(total_conv, 1),
        "estimated_monthly_waste": round(max(waste_amount, kw_waste), 2),
        "waste_pct_of_spend": round(waste_pct, 1),
        "health_score": score,
        "severity_counts": dict(sev_counts),
        "checks_run": ran,
        "negative_keyword_candidates": len(neg_candidates),
    }
    sev_rank = {"critical": 0, "high": 1, "medium": 2}
    findings.sort(key=lambda f: sev_rank.get(f["severity"], 3))
    return summary, findings, neg_candidates


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("account", help="JSON file with GAQL query results")
    ap.add_argument("--out", default=None, help="Output directory")
    ap.add_argument("--min-spend", type=float, default=10.0,
                    help="Min spend (currency units) for a zero-conv item to count as waste")
    ap.add_argument("--top", type=int, default=15)
    args = ap.parse_args()

    try:
        with open(args.account) as f:
            data = json.load(f)
    except Exception as e:
        print(f"ERROR: could not read input JSON: {e}", file=sys.stderr)
        sys.exit(1)

    if not any(data.get(k) for k in
               ("campaigns", "keywords", "search_terms", "ads", "conversion_actions")):
        print("ERROR: input has none of the expected datasets "
              "(campaigns/keywords/search_terms/ads/conversion_actions).", file=sys.stderr)
        sys.exit(1)

    summary, findings, negs = analyze(data, args.min_spend)

    base = os.path.splitext(os.path.basename(args.account))[0]
    out_dir = args.out or os.path.dirname(args.account) or "."
    os.makedirs(out_dir, exist_ok=True)
    json_path = os.path.join(out_dir, f"{base}.audit.json")
    with open(json_path, "w") as f:
        json.dump({"summary": summary, "findings": findings,
                   "negative_keyword_candidates": negs}, f, indent=2)

    cur = summary["currency"]
    print(f"Account            : {summary['account']}  ({summary['date_range']})")
    print(f"Total spend        : {money(summary['total_spend'], cur)}")
    print(f"Conversions        : {summary['total_conversions']}")
    print(f"Estimated waste    : {money(summary['estimated_monthly_waste'], cur)}"
          f"  ({summary['waste_pct_of_spend']}% of spend)")
    print(f"Health score       : {summary['health_score']}/100")
    sc = summary["severity_counts"]
    print(f"Findings           : {sc.get('critical',0)} critical, "
          f"{sc.get('high',0)} high, {sc.get('medium',0)} medium")
    print(f"Checks run         : {', '.join(summary['checks_run']) or 'none'}")
    print("\nTop findings:")
    for fd in findings[:args.top]:
        print(f"  [{fd['severity'].upper():8}] {fd['message']}")
    if negs:
        print(f"\nTop negative-keyword candidates (zero-conversion spend):")
        for n in negs[:args.top]:
            print(f"  {money(n['cost'], cur):>14}  {n['term']}")
    print(f"\nFull findings: {json_path}")


if __name__ == "__main__":
    main()
