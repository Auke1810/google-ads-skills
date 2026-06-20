---
name: google-ads-search-terms
description: >-
  Analyze a Google Ads search terms report — sort every query into winners to
  scale, losers to block as negatives, terms to test, and terms that need more
  data, with a real wasted-spend figure and the word-patterns behind waste vs.
  wins. Use this whenever someone shares a search terms report or asks what their
  queries are doing: "which search terms are wasting my budget", "find negative
  keywords from my search terms", "which queries actually convert", "clean up my
  search terms", "analyze my search query report", "what should I add as exact
  match". This is first-party performance analytics on your own account data —
  for discovering net-new keywords from the market, that's a separate
  keyword-research job.
---

# Search Terms Analyzer

Sort a search terms report into four buckets — **Winners** (scale), **Losers**
(block), **Potential** (test), **Investigate** (wait) — and surface the word
patterns that separate waste from wins, so the negatives and expansions almost
write themselves.

The classification is pure first-party math: numeric thresholds against the
report, plus a statistical-significance gate so nothing gets condemned on three
clicks. That runs in a script, deterministically, across the whole report. Your
job is reading intent and turning the output into negative lists, structure
changes, and expansion seeds.

## Run it

The script takes **either** a GAQL `search_term_view` export **or** a Search
Terms CSV straight from the Google Ads UI — it auto-detects. See
`references/gaql-queries.md` for both.

```bash
python3 scripts/classify_terms.py <report.json|report.csv> --target-cpa 25 [--target-roas 4]
```

(Use `python` if that's Python 3 on the system.) It prints a tiered summary and
writes `<name>.tiers.json` with the full classification, per-term reasons and
actions, and the n-gram patterns. Targets are optional — without them it
benchmarks against the report's own blended CPA and conversion rate, so it still
works on raw data.

## What the script decides (don't redo by hand)

Read the JSON and build the report on it. The script computes, per term: CPA,
ROAS, conversion rate, the tier, *why* it landed there, and the recommended
action (including the suggested negative match type for losers). It also computes
the **wasted spend** (losers) and **scale opportunity** (winners) figures, and the
**n-gram patterns** — the tokens over-represented in waste vs. wins, plus
**loser-only tokens** (words that cost money but never appear in a winner), which
are your strongest negative-list candidates.

## What you decide (judgment layer)

`references/intent-and-patterns.md` covers this — pull it in when writing
recommendations:

- **Read the intent**, not just the numbers. A converting commercial term that's
  inefficient needs a landing-page or bid fix, not a block. An informational term
  ("how to", "review", "pdf") usually blocks well.
- **Turn loser-only tokens into shared negative lists** at campaign/account level
  so the fix scales beyond the specific terms in this report.
- **Catch structural leaks** the numbers hint at: brand terms in non-brand
  campaigns (cannibalization), competitor terms that don't pay off.

## Prioritize

Lead with the two things that move money now: the **losers** (immediate
wasted-spend savings — group them into negatives) and the **winners** (proven
demand to scale to exact match and higher bids). Potential and Investigate are
follow-ups, not the headline.

## Scope: analytics, not discovery

This skill works your **own account's** queries — what already spent your budget.
Finding *new* keywords that exist in the market (with search volume and CPC) is a
different, forward-looking job and belongs in a keyword-research/discovery skill.
The clean handoff: this skill's Winners become the seed list for that one.

## Output: Search Terms Analysis

```markdown
## Search Terms Analysis — [date range]
**Terms**: [n]   **Spend analyzed**: [currency] [x]   **Benchmark**: target CPA [x]

### Losers — Block ([n], [currency] [waste] wasted)
| Search Term | Clicks | Cost | Conv | Block as |
|-------------|--------|------|------|----------|

### Winners — Scale ([n], [conv] conversions)
| Search Term | Clicks | Cost | Conv | CPA | Action |
|-------------|--------|------|------|-----|--------|

### Potential — Test  ·  ### Investigate — Wait
[shorter lists]

### Patterns
- **Loser-only words** (→ negative lists): [from the script]
- **Winning words** (→ expansion seeds): [from the script]

### Recommendations
1. [Negative lists to create]  2. [Terms to add as exact]  3. [Structure fix]
```

## Clarifying questions (only what changes the analysis)

- Target CPA / ROAS? (turns "good vs. average" into "good vs. your goal")
- Brand and non-brand running separately? (frames cannibalization findings)
- Tracking conversion *value*? (decides whether ROAS can be judged at all)
