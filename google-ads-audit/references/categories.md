# Category Deep-Dives (judgment layer)

`scripts/analyze_account.py` already covers the mechanical, countable checks:
wasted spend, Quality Score, duplicate keywords, budget-limited campaigns, ad
strength, RSA coverage, content-network leakage, smart-bidding data sufficiency,
and conversion-tracking config. **Read its JSON output first.** This file covers
the judgment calls the script can't make — the parts that need you to look and
think. Pull in only the categories relevant to what the data flagged.

A note on priority: don't treat the ten areas as equal. **Conversion tracking
and wasted spend move the most money and come first.** Settings and structure
come next because they shape everything downstream. Audience and competitive
work matter, but a beautifully segmented account with broken tracking is still
flying blind, so don't open the report with them.

## 1. Conversion tracking (audit first — it poisons everything)
Everything smart bidding does depends on this being right. If it's wrong, every
other recommendation is built on sand.
- Are the *right* actions counted, and counted once? Duplicate tags inflate
  conversions and make CPA look better than it is.
- Is a meaningful value attached? Without it, tROAS and value rules can't run.
- Does the conversion window match the real sales cycle? A 7-day window on a
  product with a 3-week consideration cycle undercounts and starves bidding.
- Enhanced conversions enabled? It recovers attribution lost to cookie decay.

## 2. Wasted spend
The script gives you the figure and the negative-keyword candidates. Your job:
- Decide which zero-conversion search terms are genuinely irrelevant (→ negatives)
  vs. relevant-but-not-yet-converting (→ keep, maybe rework the landing page).
- Group negatives into shared lists by theme so the fix scales beyond this audit.
- For zero-conversion keywords with real spend, decide pause vs. rework vs.
  match-type change — don't blanket-pause terms that just need a better ad.

## 3. Account structure
- Are campaigns separated by intent and economics — brand vs. non-brand, Search
  vs. Shopping vs. Display vs. Video? Mixing them makes budget and bidding lie.
- Brand and non-brand must be split: they have wildly different CPCs and intent,
  and merging them lets cheap brand traffic mask expensive non-brand waste.
- Modern structure favors **tightly themed ad groups with responsive ads and
  smart bidding**, not one-keyword-per-group micro-segmentation. Single-keyword
  ad groups (the old "SKAG" tactic) now fight close-variant matching and starve
  smart bidding of data — don't recommend them by default.

## 4. Campaign settings
- Search Partners and the Display/Content network on Search campaigns: evaluate
  with the data, don't assume. Usually off for pure Search intent, but check
  whether they actually convert before cutting.
- Location targeting: "Presence" vs. "Presence or interest" — the latter silently
  serves to people merely *searching about* your area. Match it to the goal.
- Ad schedule: only layer one once you have performance by hour/day. Imposing a
  schedule on thin data just removes auctions you might have won.

## 5. Keywords & match types
- With smart bidding, broad match can work — but only with solid conversion data
  and tight negatives guarding it. Broad + manual bidding + weak negatives is how
  budgets evaporate.
- Reserve exact match for proven, high-intent terms. Use the search-terms report
  as the source of truth for what people actually typed.

## 6. Ad copy & assets
- Ad strength is a guide, not a goal — "Excellent" with generic copy beats nothing,
  but don't chase the label at the cost of message relevance.
- Every ad group should have something to test against. Vary the *angle*
  (benefit, offer, objection), not just the wording.
- Do ads, keywords, and landing page tell one consistent story? Message-match
  between ad and page is where a lot of Quality Score and conversion rate is won.

## 7. Audiences
- Remarketing lists built and large enough to use (RLSA bid adjustments or
  dedicated campaigns)?
- Customer Match uploaded where you have first-party data — it's increasingly the
  durable signal as third-party cookies fade.
- Exclude existing converters from prospecting campaigns so you don't pay to
  re-acquire people you already have.

## 8. Landing pages
- Specific pages for specific ad groups, not everything dumped on the homepage.
- Speed (sub-3s), mobile layout, a clear above-the-fold CTA, and trust signals.
  A great account pointing at a weak page converts poorly no matter the bidding.

## 9. Budget & bidding
- Is budget weighted toward proven performers, and are winners ever capped by
  budget (the script flags impression share lost to budget)?
- Does the bid strategy match the goal and the data volume? Target CPA/ROAS need
  enough conversions (~30+/month per campaign) to be stable.
- Are the targets realistic against account history, or aspirational numbers the
  algorithm can't hit without choking volume?

## 10. Competitive position (auction insights)
- Impression share, overlap rate, position-above rate on your key terms.
- Is lost impression share due to budget (fixable with money) or rank (fixable
  with bids/Quality Score)? The script reports both; this is where you interpret
  which lever to pull.
- Is the ad copy actually differentiated, or are you bidding to look identical to
  three competitors?
