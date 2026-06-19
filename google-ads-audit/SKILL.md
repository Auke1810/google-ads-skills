---
name: google-ads-audit
description: >-
  Run a comprehensive Google Ads account audit — quantify wasted spend, find
  structure and settings problems, check conversion tracking, and produce a
  prioritized optimization roadmap with a real euro/dollar waste figure. Use this
  whenever someone wants an account reviewed or is describing a Shopping/Search
  symptom even without saying "audit": "I inherited this Google Ads account",
  "where is my ad budget going", "my CPA keeps climbing", "Google Ads spends a
  lot but barely converts", "is my account set up right", "before we scale spend,
  check it", "second opinion on what my agency is doing". Reach for it for
  onboarding a new account, a monthly/quarterly health check, or troubleshooting
  a drop in performance.
---

# Google Ads Account Audit

Find the spend that's leaking and the setup that's holding the account back, then
hand the owner a prioritized fix list — led by a **real wasted-spend number**,
not a guess.

The objective, high-volume analysis runs in a script so the euro figures are
defensible and nothing gets missed across hundreds of keywords and thousands of
search terms. Your job is the interpretation, the judgment calls, and the
roadmap.

## How the data arrives

This account's data comes through the **Google Ads API / GAQL** (the official
client, the REST endpoint, or the Query Builder), not as ad-hoc exports. The
design deliberately separates *fetching* (credential-specific, brittle) from
*analyzing* (pure, testable):

1. Run the queries in `references/gaql-queries.md` for the audit window.
2. Assemble the result rows into one `account.json` (format and per-row shape are
   in that same file).
3. Analyze:
   ```bash
   python3 scripts/analyze_account.py account.json --out <dir>
   ```
   (Use `python` if that's what resolves to Python 3.) It prints a summary +ranked
   findings and writes `account.audit.json` with full detail and the
   negative-keyword candidate list. Every dataset is optional — it reports which
   checks ran — but lead with **search_terms, keywords, and conversion_actions**;
   those drive the highest-value findings.

If all you have is read-only screen access and can't run GAQL, you can still audit
by hand against `references/categories.md`, but you lose the quantified waste
figure — so get the query data when you can.

## What the script decides for you (don't redo by hand)

Read `account.audit.json` and build the report on top of it. The script computes:
wasted spend (the headline figure) and negative-keyword candidates, zero-conversion
keywords, low Quality Score keywords with spend, duplicate keywords across ad
groups, budget-limited campaigns, content-network leakage on Search, smart-bidding
data sufficiency, ad strength, single-ad ad groups, and conversion-tracking
health. Each finding carries a severity and the reason it matters.

## What you decide (the judgment layer)

The script counts; you interpret. `references/categories.md` covers all ten areas
in depth — pull in the ones the data flagged. The calls that need you:

- **Which zero-conversion search terms are truly irrelevant** (→ negatives) vs.
  relevant-but-not-yet-converting (→ keep, fix the page or ad).
- **Whether tracking is trustworthy** — duplicate tags, missing value, a window
  that doesn't match the sales cycle. If tracking is broken, say so loudly and
  caveat every bidding recommendation, because smart bidding is only as good as
  the signal feeding it.
- **Structure and bid-strategy fit** for the account's goals and data volume.

## Prioritize — don't treat the ten areas as equal

A report that opens with "Languages: 8/10" loses the reader. Lead with the two
things that move money: **conversion tracking** (it poisons every other decision
if wrong) and **wasted spend** (it's cash leaving the door now). Structure and
settings next. Audience and competitive position matter, but they come after the
account can see straight and isn't bleeding budget.

## A note on dated advice

Modern Google Ads rewards **tightly themed ad groups + responsive ads + smart
bidding**. Single-keyword ad groups (the old "SKAG" tactic) now fight
close-variant matching and starve smart bidding of data — don't recommend them by
default. Treat "turn Search Partners off" and similar absolutes as *evaluate with
the data*, not automatic.

## Output: Audit Report

```markdown
## Google Ads Account Audit — [account] — [date range]

### Executive Summary
**Health Score**: [score]/100  (from the script)
**Estimated Monthly Waste**: [currency] [amount]  ([X]% of spend)
**Top 3 priorities**: [one line each, money-first]

### Critical Issues (fix this week)
| Issue | Impact | Fix |
|-------|--------|-----|
| [issue] | [currency]/mo or "blind bidding" | [specific action] |

### High Priority
1. **[Recommendation]** — Current: [state] → Recommended: [change] → Expected: [outcome]

### Wasted Spend & Negative Keywords
- [Top zero-conversion search terms from the script, grouped into negative lists]

### Findings by Area (only what's flagged)
[Pull the relevant deep-dives from references/categories.md, tied to the data]

### Roadmap
**This week**: [quick wins] · **30 days**: [structural] · **90 days**: [strategic]
```

## Clarifying questions (only what changes the audit)

- Target CPA/ROAS and margins? (turns "waste" from a number into a verdict)
- Recent account changes? (explains a performance shift)
- What's historically worked? (don't recommend undoing a proven winner)

If you have the query data, run the analysis first and ask only what genuinely
changes the recommendations.
