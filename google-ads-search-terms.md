---
name: google-ads-search-terms
description: Analyze Google Ads search terms reports to identify winners and losers. Use when reviewing campaign performance, finding new keyword opportunities, or optimizing existing campaigns.
---

# Google Ads Search Terms Analyzer

Surface the winners and losers in your search terms report to optimize performance.

## When to Use

- Regular campaign optimization reviews
- Identifying new keyword opportunities
- Finding negative keyword candidates
- Understanding user intent patterns
- Improving Quality Scores

## Input Requirements

Provide your Search Terms Report with:
- Search term
- Match type
- Clicks
- Impressions
- CTR
- Cost
- Conversions
- Conversion value (if available)
- Campaign/Ad Group (optional)

**Export from Google Ads**: Reports > Predefined Reports > Search Terms

## Analysis Framework

### Tier 1: Winners (Scale These)

**Criteria for Winners**:
- Conversions > 0 AND CPA below target
- OR Conversion rate > campaign average
- OR ROAS above target (if tracking value)

**Actions for Winners**:
1. Add as exact match keyword (if not already)
2. Increase bids if not hitting position 1
3. Create dedicated ad group with specific ads
4. Build similar keyword variations

### Tier 2: Potential (Test These)

**Criteria for Potential**:
- High impressions, decent CTR, no conversions yet
- OR Low CPA but low volume
- OR High CTR but limited data

**Actions for Potential**:
1. Add as phrase/broad match modified
2. Monitor for 2-4 weeks with set budget
3. Create specific ads to improve relevance

### Tier 3: Losers (Block These)

**Criteria for Losers**:
- Cost > 2x target CPA with no conversions
- OR Clicks > 50 with no conversions
- OR Low CTR (<1%) indicating poor relevance

**Actions for Losers**:
1. Add as negative keyword
2. Determine match type needed (exact vs phrase vs broad)
3. Apply at appropriate level (ad group, campaign, account)

### Tier 4: Investigate (Need More Data)

**Criteria**:
- Low impressions/clicks (insufficient data)
- OR Mixed signals (good CTR, bad conversion rate)

**Actions**:
1. Wait for more data before deciding
2. Check landing page relevance
3. Review ad copy match

## Output: Search Terms Analysis Report

```markdown
## Search Terms Analysis

**Report Period**: [dates]
**Total Terms Analyzed**: [count]
**Total Spend Analyzed**: $[amount]

---

### Winners (Add/Scale) - [count] terms

| Search Term | Clicks | Cost | Conv | CPA | Action |
|-------------|--------|------|------|-----|--------|
| [term] | X | $X | X | $X | Add [exact] |
| [term] | X | $X | X | $X | Increase bid |
| ... | | | | | |

**Revenue Opportunity**: $[estimated value if scaled]

---

### Potential (Test) - [count] terms

| Search Term | Clicks | Cost | CTR | Why Test |
|-------------|--------|------|-----|----------|
| [term] | X | $X | X% | High intent |
| [term] | X | $X | X% | Low CPA potential |
| ... | | | | |

**Test Budget Needed**: $[amount] over [period]

---

### Losers (Block) - [count] terms

| Search Term | Clicks | Cost | Conv | Waste | Block As |
|-------------|--------|------|------|-------|----------|
| [term] | X | $X | 0 | $X | [broad/phrase/exact] |
| [term] | X | $X | 0 | $X | [broad/phrase/exact] |
| ... | | | | | |

**Potential Monthly Savings**: $[amount]

---

### Investigate (Watch) - [count] terms

| Search Term | Issue | Recommendation |
|-------------|-------|----------------|
| [term] | Low data | Wait [X] weeks |
| [term] | High CTR, no conv | Check landing page |

---

### Patterns Discovered

**Winning Themes**:
- [pattern] appears in X winning terms
- [modifier] increases conversion rate by X%

**Losing Patterns**:
- [word/phrase] = waste indicator
- [intent pattern] doesn't convert

**Recommendations**:
1. [Specific strategic recommendation]
2. [Keyword structure suggestion]
3. [Targeting adjustment]
```

## Analysis Techniques

### Intent Categorization

**Commercial Intent** (likely to convert):
- "buy", "price", "cost", "near me"
- Brand + product terms
- Specific model/SKU searches

**Informational Intent** (educate or block):
- "what is", "how to", "vs", "review"
- Definition searches
- Comparison searches

**Navigational Intent** (competitor or branded):
- Competitor names
- Your brand + specific page

### Pattern Recognition

Look for commonalities:
- **Modifiers**: Words that appear in winning/losing terms
- **Length**: Do longer or shorter queries convert better?
- **Question vs statement**: Different intent signals
- **Location terms**: Geographic patterns
- **Time indicators**: Urgency signals

### Statistical Significance

Before declaring a winner or loser, ensure:
- Minimum 20-30 clicks for directional data
- Minimum 50+ clicks for confident decisions
- At least 5-10 conversions to judge CPA

**Quick significance formula**:
```
If clicks > (10 / expected conversion rate), data is meaningful
Example: 5% conv rate = need 200 clicks minimum
```

## Common Insights to Look For

### Red Flags
- Brand terms in non-brand campaigns (cannibalization)
- Competitor terms with high cost, low conversion
- "Free", "jobs", "DIY" terms eating budget
- Very long queries with 0 conversions (too specific)

### Green Flags
- High-converting long-tail terms (expand these)
- Location-specific terms outperforming (geo-target)
- Product-specific terms beating category terms
- Question queries that convert (content opportunity)

## Questions to Ask

1. What's your target CPA or ROAS?
2. What conversion actions are you tracking?
3. Are you running brand and non-brand separately?
4. What's your typical conversion cycle length?
5. Any known seasonal patterns?
