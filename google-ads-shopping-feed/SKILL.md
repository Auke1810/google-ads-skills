---
name: google-ads-shopping-feed
description: >-
  Audit and optimize Google Shopping / Merchant Center product feeds — flag the
  rows that cause disapprovals, truncated titles, low impression share, and weak
  relevance, then rewrite the worst titles and descriptions. Use this whenever
  someone shares a product feed (CSV, TSV, XML, a Google Sheet, or a Merchant
  Center feed URL) and wants it checked or improved, AND whenever they describe a
  Shopping symptom without naming the feed — "my product ads barely get
  impressions", "products keep getting disapproved", "rewrite these product
  titles for Google", "why is my Shopping campaign underperforming", "clean up my
  Merchant Center data". Reach for it even when the user just pastes a few product
  titles and asks if they're good.
---

# Google Shopping Feed Auditor

Find and fix the feed issues that quietly throttle Shopping performance:
disapprovals, titles truncated past 150 characters, missing brand, promotional
text Google rejects, and thin titles that never match the queries they should.

The mechanical, high-volume checks run in a script so they're fast and exact
across thousands of rows. Your job is the judgment the script can't do: reading
the pattern, **rewriting the worst titles and descriptions**, and turning the
findings into a report the merchant can act on.

## Workflow

1. **Get the feed into a file the script can read.** See *Getting the feed* below.
2. **Run the auditor** to get every mechanical violation, severity-tiered:
   ```bash
   python3 scripts/audit_feed.py <feed.csv|feed.tsv|feed.xml|URL> --out <dir>
   ```
   (Use `python` if that's what resolves to Python 3 on the system.)
   It prints a summary + the worst rows, and writes `<name>.audit.json` (full
   findings) and `<name>.audit.md` (violation tables). Read the JSON for detail.
3. **Triage and explain.** Lead with the critical issues (these block products or
   waste the title's visible space), then high, then medium. Group by *pattern*,
   not row-by-row — "47 products are missing brand in the title" is more useful
   than 47 separate lines.
4. **Rewrite the worst offenders.** This is the high-value part. For the
   highest-impact products (most impressions to gain, or outright disapproved),
   produce before/after titles and improved descriptions using the patterns below.
5. **Do the checks the script can't.** Image quality, landing-page price/stock
   match, and counterfeit/policy judgment need a human eye — see *Beyond the
   script*.
6. **Deliver the report** using the template below.

## Getting the feed

Feeds rarely arrive as neatly pasted rows — they live in files and tools. Handle
the real cases:

- **CSV / TSV export**: pass the file path directly. The script sniffs the
  delimiter and maps common header variants (`Title`, `product title`, `g:title`
  all resolve to the same field).
- **Google Shopping XML** (RSS 2.0 with the `g:` namespace): pass the file or its
  URL directly.
- **Google Sheet**: ask for the share link. The script auto-rewrites a
  `docs.google.com/spreadsheets/d/<id>/...` link to its CSV export, *if the sheet
  is link-viewable*. If it's private, ask the user to **File → Download → CSV**
  and share that.
- **Merchant Center**: ask for the feed URL (Merchant Center serves the same XML/
  TSV), or have them export the products. If they only have screenshots or a
  handful of products, just audit those inline using the rules below — no script
  needed for a few rows.

If you're unsure what you received, parse a few rows first and confirm the fields
look right before running the full audit.

## What the script flags (and why it matters)

The codes in the JSON map to concrete performance consequences:

| Code | Severity | Why it hurts |
|------|----------|--------------|
| `missing_required` / `missing_identity` | Critical | Product gets disapproved; zero impressions |
| `title_over_max` | Critical | Past 150 chars the title is truncated mid-phrase |
| `title_promo` | Critical | "Sale", "free shipping", "% off" in titles is a policy violation |
| `desc_over_max` / `desc_link` | Critical/High | Over 5,000 chars or external links get rejected |
| `title_missing_brand` | High | Branded queries are the highest-intent traffic; no brand = no match |
| `title_caps` / `title_stuffing` | High | Shouting and repetition read as spam and erode trust/CTR |
| `title_too_short` | High | A 1-3 word title can't match the long-tail queries that convert |
| `missing_apparel_attr` | High | Apparel without gender/age_group/color/size is filtered out of many surfaces |
| `title_short` | Medium | Under ~70 chars wastes the most visible real estate you get |
| `desc_too_short` / `desc_html` | Medium | Thin or HTML-laden descriptions reduce relevance signals |
| `category_generic` | Medium | A shallow category mismatches queries and bidding |

The first ~70 characters of a title carry the most weight: that's what renders in
most placements, and it's where the matching algorithm leans hardest. So when you
rewrite, front-load brand and product type and push optional attributes later.

## Title rewrite patterns

A strong title is `[Brand] + [Product] + [Key Attributes] + [Model/SKU]`, ordered
by how much a shopper would search for each part. Tune the attribute order by
vertical:

| Vertical | Pattern | Example |
|----------|---------|---------|
| Apparel | Brand · Gender · Type · Style/Fit · Color · Size | `Nike Women's Running Shorts Tempo Dri-FIT Black` |
| Electronics | Brand · Line · Model · Key Spec · Capacity | `Apple MacBook Pro 14-inch M3 Pro 18GB RAM 512GB SSD` |
| Home & Garden | Brand · Type · Material · Size · Color | `Cuisinart Stainless Steel Cookware Set 12-Piece` |
| Beauty | Brand · Line · Type · Variant · Size | `CeraVe Hydrating Facial Cleanser Normal to Dry 16 oz` |

**Before → After:**

Input: `SALE!! Running Shoes 50% OFF Best Price`
Output: `Nike Air Max 90 Men's Running Shoes Black Size 10`
Changes: removed promo text (policy violation), added brand + model + key
attributes + size, front-loaded the brand.

Input: `NIKE AIR MAX RUNNING SHOES SHOES SHOES ATHLETIC`
Output: `Nike Air Max 90 Men's Athletic Running Shoes White`
Changes: fixed shouting, removed the repeated "shoes" stuffing, added the model
and color a shopper would actually search.

## Description guidance

Descriptions don't need the title's keyword discipline, but they feed relevance
and should read like a person wrote them. A reliable structure:

```
[One-line hook: what the product is]
[3-5 key features / benefits]
[Specifications: size, material, dimensions]
[Who it's for / when to use it]
```

Keep them 500-1,000 characters, no HTML, no links to other sites, no promo
language, no competitor mentions.

## Beyond the script (human judgment)

The script can't see these — check them yourself when the data is available:

- **Image**: main image on a white/neutral background, product filling ~75-90% of
  the frame, no watermarks, overlays, or placeholder images. (≥100×100 px, 800×800
  recommended.)
- **Landing page match**: price and availability in the feed must match the
  product page exactly, or the product is disapproved for mismatch.
- **Policy judgment**: counterfeit/replica wording, restricted products, adult
  content miscategorization — these need reading comprehension, not a regex.

## Output: Feed Audit Report

Use this structure. Fill the numbers from the script's `summary` block and the
rewrites from your own work.

```markdown
## Shopping Feed Audit Report

**Products Analyzed**: [count]   **Health Score**: [X/100]

### Critical Issues (fix immediately — these block products)
| Product ID | Issue | Current | Recommended |
|------------|-------|---------|-------------|
| [id] | [issue] | "[current]" | "[fix]" |

**Disapproval risk**: [X] products

### High Priority (significant visibility impact)
| Product ID | Issue | Impact |
|------------|-------|--------|

### Title Rewrites (the high-value fixes)
Product [id]:
- Before: "[current]"
- After: "[optimized]"
- Why: [what improved and the expected gain]

### Patterns & Quick Wins
1. [Batch fix that improves many products at once]
2. [Template change for consistency]

### Summary Statistics
| Metric | Count | % of Feed |
|--------|-------|-----------|
| Missing brand in title | X | X% |
| Promo text in title | X | X% |
| Titles over 150 chars | X | X% |
| Missing required attributes | X | X% |
```

## Clarifying questions (only when they change the audit)

- What categories are in this feed? (drives required-attribute checks)
- Selling internationally? (language/currency adds title and locale concerns)
- Any products you already know are disapproved? (start there)

Don't interrogate — if you have the feed, run the audit first and ask only what
genuinely changes the recommendations.
