# Intent & Patterns (judgment layer)

`scripts/classify_terms.py` does the tiering and the n-gram math: it sorts every
term into Winners / Potential / Losers / Investigate, applies the significance
gate, computes the wasted-spend and scale figures, and surfaces the tokens
over-represented in waste vs. wins (including **loser-only tokens** — words that
cost money but never appear in a winning term, which are your strongest negative
candidates). **Read its JSON first.** This file is for turning that output into
decisions.

## How the tiers are decided (so you can explain and override)
- **Winner**: converts, and does it efficiently — CPA at/below target, ROAS
  at/above target, or a conversion rate above the account average.
- **Potential**: either converts but *inefficiently* (don't scale, optimize or
  bid down — never block a term that converts), or has real traffic but no
  conversions yet and not enough clicks to condemn it.
- **Loser**: zero conversions with enough clicks to trust the verdict, or spend
  already past 2× target CPA. Confident waste.
- **Investigate**: too little data to say anything — wait, don't act.

The significance threshold (clicks needed before a zero-conversion term is called
a loser) is derived from the account's blended conversion rate, so a 3-click term
is never blocked. If you disagree with a single classification, the per-term
`why` field tells you exactly which rule fired.

## Turning patterns into action
- **Loser-only tokens → shared negative lists.** If "free", "jobs", or "diy" cost
  money across several terms and never convert, add them as *phrase* negatives
  once at the campaign or account level — that scales the fix beyond the specific
  terms in this report.
- **Winning tokens → expansion seeds.** The words common to your winners are the
  intent worth doubling down on. (Finding *new* keywords from them is a discovery
  job, not this skill — hand the winners to a keyword-research step.)
- **Individual losers** that are specific phrases (not a junk token) → exact
  negatives, so you don't accidentally block a good variant.

## Intent categories (read the term, not just the numbers)
- **Commercial** ("buy", "price", "deal", model/SKU, brand+product): should
  convert; if it doesn't, suspect the landing page or bid, not the term.
- **Informational** ("what is", "how to", "review", "vs", "pdf", "meaning"):
  usually browse, not buy. Blocks well unless you have content that monetizes it.
- **Navigational** (competitor names, your brand): brand terms in a non-brand
  campaign are cannibalization — route them, don't just judge them. Competitor
  terms are often high-cost, low-conversion; keep only if the math works.

## Red flags worth a manual scan
- Brand terms surfacing in non-brand campaigns (cannibalization / structure leak).
- "Free / jobs / diy / used / salary" eating budget (the loser-only list catches
  most, but skim for new ones).
- Very long, hyper-specific queries with zero conversions — often too niche; cheap
  to leave but not worth chasing.

## Green flags worth expanding
- High-converting long-tail terms — the cheapest efficient volume you'll find.
- Location or product-specific terms beating generic category terms — a signal to
  restructure toward the specific.
- Question queries that *do* convert — a content + campaign opportunity.

## Mind the data caveats
- A short window or a tiny account produces a high significance threshold (lots of
  Investigate). Say so rather than forcing terms into Winner/Loser on thin data.
- Without conversion *value*, ROAS can't be judged — tier on CPA and conversion
  rate, and flag that value tracking is missing (it limits value-based bidding).
