---
name: google-ads-negative-keywords
description: Analyze Google Ads search terms reports to find wasted spend and generate negative keyword block lists. Use when reviewing search term reports, identifying irrelevant queries, or optimizing ad spend efficiency.
---

# Google Ads Negative Keywords Analyzer

Find wasted spend in your Google Ads campaigns and generate actionable negative keyword lists.

## When to Use

- Reviewing search terms reports from Google Ads
- Identifying irrelevant queries eating your budget
- Building negative keyword lists for campaigns
- Optimizing ROAS by eliminating wasteful clicks

## Input Requirements

Provide one of the following:
1. **Search Terms Report** (CSV or pasted data) with columns:
   - Search term
   - Clicks
   - Impressions
   - Cost
   - Conversions (if available)
2. **Campaign context**: What you're selling, target audience, business goals

## Analysis Process

### Step 1: Identify Wasted Spend Categories

Look for these red flags:
- **Irrelevant intent**: Searches for free, DIY, jobs, reviews (when selling)
- **Wrong audience**: B2C terms when targeting B2B (or vice versa)
- **Competitor traffic**: Searches for competitor names (unless intentional)
- **Geographic mismatches**: Location terms outside service area
- **Product mismatches**: Wrong products, sizes, colors, models
- **Informational queries**: "What is", "How to" (unless content marketing)

### Step 2: Calculate Waste Metrics

For each suspicious term:
```
Waste Score = Cost × (1 - Conversion Rate) × Intent Mismatch Factor
```

Prioritize by:
1. High cost, zero conversions
2. High clicks, low conversion rate
3. High impressions, low CTR (indicates poor match)

### Step 3: Generate Negative Keyword List

Output format:
```
BROAD MATCH NEGATIVES:
- free
- cheap
- diy
- jobs
- salary

PHRASE MATCH NEGATIVES:
- "how to make"
- "what is a"
- "jobs near me"

EXACT MATCH NEGATIVES:
- [competitor name]
- [specific irrelevant product]
```

## Output Structure

### Summary Report

```markdown
## Negative Keywords Analysis

**Report Period**: [date range]
**Total Search Terms Analyzed**: [count]
**Estimated Wasted Spend**: $[amount] ([percentage]% of total)

### Top Waste Categories
1. [Category] - $[waste] - [example terms]
2. [Category] - $[waste] - [example terms]
3. [Category] - $[waste] - [example terms]

### Recommended Negative Keywords

#### Campaign-Level Negatives ([count] terms)
[list]

#### Ad Group-Level Negatives
- Ad Group: [name] - [negatives]
- Ad Group: [name] - [negatives]

### Quick Wins (Implement Immediately)
- Block "[term]" - Save ~$[amount]/month
- Block "[term]" - Save ~$[amount]/month
```

## Common Negative Keyword Categories

### Universal Negatives (Most Businesses)
- free, cheap, discount, coupon
- jobs, careers, salary, hiring
- diy, homemade, how to make
- reviews, complaints, scam
- wiki, definition, meaning

### B2B Specific
- personal, home, residential
- cheap, budget, free
- student, beginner

### B2C Specific
- wholesale, bulk, enterprise
- B2B, corporate, business

### Service Businesses
- diy, yourself, tutorial
- classes, courses, training (unless you offer these)

### E-commerce
- used, refurbished (unless you sell these)
- rental, rent, lease
- repair, fix, parts

## Implementation Tips

1. **Start with campaign-level negatives** for obvious mismatches
2. **Use ad group-level negatives** for nuanced exclusions
3. **Review weekly** during first month, then monthly
4. **Don't over-exclude** - some broad terms convert
5. **Check Search Terms regularly** after adding negatives

## Questions to Ask

Before generating the list, understand:
1. What products/services do you sell?
2. Who is your target customer (B2B/B2C, demographics)?
3. What's your geographic service area?
4. Are there any terms that seem irrelevant but actually convert?
5. Do you have existing negative keyword lists?
