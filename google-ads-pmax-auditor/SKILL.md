---
name: google-ads-pmax-auditor
description: >-
  Audit a Google Ads Performance Max campaign — grade asset coverage and quality,
  surface Google's LOW-rated assets to replace, check character limits, find
  duplicate copy, verify image sizes and aspect ratios, and review audience
  signals and conversion tracking. Use this whenever someone wants a PMax campaign
  reviewed or graded, AND when they describe a PMax symptom without naming it:
  "my Performance Max isn't performing", "which assets should I replace", "is my
  PMax set up right", "PMax asset strength is low", "grade my asset groups", "I
  launched PMax and it's burning budget". Covers both a pre-launch asset review
  and a live campaign audit.
---

# Performance Max Auditor

Grade a PMax campaign on the things that actually move it: which assets Google
rates LOW and should be swapped, where coverage is thin, which copy is duplicated
or over the limit, whether images meet spec, and whether the signals and tracking
are feeding the algorithm properly.

The countable work runs in a script so nothing is missed across asset groups and
the grade is repeatable. Your job is the judgment: rewriting weak assets toward
new angles, assessing image *visual* quality, and reading whether the signals fit.

## Two modes

- **Pre-launch review** — no performance data yet (labels are all PENDING). Audit
  *coverage and quality*: counts, character limits, duplicates, image specs,
  signal strength, tracking.
- **Live audit** — the campaign has run. Adds Google's **performance labels** and
  search-theme data, which is where the real optimization leverage is. Push to
  audit live campaigns when you can — a pre-launch audit can't tell you what's
  actually working.

## How the data arrives

PMax data comes through the **Google Ads API / GAQL**, the same as the account
audit, with *fetching* (credential-specific) separated from *analysis* (pure):

1. Run the queries in `references/gaql-queries.md` for the campaign.
2. Assemble the rows into one `pmax.json` (format in that file).
3. Analyze:
   ```bash
   python3 scripts/analyze_pmax.py pmax.json --out <dir>
   ```
   (Use `python` if that's Python 3 on the system.) It fetches each image asset to
   verify it resolves and read real dimensions, prints a graded summary + ranked
   findings, and writes `pmax.audit.json` with full detail. Add `--no-fetch` to
   skip downloads and use the GAQL-provided dimensions only (offline, or when the
   image URLs aren't reachable).

If you only have screen access and can't run GAQL, you can audit by hand against
`references/asset-guidance.md`, but you lose the performance labels and the
mechanical checks — so get the query data when you can.

## What the script decides (don't redo by hand)

Read `pmax.audit.json` and build the report on it. The script computes: the
LOW/GOOD/BEST label breakdown and the full **LOW-asset replacement list** (the
backbone), asset counts vs. targets per group, character-limit violations
(30/90/90), exact and near-duplicate copy, ad strength, image resolution and
aspect-ratio problems, missing image formats, search-theme coverage, URL
expansion, and conversion-tracking gaps. Each finding carries a severity and the
reason it matters.

## What you decide (judgment layer)

`references/asset-guidance.md` covers this in depth — pull it in when writing
recommendations:

- **For each LOW asset, why it's weak and what replaces it** — toward a new angle,
  not a synonym swap. Don't mass-delete to the minimum; that starves PMax of
  combinations.
- **Image visual quality** — the script confirms size/ratio/that it resolves, but
  can't see whether the picture is on-brand, clear, and varied.
- **Whether signals fit** the asset group's products, and whether a real video
  exists (or Google is auto-generating a weak one).

## Prioritize

Lead with the two highest-leverage things: **the LOW-asset replacements** (Google
is telling you exactly what's dragging the campaign) and **conversion tracking**
(PMax leans heavily on the conversion signal and its value — if that's wrong,
everything downstream is). Coverage gaps and character-limit fixes are quick wins.
Visual/signal refinement comes after.

## A note on dated advice

PMax now supports **negative keywords and brand exclusions** (account-level
self-serve; campaign-level available) — if brand or junk terms leak spend, the fix
is to *add* them, not to accept it as a limitation. And Google does **not** require
Title Case in headlines; judge clarity, not casing.

## Output: Audit Report

```markdown
## Performance Max Audit — [campaign] — [date]
**Grade**: [A–F]  ([score]/100, from the script)
**Asset labels**: [BEST/GOOD/LOW breakdown]

### Replace First — LOW-rated assets
| Asset Group | Slot | Current asset | Why / replacement angle |
|-------------|------|---------------|--------------------------|

### Critical (won't serve / below minimum)
| Asset Group | Issue | Fix |
|-------------|-------|-----|

### Coverage & Quality
- [Counts vs. target, duplicates, char limits, image specs — from the script]

### Signals & Tracking
- [Search-theme coverage, conversion tracking/value, URL expansion]

### Roadmap
**This week**: [replace LOW assets, fix char limits/coverage]
**Next**: [add variety/angles, video, refine signals]
```

## Clarifying questions (only what changes the audit)

- Is this pre-launch or a running campaign? (decides whether labels apply)
- Primary goal and is conversion value tracked? (turns the tracking check into a verdict)
- Retail/Shopping PMax or feed-less? (affects what coverage is expected)
