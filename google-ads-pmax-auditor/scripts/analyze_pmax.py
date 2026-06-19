#!/usr/bin/env python3
"""
analyze_pmax.py — deterministic analyzer for a Performance Max audit.

Like the account-audit script, this separates fetching (credential-specific) from
analysis (pure). It consumes the JSON results of the GAQL queries in
references/gaql-queries.md and computes the objective findings a human shouldn't
be eyeballing across asset groups: asset counts vs. targets, character-limit
violations, exact and near-duplicate text, and — the backbone of any real PMax
audit — Google's own LOW/GOOD/BEST asset performance labels.

It also fetches image assets (unless --no-fetch) to verify the URL resolves and
to read real pixel dimensions, checking each image against the minimum size and
aspect ratio for its slot. Image *visual quality* still needs a human/vision eye;
this covers the part that's measurable. Image dimensions are read from the file
header with a small built-in parser (PNG/JPEG/GIF/WebP) — no third-party deps.

Input JSON (datasets optional; checks needing a dataset are skipped):
    {
      "campaign": "PMax - Shoes",
      "currency": "EUR",
      "date_range": "LAST_30_DAYS",
      "asset_groups":        [ <gaql rows: asset_group> ],
      "asset_group_assets":  [ <gaql rows: asset_group_asset + asset inlined> ],
      "search_themes":       [ <gaql rows: asset_group_signal search themes> ],
      "campaigns":           [ <gaql rows: campaign settings> ],
      "conversion_actions":  [ <gaql rows: conversion_action> ]
    }

Usage:
    python3 analyze_pmax.py <pmax.json> [--out DIR] [--no-fetch] [--top N]
"""

import argparse
import json
import os
import re
import struct
import sys
import urllib.request
from collections import Counter, defaultdict

# --- Slot specs -------------------------------------------------------------
TEXT_LIMITS = {"HEADLINE": 30, "LONG_HEADLINE": 90, "DESCRIPTION": 90}

# (minimum, recommended) count per asset group, by field type.
TARGETS = {
    "HEADLINE": (3, 11), "LONG_HEADLINE": (1, 5), "DESCRIPTION": (2, 4),
    "MARKETING_IMAGE": (1, 5), "SQUARE_MARKETING_IMAGE": (1, 5),
    "PORTRAIT_MARKETING_IMAGE": (0, 3),
    "LOGO": (1, 1), "LANDSCAPE_LOGO": (0, 1), "YOUTUBE_VIDEO": (0, 1),
}

IMAGE_SPECS = {
    "MARKETING_IMAGE": {"ratio": 1.91, "min": (600, 314), "name": "landscape image"},
    "SQUARE_MARKETING_IMAGE": {"ratio": 1.0, "min": (300, 300), "name": "square image"},
    "PORTRAIT_MARKETING_IMAGE": {"ratio": 0.8, "min": (480, 600), "name": "portrait image"},
    "LOGO": {"ratio": 1.0, "min": (128, 128), "name": "square logo"},
    "LANDSCAPE_LOGO": {"ratio": 4.0, "min": (512, 128), "name": "landscape logo"},
}
TEXT_TYPES = set(TEXT_LIMITS)
IMAGE_TYPES = set(IMAGE_SPECS)


def g(obj, path, default=None):
    cur = obj
    for part in path.split("."):
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            return default
    return cur


# --- Image dimensions from header bytes (no PIL) ----------------------------
def image_dimensions(b):
    """Return (width, height) or None. Handles PNG, GIF, JPEG, WebP(VP8X)."""
    try:
        if b[:8] == b"\x89PNG\r\n\x1a\n" and b[12:16] == b"IHDR":
            w, h = struct.unpack(">II", b[16:24])
            return w, h
        if b[:6] in (b"GIF87a", b"GIF89a"):
            w, h = struct.unpack("<HH", b[6:10])
            return w, h
        if b[:2] == b"\xff\xd8":  # JPEG: walk segments to a SOF marker
            i = 2
            while i + 9 < len(b):
                if b[i] != 0xFF:
                    i += 1
                    continue
                marker = b[i + 1]
                if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):
                    h, w = struct.unpack(">HH", b[i + 5:i + 9])
                    return w, h
                seg_len = struct.unpack(">H", b[i + 2:i + 4])[0]
                i += 2 + seg_len
            return None
        if b[:4] == b"RIFF" and b[8:12] == b"WEBP":
            chunk = b[12:16]
            if chunk == b"VP8X":
                w = 1 + (b[24] | b[25] << 8 | b[26] << 16)
                h = 1 + (b[27] | b[28] << 8 | b[29] << 16)
                return w, h
            if chunk == b"VP8 ":
                w = struct.unpack("<H", b[26:28])[0] & 0x3FFF
                h = struct.unpack("<H", b[28:30])[0] & 0x3FFF
                return w, h
    except Exception:
        return None
    return None


def fetch_bytes(url, limit=2_000_000):
    if url.startswith("file://"):
        url = url[7:]
    if re.match(r"^https?://", url, re.IGNORECASE):
        req = urllib.request.Request(url, headers={"User-Agent": "pmax-auditor/1.0"})
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.read(limit)
    with open(url, "rb") as f:
        return f.read(limit)


def tokens(text):
    return set(re.findall(r"[a-z0-9]+", (text or "").lower()))


def analyze(data, fetch):
    cur = data.get("currency", "")
    findings = []
    ran = []

    groups = {str(g(ag, "assetGroup.id")): ag for ag in (data.get("asset_groups") or [])}
    aga = data.get("asset_group_assets") or []
    themes = data.get("search_themes") or []
    campaigns = data.get("campaigns") or []
    conv_actions = data.get("conversion_actions") or []

    def add(sev, code, msg, detail=None):
        findings.append({"severity": sev, "code": code, "message": msg,
                         "detail": detail or {}})

    # Organize assets by group + field type.
    by_group = defaultdict(lambda: defaultdict(list))
    label_counts = Counter()
    low_assets = []
    if aga:
        ran.append("assets")
        for row in aga:
            ag_id = str(g(row, "assetGroup.id"))
            ftype = g(row, "assetGroupAsset.fieldType")
            label = g(row, "assetGroupAsset.performanceLabel")
            text = g(row, "asset.textAsset.text")
            img_url = g(row, "asset.imageAsset.fullSize.url")
            img_w = g(row, "asset.imageAsset.fullSize.widthPixels")
            img_h = g(row, "asset.imageAsset.fullSize.heightPixels")
            video = g(row, "asset.youtubeVideoAsset.youtubeVideoId")
            item = {"field_type": ftype, "label": label, "text": text,
                    "image_url": img_url, "image_w": img_w, "image_h": img_h,
                    "video": video, "group": ag_id}
            by_group[ag_id][ftype].append(item)
            if label:
                label_counts[label] += 1
            if label == "LOW":
                low_assets.append(item)

    # --- Backbone: Google performance labels ---
    if label_counts:
        ran.append("performance_labels")
        if low_assets:
            detail = []
            for a in low_assets[:40]:
                what = a["text"] or a["image_url"] or (f"video:{a['video']}" if a["video"] else "?")
                detail.append({"group": a["group"], "field_type": a["field_type"], "asset": what})
            add("high", "low_performance_assets",
                f"{len(low_assets)} assets are rated LOW by Google — replace these first; "
                f"they drag down ad combinations and eligibility",
                {"assets": detail})
        graded = label_counts.get("LOW", 0) + label_counts.get("GOOD", 0) + label_counts.get("BEST", 0)
        best = label_counts.get("BEST", 0)
        if graded >= 5 and best / graded < 0.2:
            add("medium", "few_best_assets",
                f"Only {best}/{graded} graded assets are BEST — the creative ceiling is low; "
                f"feed in stronger variants")

    # --- Per-group quantity + char limits + duplicates ---
    if by_group:
        ran.append("coverage")
        for ag_id, fields in by_group.items():
            name = g(groups.get(ag_id, {}), "assetGroup.name") or ag_id

            # Quantity vs targets.
            for ftype, (mn, rec) in TARGETS.items():
                count = len(fields.get(ftype, []))
                label_name = ftype.replace("_", " ").title()
                if count < mn:
                    add("critical", "below_minimum_assets",
                        f"[{name}] {label_name}: {count}/{mn} — below the minimum to serve",
                        {"group": name, "field_type": ftype, "count": count, "min": mn})
                elif count < rec:
                    add("medium", "below_recommended_assets",
                        f"[{name}] {label_name}: {count}, recommended {rec} — more variety = more combinations",
                        {"group": name, "field_type": ftype, "count": count, "recommended": rec})

            # Text: char limits + duplicates + near-duplicates.
            for ftype in TEXT_TYPES:
                items = fields.get(ftype, [])
                limit = TEXT_LIMITS[ftype]
                texts = []
                over = []
                for it in items:
                    t = (it["text"] or "").strip()
                    texts.append(t)
                    if len(t) > limit:
                        over.append({"text": t, "len": len(t), "limit": limit})
                if over:
                    add("critical", "text_over_limit",
                        f"[{name}] {len(over)} {ftype.lower()} over the {limit}-char limit (won't serve)",
                        {"group": name, "items": over})

                lowered = [t.lower() for t in texts if t]
                dup = [t for t, c in Counter(lowered).items() if c > 1]
                if dup:
                    add("high", "duplicate_text",
                        f"[{name}] exact duplicate {ftype.lower()}(s): {len(dup)} — wasted slots, fewer combinations",
                        {"group": name, "duplicates": dup[:10]})

                # Near-duplicates (high token overlap) within headlines/long headlines.
                if ftype in ("HEADLINE", "LONG_HEADLINE"):
                    near = []
                    toks = [(t, tokens(t)) for t in texts if t]
                    for i in range(len(toks)):
                        for j in range(i + 1, len(toks)):
                            a, ta = toks[i]
                            bb, tb = toks[j]
                            if ta and tb:
                                jac = len(ta & tb) / len(ta | tb)
                                if 0.8 <= jac < 1.0:
                                    near.append([a, bb])
                    if near:
                        add("medium", "near_duplicate_text",
                            f"[{name}] {len(near)} near-identical {ftype.lower()} pairs — "
                            f"they add little and limit the angles Google can test",
                            {"group": name, "pairs": near[:8]})

            # Ad strength per group.
            strength = g(groups.get(ag_id, {}), "assetGroup.adStrength")
            if strength in ("POOR", "AVERAGE"):
                add("high", "weak_ad_strength",
                    f"[{name}] ad strength is {strength} — add assets/variety to lift it",
                    {"group": name, "ad_strength": strength})

            # Image coverage: every group should have landscape + square; portrait recommended.
            for ftype in ("MARKETING_IMAGE", "SQUARE_MARKETING_IMAGE"):
                if not fields.get(ftype):
                    add("high", "missing_image_format",
                        f"[{name}] no {IMAGE_SPECS[ftype]['name']} — Google can't serve some placements",
                        {"group": name, "field_type": ftype})

    # --- Image fetch + dimension/aspect check ---
    image_items = [it for fields in by_group.values()
                   for ft in IMAGE_TYPES for it in fields.get(ft, [])]
    if image_items:
        ran.append("image_dimensions")
        checked = {}
        broken, low_res, wrong_ratio = [], [], []
        for it in image_items:
            url = it["image_url"]
            spec = IMAGE_SPECS[it["field_type"]]
            w = h = None
            if fetch and url and url not in checked:
                try:
                    w, h = image_dimensions(fetch_bytes(url)) or (None, None)
                    checked[url] = (w, h)
                except Exception:
                    broken.append({"group": it["group"], "url": url})
                    continue
            elif url in checked:
                w, h = checked[url]
            if w is None:  # fall back to dimensions GAQL gave us
                try:
                    w, h = int(it["image_w"]), int(it["image_h"])
                except (TypeError, ValueError):
                    w = h = None
            if not w or not h:
                continue
            mn_w, mn_h = spec["min"]
            if w < mn_w or h < mn_h:
                low_res.append({"group": it["group"], "name": spec["name"],
                                "size": f"{w}x{h}", "min": f"{mn_w}x{mn_h}"})
            ratio = w / h
            if abs(ratio - spec["ratio"]) / spec["ratio"] > 0.1:
                wrong_ratio.append({"group": it["group"], "name": spec["name"],
                                    "size": f"{w}x{h}", "expected_ratio": spec["ratio"]})
        if broken:
            add("critical", "broken_image_url",
                f"{len(broken)} image asset URLs did not resolve", {"images": broken[:15]})
        if low_res:
            add("high", "low_resolution_image",
                f"{len(low_res)} images are below the minimum size for their slot",
                {"images": low_res[:15]})
        if wrong_ratio:
            add("medium", "wrong_aspect_ratio",
                f"{len(wrong_ratio)} images don't match the expected aspect ratio for their slot",
                {"images": wrong_ratio[:15]})

    # --- Search themes (audience signals) ---
    if by_group:
        ran.append("search_themes")
        groups_with_themes = {str(g(t, "assetGroup.id")) for t in themes}
        missing = [g(groups.get(ag, {}), "assetGroup.name") or ag
                   for ag in by_group if ag not in groups_with_themes]
        if themes and missing:
            add("medium", "missing_search_themes",
                f"{len(missing)} asset groups have no search-theme audience signal — "
                f"you're leaning entirely on Google's automation to find intent",
                {"groups": missing[:15]})
        elif not themes:
            add("medium", "no_search_themes_data",
                "No search-theme/audience-signal data provided — strong signals materially speed up learning")

    # --- Settings: URL expansion + conversion tracking ---
    if campaigns:
        ran.append("campaign_settings")
        for c in campaigns:
            if g(c, "campaign.urlExpansionOptOut") is False:
                add("medium", "url_expansion_on",
                    f"Final URL expansion is ON for '{g(c,'campaign.name')}' — confirm it isn't "
                    f"sending traffic to thin/irrelevant pages; add URL exclusions or a page feed")

    if conv_actions:
        ran.append("conversion_tracking")
        enabled = [a for a in conv_actions if g(a, "conversionAction.status") == "ENABLED"]
        if not enabled:
            add("critical", "no_active_conversions",
                "No ENABLED conversion actions — PMax is optimizing blind")
        else:
            no_value = all(not float(g(a, "conversionAction.valueSettings.defaultValue") or 0)
                           for a in enabled)
            if no_value:
                add("high", "conversions_no_value",
                    "No conversion value set — PMax leans on value; tROAS can't work without it")

    # --- Score + grade ---
    sev = Counter(f["severity"] for f in findings)
    score = max(0, 100 - sev["critical"] * 12 - sev["high"] * 6 - sev["medium"] * 2)
    grade = ("A" if score >= 90 else "B" if score >= 80 else "C" if score >= 70
             else "D" if score >= 60 else "F")
    summary = {
        "campaign": data.get("campaign"),
        "currency": cur,
        "date_range": data.get("date_range"),
        "asset_groups": len(by_group),
        "health_score": score,
        "grade": grade,
        "performance_labels": dict(label_counts),
        "low_assets": len(low_assets),
        "severity_counts": dict(sev),
        "checks_run": ran,
        "image_fetch": fetch,
    }
    rank = {"critical": 0, "high": 1, "medium": 2}
    findings.sort(key=lambda f: rank.get(f["severity"], 3))
    return summary, findings


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pmax", help="JSON file with GAQL query results")
    ap.add_argument("--out", default=None)
    ap.add_argument("--no-fetch", action="store_true",
                    help="Skip downloading images; use GAQL-provided dimensions only")
    ap.add_argument("--top", type=int, default=20)
    args = ap.parse_args()

    try:
        with open(args.pmax) as f:
            data = json.load(f)
    except Exception as e:
        print(f"ERROR: could not read input JSON: {e}", file=sys.stderr)
        sys.exit(1)

    if not any(data.get(k) for k in
               ("asset_groups", "asset_group_assets", "campaigns", "conversion_actions")):
        print("ERROR: input has none of the expected datasets.", file=sys.stderr)
        sys.exit(1)

    summary, findings = analyze(data, fetch=not args.no_fetch)

    base = os.path.splitext(os.path.basename(args.pmax))[0]
    out_dir = args.out or os.path.dirname(args.pmax) or "."
    os.makedirs(out_dir, exist_ok=True)
    json_path = os.path.join(out_dir, f"{base}.audit.json")
    with open(json_path, "w") as f:
        json.dump({"summary": summary, "findings": findings}, f, indent=2)

    s = summary
    print(f"Campaign       : {s['campaign']}  ({s['date_range']})")
    print(f"Asset groups   : {s['asset_groups']}")
    print(f"Grade          : {s['grade']}  ({s['health_score']}/100)")
    print(f"Perf labels    : {s['performance_labels'] or 'none provided'}")
    sc = s["severity_counts"]
    print(f"Findings       : {sc.get('critical',0)} critical, {sc.get('high',0)} high, {sc.get('medium',0)} medium")
    print(f"Checks run     : {', '.join(s['checks_run']) or 'none'}")
    print("\nTop findings:")
    for fd in findings[:args.top]:
        print(f"  [{fd['severity'].upper():8}] {fd['message']}")
    print(f"\nFull findings: {json_path}")


if __name__ == "__main__":
    main()
