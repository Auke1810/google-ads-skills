#!/usr/bin/env python3
"""
audit_feed.py — mechanical auditor for Google Shopping product feeds.

Handles the deterministic, high-volume part of a feed audit: parsing a real
feed (CSV / TSV / Google Shopping XML, from a local file OR a URL such as a
published Google Sheet or a Merchant Center feed URL), then flagging every row
that breaks a checkable rule — character limits, missing brand, ALL-CAPS,
promotional text, missing required attributes, keyword stuffing, and so on.

The model's job is what comes AFTER this: interpreting the findings, rewriting
the worst titles, and writing the final report. This script exists so that part
never has to eyeball thousands of rows by hand.

Usage:
    python audit_feed.py <feed.csv|feed.tsv|feed.xml|URL> [--out DIR] [--top N]

Outputs (written to --out, default: alongside the input / current dir):
    <name>.audit.json   full structured findings (every flagged row)
    <name>.audit.md     human-readable violation tables, severity-tiered

Also prints a compact summary + the worst N rows to stdout so the caller can
read the shape of the problem without loading the whole file into context.

No third-party dependencies — standard library only.
"""

import argparse
import csv
import io
import json
import os
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from collections import Counter

# ----------------------------------------------------------------------------
# Spec constants (Google Merchant Center). Kept here so the rules have one home.
# ----------------------------------------------------------------------------
TITLE_MAX = 150           # hard limit; over this is truncated/disapproval risk
TITLE_RECOMMENDED_MIN = 30  # below this a title is almost always too thin
TITLE_VISIBLE = 70        # most placements only render ~first 70 chars
DESC_MAX = 5000           # hard limit
DESC_MIN = 100            # below this is too thin to describe the product

# Promotional / policy-violating language that is not allowed in titles, and
# discouraged in descriptions. Matched case-insensitively as whole phrases.
PROMO_PATTERNS = [
    r"\bsale\b", r"\bon sale\b", r"\bdiscount(ed|s)?\b", r"\bclearance\b",
    r"\bfree shipping\b", r"\bfree delivery\b", r"\bbuy now\b", r"\border now\b",
    r"\bbest price\b", r"\blowest price\b", r"\bcheapest\b", r"\bbest seller\b",
    r"\b\d{1,3}\s?% ?off\b", r"\bsave \$?\d+\b", r"\blimited time\b",
    r"\bhurry\b", r"\bdeal\b", r"\bspecial offer\b", r"\bhot\b",
]
PROMO_RE = re.compile("|".join(PROMO_PATTERNS), re.IGNORECASE)

# Tokens that are legitimately uppercase and must NOT count as "shouting".
CAPS_ALLOWLIST = {
    "XS", "XXL", "XXXL", "XL", "XXS", "USB", "LED", "HDMI", "SSD", "HDD",
    "RAM", "ROM", "GB", "TB", "MB", "KG", "ML", "UV", "LCD", "OLED", "QLED",
    "HD", "UHD", "4K", "8K", "GPS", "NFC", "RGB", "PC", "TV", "AC", "DC",
    "USA", "UK", "EU", "II", "III", "IV", "SPF", "PRO", "MAX", "SE", "M3",
    "M2", "M1", "CPU", "GPU", "DDR", "PSU", "ATX", "IP67", "IP68",
}

# Canonical field -> accepted header aliases (lowercased, stripped, no "g:").
FIELD_ALIASES = {
    "id": {"id", "item id", "item_id", "sku", "offer id", "offer_id"},
    "title": {"title", "product title", "name", "product name"},
    "description": {"description", "product description", "desc"},
    "link": {"link", "url", "product url", "product_url", "product link"},
    "image_link": {"image_link", "image link", "image url", "image_url", "image"},
    "price": {"price"},
    "availability": {"availability", "stock status", "stock_status", "in stock"},
    "brand": {"brand", "brand name", "manufacturer"},
    "gtin": {"gtin", "ean", "upc", "barcode", "isbn"},
    "mpn": {"mpn", "manufacturer part number"},
    "google_product_category": {
        "google_product_category", "google product category", "google category",
    },
    "product_type": {"product_type", "product type", "category", "categories"},
    "condition": {"condition"},
    "color": {"color", "colour"},
    "size": {"size"},
    "gender": {"gender"},
    "age_group": {"age_group", "age group"},
}

# Required for essentially every product.
REQUIRED_UNIVERSAL = [
    "id", "title", "description", "link", "image_link", "price", "availability",
]
# brand OR gtin OR mpn must be present (identity).
IDENTITY_FIELDS = ["brand", "gtin", "mpn"]
# Apparel needs these on top, when the category says it's apparel.
APPAREL_REQUIRED = ["gender", "age_group", "color", "size"]


def _norm_header(h):
    h = (h or "").strip().lower()
    if h.startswith("g:"):
        h = h[2:]
    h = h.replace("-", " ").replace("_", " ").strip()
    return h


def _canon_map(headers):
    """Map raw headers -> canonical field names."""
    alias_to_canon = {}
    for canon, aliases in FIELD_ALIASES.items():
        for a in aliases:
            alias_to_canon[a.replace("_", " ")] = canon
    out = {}
    for h in headers:
        nh = _norm_header(h)
        if nh in alias_to_canon:
            out[h] = alias_to_canon[nh]
    return out


def _read_bytes(source):
    if re.match(r"^https?://", source, re.IGNORECASE):
        # Nudge Google Sheets share links toward a CSV export.
        m = re.match(r"https://docs.google.com/spreadsheets/d/([^/]+)", source)
        if m and "export" not in source:
            source = (
                f"https://docs.google.com/spreadsheets/d/{m.group(1)}/export?format=csv"
            )
        req = urllib.request.Request(source, headers={"User-Agent": "feed-auditor/1.0"})
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.read(), source
    with open(source, "rb") as f:
        return f.read(), source


def parse_feed(source):
    """Return (rows, fields_present) where rows is a list of canonical dicts."""
    raw, resolved = _read_bytes(source)
    text = raw.decode("utf-8", errors="replace").lstrip("﻿")
    stripped = text.lstrip()

    # XML (Google Shopping RSS 2.0)
    if stripped.startswith("<"):
        return _parse_xml(text)

    # Delimited text: sniff comma vs tab.
    sample = text[:4096]
    delim = "\t" if sample.count("\t") > sample.count(",") else ","
    reader = csv.DictReader(io.StringIO(text), delimiter=delim)
    headers = reader.fieldnames or []
    cmap = _canon_map(headers)
    rows = []
    for raw_row in reader:
        row = {}
        for h, v in raw_row.items():
            if h in cmap:
                row[cmap[h]] = (v or "").strip()
        rows.append(row)
    fields_present = set(cmap.values())
    return rows, fields_present


def _parse_xml(text):
    root = ET.fromstring(text)

    def local(tag):
        return tag.split("}")[-1].lower()

    items = [el for el in root.iter() if local(el.tag) == "item"]
    rows, fields_present = [], set()
    alias_to_canon = {}
    for canon, aliases in FIELD_ALIASES.items():
        for a in aliases:
            alias_to_canon[a.replace("_", " ")] = canon
    for item in items:
        row = {}
        for child in item:
            key = _norm_header(local(child.tag))
            if key in alias_to_canon:
                canon = alias_to_canon[key]
                row[canon] = (child.text or "").strip()
                fields_present.add(canon)
        rows.append(row)
    return rows, fields_present


# ----------------------------------------------------------------------------
# Checks. Each returns a list of (severity, code, message) for one product.
# ----------------------------------------------------------------------------
STOPWORDS = {
    "the", "and", "for", "with", "your", "you", "our", "men", "women", "kids",
    "new", "set", "pack", "size", "color", "colour", "of", "in", "to",
}


def check_product(row, is_apparel):
    issues = []
    title = row.get("title", "")
    desc = row.get("description", "")

    # --- Required attributes (disapproval risk) ---
    for f in REQUIRED_UNIVERSAL:
        if not row.get(f):
            issues.append(("critical", "missing_required",
                           f"Missing required attribute: {f}"))
    if not any(row.get(f) for f in IDENTITY_FIELDS):
        issues.append(("critical", "missing_identity",
                       "No brand, gtin, or mpn — product identity is required"))
    if is_apparel:
        for f in APPAREL_REQUIRED:
            if not row.get(f):
                issues.append(("high", "missing_apparel_attr",
                               f"Apparel product missing required attribute: {f}"))

    # --- Title ---
    if title:
        n = len(title)
        if n > TITLE_MAX:
            issues.append(("critical", "title_over_max",
                           f"Title is {n} chars (max {TITLE_MAX}); will be truncated"))
        elif n < TITLE_RECOMMENDED_MIN:
            issues.append(("high", "title_too_short",
                           f"Title is only {n} chars; too thin to match queries"))
        elif n < TITLE_VISIBLE:
            issues.append(("medium", "title_short",
                           f"Title is {n} chars; aim for {TITLE_VISIBLE}-{TITLE_MAX} to use visible space"))

        if PROMO_RE.search(title):
            issues.append(("critical", "title_promo",
                           "Title contains promotional text (policy violation)"))

        # Brand should appear in the title.
        brand = row.get("brand", "")
        if brand and brand.lower() not in title.lower():
            issues.append(("high", "title_missing_brand",
                           f"Brand '{brand}' not present in title"))

        # ALL-CAPS shouting.
        shouty = [w for w in re.findall(r"[A-Za-z]{4,}", title)
                  if w.isupper() and w.upper() not in CAPS_ALLOWLIST]
        letters = [c for c in title if c.isalpha()]
        caps_ratio = sum(c.isupper() for c in letters) / len(letters) if letters else 0
        if len(shouty) >= 2 or caps_ratio > 0.6:
            issues.append(("high", "title_caps",
                           "Excessive capitalization in title"))

        # Keyword stuffing: a meaningful word repeated 3+ times.
        words = [w.lower() for w in re.findall(r"[A-Za-z]{3,}", title)]
        counts = Counter(w for w in words if w not in STOPWORDS)
        stuffed = [w for w, c in counts.items() if c >= 3]
        if stuffed:
            issues.append(("high", "title_stuffing",
                           f"Possible keyword stuffing: {', '.join(stuffed)} repeated"))

    # --- Description ---
    if "description" in row:
        if not desc:
            pass  # already caught as missing_required
        else:
            dn = len(desc)
            if dn > DESC_MAX:
                issues.append(("critical", "desc_over_max",
                               f"Description is {dn} chars (max {DESC_MAX})"))
            elif dn < DESC_MIN:
                issues.append(("medium", "desc_too_short",
                               f"Description is only {dn} chars; add features and specs"))
            if re.search(r"<[a-z/][^>]*>", desc, re.IGNORECASE):
                issues.append(("medium", "desc_html",
                               "Description contains HTML tags"))
            if re.search(r"https?://", desc):
                issues.append(("high", "desc_link",
                               "Description contains a link to another site (not allowed)"))
            if PROMO_RE.search(desc):
                issues.append(("medium", "desc_promo",
                               "Description contains promotional language"))

    # --- Category ---
    # Only flag when there's no breadcrumb depth anywhere: a full Google product
    # category compensates for a shallow product_type, so don't punish a clean row.
    pt = row.get("product_type", "")
    gpc = row.get("google_product_category", "")
    if pt and ">" not in pt and ">" not in gpc:
        issues.append(("medium", "category_generic",
                       f"Product type '{pt}' is shallow and no full Google category path is set"))

    return issues


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("feed", help="Feed file (.csv/.tsv/.xml) or URL")
    ap.add_argument("--out", default=None, help="Output directory (default: input dir / cwd)")
    ap.add_argument("--top", type=int, default=20, help="How many worst rows to print")
    args = ap.parse_args()

    try:
        rows, fields_present = parse_feed(args.feed)
    except Exception as e:
        print(f"ERROR: could not parse feed: {e}", file=sys.stderr)
        sys.exit(1)

    if not rows:
        print("ERROR: no products found in feed.", file=sys.stderr)
        sys.exit(1)

    # Apparel detection from the category field (feed-level heuristic).
    apparel_hint = any(
        "apparel" in (r.get("google_product_category", "") + r.get("product_type", "")).lower()
        or "clothing" in (r.get("google_product_category", "") + r.get("product_type", "")).lower()
        for r in rows
    )

    findings = []
    sev_counts = Counter()
    code_counts = Counter()
    for i, row in enumerate(rows):
        is_apparel = apparel_hint and (
            "apparel" in (row.get("google_product_category", "") + row.get("product_type", "")).lower()
            or "clothing" in (row.get("google_product_category", "") + row.get("product_type", "")).lower()
            or apparel_hint  # if the feed is clearly an apparel feed, apply to all
        )
        issues = check_product(row, is_apparel)
        for sev, code, msg in issues:
            sev_counts[sev] += 1
            code_counts[code] += 1
        if issues:
            findings.append({
                "id": row.get("id") or f"row-{i+1}",
                "title": row.get("title", ""),
                "issues": [{"severity": s, "code": c, "message": m} for s, c, m in issues],
                "worst": min(("critical", "high", "medium").index(issues[0][0])
                             if issues else 3, 3),
            })

    sev_rank = {"critical": 0, "high": 1, "medium": 2}
    for f in findings:
        f["worst"] = min(sev_rank[i["severity"]] for i in f["issues"])
    findings.sort(key=lambda f: (f["worst"], -len(f["issues"])))

    total = len(rows)
    clean = total - len(findings)
    # Health score: weighted by severity, normalized to feed size.
    penalty = sev_counts["critical"] * 3 + sev_counts["high"] * 2 + sev_counts["medium"] * 1
    score = max(0, round(100 - (penalty / total) * 12))

    summary = {
        "products_analyzed": total,
        "products_clean": clean,
        "products_with_issues": len(findings),
        "health_score": score,
        "severity_counts": dict(sev_counts),
        "issue_counts": dict(code_counts.most_common()),
        "fields_present": sorted(fields_present),
        "apparel_feed": apparel_hint,
    }

    # Resolve output paths.
    base = os.path.basename(re.sub(r"\?.*$", "", args.feed)) or "feed"
    base = re.sub(r"\.[^.]+$", "", base) or "feed"
    out_dir = args.out or (os.path.dirname(args.feed) if os.path.exists(args.feed) else ".")
    os.makedirs(out_dir, exist_ok=True)
    json_path = os.path.join(out_dir, f"{base}.audit.json")
    md_path = os.path.join(out_dir, f"{base}.audit.md")

    with open(json_path, "w") as f:
        json.dump({"summary": summary, "findings": findings}, f, indent=2)

    _write_md(md_path, summary, findings)

    # ---- stdout: compact, context-friendly ----
    print(f"Products analyzed : {total}")
    print(f"Clean             : {clean}  ({round(clean/total*100)}%)")
    print(f"With issues       : {len(findings)}")
    print(f"Health score      : {score}/100")
    print(f"Severity          : "
          f"{sev_counts['critical']} critical, {sev_counts['high']} high, "
          f"{sev_counts['medium']} medium")
    print("\nMost common issues:")
    for code, c in code_counts.most_common(10):
        print(f"  {c:>5}  {code}")
    print(f"\nWorst {min(args.top, len(findings))} products:")
    for f in findings[:args.top]:
        codes = ", ".join(sorted({i["code"] for i in f["issues"]}))
        t = (f["title"][:60] + "…") if len(f["title"]) > 60 else f["title"]
        print(f"  [{f['id']}] {t or '(no title)'}\n        {codes}")
    print(f"\nFull findings : {json_path}")
    print(f"Report (md)   : {md_path}")


def _write_md(path, summary, findings):
    sev_order = {"critical": 0, "high": 1, "medium": 2}
    by_sev = {"critical": [], "high": [], "medium": []}
    for f in findings:
        worst = min(f["issues"], key=lambda i: sev_order[i["severity"]])["severity"]
        by_sev[worst].append(f)

    lines = []
    lines.append("# Shopping Feed Audit — Mechanical Findings\n")
    s = summary
    lines.append(f"- Products analyzed: **{s['products_analyzed']}**")
    lines.append(f"- Clean: **{s['products_clean']}** | With issues: **{s['products_with_issues']}**")
    lines.append(f"- Health score: **{s['health_score']}/100**")
    lines.append(f"- Severity: {s['severity_counts'].get('critical',0)} critical, "
                 f"{s['severity_counts'].get('high',0)} high, "
                 f"{s['severity_counts'].get('medium',0)} medium\n")

    titles = {"critical": "Critical (disapproval / truncation risk)",
              "high": "High (hurts visibility & relevance)",
              "medium": "Medium (optimization)"}
    for sev in ("critical", "high", "medium"):
        group = by_sev[sev]
        if not group:
            continue
        lines.append(f"\n## {titles[sev]} — {len(group)} products\n")
        lines.append("| Product ID | Title | Issues |")
        lines.append("|---|---|---|")
        for f in group[:200]:
            t = f["title"].replace("|", "\\|")
            t = (t[:70] + "…") if len(t) > 70 else t
            msgs = "; ".join(i["message"] for i in f["issues"]).replace("|", "\\|")
            lines.append(f"| {f['id']} | {t or '(none)'} | {msgs} |")
        if len(group) > 200:
            lines.append(f"\n_…and {len(group)-200} more (see JSON)._")
    with open(path, "w") as f:
        f.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
