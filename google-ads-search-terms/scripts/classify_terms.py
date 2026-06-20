#!/usr/bin/env python3
"""
classify_terms.py — tiering engine for a Google Ads search terms report.

Search-terms analysis is pure first-party math: every term gets sorted into
Winners / Potential / Losers / Investigate by numeric thresholds, and the
patterns across terms (which words show up in waste vs. wins) are n-gram
frequency analysis. Doing that by hand across thousands of terms is slow and
inconsistent. This script does it deterministically and applies the statistical-
significance gate automatically, so a term with three clicks never gets called a
"loser."

Input is EITHER:
  - GAQL JSON: the search_term_view rows (see references/gaql-queries.md), or
  - a Search Terms CSV exported straight from the Google Ads UI.
Format is auto-detected.

Targets are optional. With --target-cpa / --target-roas the tiers are judged
against your goals; without them, the script falls back to the report's own
blended CPA and conversion rate as the benchmark, so it still works on raw data.

Usage:
    python3 classify_terms.py <report.json|report.csv> \
        [--target-cpa N] [--target-roas N] [--out DIR] [--top N]

Writes <name>.tiers.json (full classification + patterns). Stdlib only.
"""

import argparse
import csv
import json
import math
import os
import re
import sys
from collections import Counter, defaultdict

STOPWORDS = {
    "the", "a", "an", "and", "or", "for", "to", "of", "in", "on", "with", "my",
    "your", "is", "are", "best", "near", "me", "vs", "how", "what", "i", "do",
}
# Words that, when they show up in zero-conversion spend, are usually junk intent.
JUNK_HINTS = {"free", "jobs", "job", "diy", "salary", "course", "courses",
              "torrent", "crack", "used", "second", "hand", "wiki", "meaning",
              "definition", "pdf", "template", "cheap"}


def parse_number(s, decimal="dot"):
    """Tolerant numeric parse. `decimal` ('dot' US / 'comma' EU) resolves the
    1.234 ambiguity (1.234 dollars vs. 1.234 = 1234) using the file's convention."""
    if s is None:
        return 0.0
    s = str(s).strip()
    if s in ("", "--", "-", "—", " --"):
        return 0.0
    s = re.sub(r"[^\d,.\-]", "", s.replace("%", ""))
    if decimal == "comma":          # 1.234,56 -> dot is thousands, comma is decimal
        s = s.replace(".", "").replace(",", ".")
    else:                            # 1,234.56 -> comma is thousands, dot is decimal
        s = s.replace(",", "")
    try:
        return float(s)
    except ValueError:
        return 0.0


# --- Input loading ----------------------------------------------------------
def g(obj, path, default=None):
    cur = obj
    for part in path.split("."):
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            return default
    return cur


def load_terms(path):
    """Return (list of normalized term dicts, currency)."""
    with open(path, "rb") as f:
        raw = f.read()
    text = raw.decode("utf-8", errors="replace").lstrip("﻿")
    stripped = text.lstrip()
    if stripped.startswith("{") or stripped.startswith("["):
        return _load_json(json.loads(text))
    return _load_csv(text)


def _load_json(data):
    rows = data.get("search_terms") if isinstance(data, dict) else data
    rows = rows or []
    cur = data.get("currency", "") if isinstance(data, dict) else ""
    out = []
    for r in rows:
        out.append({
            "term": g(r, "searchTermView.searchTerm") or g(r, "searchTerm") or "",
            "match_type": g(r, "segments.searchTermMatchType") or "",
            "campaign": g(r, "campaign.name") or "",
            "ad_group": g(r, "adGroup.name") or "",
            "clicks": int(g(r, "metrics.clicks", 0) or 0),
            "impressions": int(g(r, "metrics.impressions", 0) or 0),
            "cost": (int(g(r, "metrics.costMicros", 0) or 0)) / 1_000_000,
            "conversions": float(g(r, "metrics.conversions", 0) or 0),
            "conv_value": float(g(r, "metrics.conversionsValue", 0) or 0),
        })
    return out, cur


CSV_MAP = {
    "search term": "term", "search keyword": "term",
    "match type": "match_type",
    "campaign": "campaign", "ad group": "ad_group",
    "clicks": "clicks", "impr": "impressions", "impressions": "impressions",
    "cost": "cost",
    "conversions": "conversions", "conv": "conversions",
    "conv value": "conv_value", "conversion value": "conv_value",
    "all conv value": "conv_value", "total conv value": "conv_value",
}


def _clean_header(h):
    return re.sub(r"\.", "", (h or "").strip().lower()).strip()


def _load_csv(text):
    rows_all = list(csv.reader(text.splitlines()))
    # Google Ads CSVs carry title/date preamble rows before the real header.
    # Match the header by an exact cell, so the "Search terms report" title row
    # (which merely *contains* "search term") isn't mistaken for it.
    start = None
    for i, row in enumerate(rows_all):
        cleaned = [_clean_header(c) for c in row]
        if "search term" in cleaned or "search keyword" in cleaned:
            start = i
            break
    if start is None:
        return [], ""
    header = rows_all[start]
    cmap = {}
    for idx, h in enumerate(header):
        key = _clean_header(h)
        if key in CSV_MAP:
            cmap[idx] = CSV_MAP[key]
    # Detect the file's decimal convention once, from cells that look like money.
    eu = len(re.findall(r"\d,\d{1,2}(?:\D|$)", text))
    us = len(re.findall(r"\d\.\d{1,2}(?:\D|$)", text))
    decimal = "comma" if eu > us else "dot"
    # Best-effort currency for display (single-account exports use one currency).
    iso = re.search(r"\b(EUR|USD|GBP|CAD|AUD|SEK|DKK|NOK|CHF)\b", text)
    cur = (iso.group(1) if iso else
           "EUR" if "€" in text else "GBP" if "£" in text else
           "USD" if "$" in text else "")
    out = []
    for row in rows_all[start + 1:]:
        if not row or all(not c.strip() for c in row):
            continue
        first = row[0].strip().lower()
        if first.startswith("total") or first.startswith("—") or first == "--":
            continue  # totals/footer rows
        rec = {"term": "", "match_type": "", "campaign": "", "ad_group": "",
               "clicks": 0, "impressions": 0, "cost": 0.0,
               "conversions": 0.0, "conv_value": 0.0}
        for idx, field in cmap.items():
            if idx >= len(row):
                continue
            val = row[idx]
            if field in ("term", "match_type", "campaign", "ad_group"):
                rec[field] = val.strip()
            else:
                rec[field] = parse_number(val, decimal)
        if rec["term"]:
            out.append(rec)
    return out, cur


# --- Classification ---------------------------------------------------------
def tokenize(term):
    return [t for t in re.findall(r"[a-z0-9]+", term.lower()) if t not in STOPWORDS]


def classify(terms, target_cpa, target_roas):
    total_cost = sum(t["cost"] for t in terms)
    total_conv = sum(t["conversions"] for t in terms)
    total_clicks = sum(t["clicks"] for t in terms)
    total_value = sum(t["conv_value"] for t in terms)

    blended_cr = (total_conv / total_clicks) if total_clicks else 0.0
    blended_cpa = (total_cost / total_conv) if total_conv else None
    blended_roas = (total_value / total_cost) if total_cost and total_value else None

    cpa_target = target_cpa if target_cpa else blended_cpa
    roas_target = target_roas if target_roas else blended_roas

    # Significance: clicks needed to trust a zero-conversion verdict.
    expected_cr = max(blended_cr, 0.01)
    sig_clicks = int(min(200, max(20, round(10 / expected_cr))))
    MIN_DIRECTIONAL = 10

    for t in terms:
        conv, cost, clicks = t["conversions"], t["cost"], t["clicks"]
        t["cpa"] = (cost / conv) if conv else None
        t["roas"] = (t["conv_value"] / cost) if cost and t["conv_value"] else None
        t["cr"] = (conv / clicks) if clicks else 0.0

        reasons = []
        if conv > 0:
            if cpa_target and t["cpa"] is not None and t["cpa"] <= cpa_target:
                reasons.append("CPA at/below target")
            if roas_target and t["roas"] is not None and t["roas"] >= roas_target:
                reasons.append("ROAS at/above target")
            if t["cr"] > blended_cr:
                reasons.append("converts above account average")
            if reasons:
                t["tier"], t["why"] = "winner", "; ".join(reasons)
                t["action"] = "Add as exact-match keyword; raise bids if below top position"
            else:
                t["tier"] = "potential"
                t["why"] = "converts but inefficiently (above target CPA / below ROAS)"
                t["action"] = "Keep; tighten landing page or bid down rather than scale"
        else:  # zero conversions
            confident_loser = clicks >= sig_clicks or (cpa_target and cost >= 2 * cpa_target)
            if confident_loser:
                t["tier"] = "loser"
                t["why"] = (f"{clicks} clicks, 0 conv"
                            + (f", spent ≥2× target CPA" if cpa_target and cost >= 2 * cpa_target else ""))
                junk = [tok for tok in tokenize(t["term"]) if tok in JUNK_HINTS]
                t["action"] = ("Add as negative — "
                               + (f"phrase negative on '{junk[0]}'" if junk
                                  else "exact negative for this term"))
            elif clicks >= MIN_DIRECTIONAL:
                t["tier"] = "potential"
                t["why"] = "traffic but no conversions yet, below significance"
                t["action"] = "Watch 2–4 weeks; check ad/landing-page match"
            else:
                t["tier"] = "investigate"
                t["why"] = "too little data to decide"
                t["action"] = "Wait for more clicks"

    summary = {
        "total_terms": len(terms),
        "total_spend": round(total_cost, 2),
        "total_conversions": round(total_conv, 1),
        "blended_cpa": round(blended_cpa, 2) if blended_cpa else None,
        "blended_conv_rate": round(blended_cr, 4),
        "target_cpa_used": round(cpa_target, 2) if cpa_target else None,
        "target_roas_used": round(roas_target, 2) if roas_target else None,
        "significance_clicks": sig_clicks,
    }
    return summary


def ngram_patterns(terms):
    """Tokens over-represented in waste vs. wins, weighted by money/conversions."""
    loser_cost = defaultdict(float)
    loser_terms = defaultdict(int)
    winner_conv = defaultdict(float)
    for t in terms:
        toks = set(tokenize(t["term"]))
        for tok in toks:
            if t["tier"] == "loser":
                loser_cost[tok] += t["cost"]
                loser_terms[tok] += 1
            elif t["tier"] == "winner":
                winner_conv[tok] += t["conversions"]

    wasting = sorted(({"token": k, "wasted_cost": round(v, 2),
                       "terms": loser_terms[k]} for k, v in loser_cost.items()),
                     key=lambda x: -x["wasted_cost"])[:15]
    winning = sorted(({"token": k, "conversions": round(v, 1)}
                      for k, v in winner_conv.items()),
                     key=lambda x: -x["conversions"])[:15]
    # Pure-junk tokens: cost a lot in losers, never appear in a winner.
    junk = sorted(({"token": k, "wasted_cost": round(v, 2), "terms": loser_terms[k]}
                   for k, v in loser_cost.items()
                   if k not in winner_conv and loser_terms[k] >= 2),
                  key=lambda x: -x["wasted_cost"])[:15]
    return {"winning_tokens": winning, "wasting_tokens": wasting,
            "loser_only_tokens": junk}


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("report", help="search_term_view JSON or Search Terms CSV")
    ap.add_argument("--target-cpa", type=float, default=None)
    ap.add_argument("--target-roas", type=float, default=None)
    ap.add_argument("--out", default=None)
    ap.add_argument("--top", type=int, default=15)
    args = ap.parse_args()

    try:
        terms, cur = load_terms(args.report)
    except Exception as e:
        print(f"ERROR: could not load report: {e}", file=sys.stderr)
        sys.exit(1)
    if not terms:
        print("ERROR: no search terms found in input.", file=sys.stderr)
        sys.exit(1)

    summary = classify(terms, args.target_cpa, args.target_roas)
    patterns = ngram_patterns(terms)

    tiers = {"winner": [], "potential": [], "loser": [], "investigate": []}
    for t in terms:
        tiers[t["tier"]].append(t)
    for k in tiers:
        tiers[k].sort(key=lambda x: -x["cost"])

    summary["currency"] = cur
    summary["tier_counts"] = {k: len(v) for k, v in tiers.items()}
    summary["wasted_spend"] = round(sum(t["cost"] for t in tiers["loser"]), 2)
    summary["winner_spend"] = round(sum(t["cost"] for t in tiers["winner"]), 2)
    summary["winner_conversions"] = round(sum(t["conversions"] for t in tiers["winner"]), 1)

    base = os.path.splitext(os.path.basename(args.report))[0]
    out_dir = args.out or os.path.dirname(args.report) or "."
    os.makedirs(out_dir, exist_ok=True)
    json_path = os.path.join(out_dir, f"{base}.tiers.json")
    capped = {k: v[:200] for k, v in tiers.items()}
    with open(json_path, "w") as f:
        json.dump({"summary": summary, "patterns": patterns, "tiers": capped}, f, indent=2)

    def fmt(x):
        return f"{cur} {x:,.0f}" if x >= 100 else f"{cur} {x:,.2f}"

    c = summary["tier_counts"]
    print(f"Terms analyzed   : {summary['total_terms']}   Spend: {fmt(summary['total_spend'])}")
    print(f"Benchmark        : target CPA {summary['target_cpa_used']}, "
          f"blended CR {summary['blended_conv_rate']*100:.1f}%, "
          f"significance ≥{summary['significance_clicks']} clicks")
    print(f"Tiers            : {c['winner']} winners, {c['potential']} potential, "
          f"{c['loser']} losers, {c['investigate']} investigate")
    print(f"Wasted (losers)  : {fmt(summary['wasted_spend'])}")
    print(f"Winner spend     : {fmt(summary['winner_spend'])}  "
          f"({summary['winner_conversions']} conv)")
    print(f"\nTop losers (block):")
    for t in tiers["loser"][:args.top]:
        print(f"  {fmt(t['cost']):>12}  {t['term']:<40}  → {t['action']}")
    print(f"\nTop winners (scale):")
    for t in tiers["winner"][:args.top]:
        print(f"  {fmt(t['cost']):>12}  {t['term']:<40}  ({t['conversions']:.0f} conv)")
    if patterns["loser_only_tokens"]:
        print(f"\nLoser-only words (strong negative candidates):")
        for tok in patterns["loser_only_tokens"][:args.top]:
            print(f"  {fmt(tok['wasted_cost']):>12}  '{tok['token']}'  in {tok['terms']} terms")
    print(f"\nFull classification: {json_path}")


if __name__ == "__main__":
    main()
