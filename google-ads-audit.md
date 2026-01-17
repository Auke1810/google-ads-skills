---
name: google-ads-audit
description: Perform comprehensive Google Ads account audits to identify wasted spend, structure issues, and optimization opportunities. Use when reviewing account health, onboarding new clients, or troubleshooting poor performance.
---

# Google Ads Account Audit

Complete account health audit to catch wasted spend, structural issues, and missed opportunities.

## When to Use

- Onboarding a new client or inheriting an account
- Quarterly or monthly account health checks
- Troubleshooting declining performance
- Before scaling ad spend
- Preparing optimization roadmap

## Input Requirements

Provide access or exports of:
1. **Account Structure**: Campaigns, ad groups, keywords
2. **Performance Data**: Last 30/60/90 days metrics
3. **Settings**: Bidding, targeting, schedules
4. **Conversion Tracking**: Goals and values
5. **Business Context**: Goals, target CPA/ROAS, margins

## Audit Framework (10 Categories)

### 1. Account Structure Audit

**Campaign Organization**:
- [ ] Campaigns organized by goal (Brand, Non-Brand, Shopping, etc.)
- [ ] Clear naming conventions used
- [ ] No conflicting campaigns targeting same keywords
- [ ] Separate campaigns for Search, Display, Video, Shopping

**Ad Group Structure**:
- [ ] Ad groups tightly themed (10-20 keywords max)
- [ ] SKAGs used where appropriate (branded, high-value)
- [ ] No "catch-all" ad groups with 100+ keywords

**Red Flags**:
- Single campaign with all keywords
- Ad groups with 50+ keywords
- Mixing match types in same ad group poorly

### 2. Campaign Settings Audit

**Networks**:
- [ ] Search Partners evaluated (usually turn OFF)
- [ ] Display Network OFF for Search campaigns
- [ ] Proper network for each campaign type

**Locations**:
- [ ] Targeting correct geographic areas
- [ ] "Presence" vs "Presence or Interest" set correctly
- [ ] Location exclusions where needed

**Languages**:
- [ ] Appropriate languages selected
- [ ] Not over-restricting unintentionally

**Bid Strategy**:
- [ ] Strategy matches campaign goals
- [ ] Sufficient conversion data for smart bidding (50+ conv/month)
- [ ] Target CPA/ROAS realistic based on history

**Budget**:
- [ ] Daily budgets appropriate for goals
- [ ] Not "limited by budget" on profitable campaigns
- [ ] Shared budgets used appropriately

**Ad Schedule**:
- [ ] Schedule based on performance data
- [ ] High-performing hours/days prioritized
- [ ] Not running 24/7 without analysis

### 3. Keyword Audit

**Match Types**:
- [ ] Appropriate mix of match types
- [ ] Broad match used with smart bidding only
- [ ] Exact match for high-intent, proven terms

**Keyword Quality**:
- [ ] Quality Scores reviewed (aim for 7+)
- [ ] Low QS keywords addressed or paused
- [ ] Relevance between keywords and ad groups

**Negative Keywords**:
- [ ] Negative keyword lists exist
- [ ] Search terms report reviewed regularly
- [ ] Cross-campaign negatives prevent cannibalization

**Keyword Performance**:
- [ ] Underperforming keywords paused
- [ ] High-cost, no-conversion keywords addressed
- [ ] Winning keywords expanded

### 4. Ad Copy Audit

**RSA Best Practices**:
- [ ] 15 headlines used (maximum)
- [ ] 4 descriptions used (maximum)
- [ ] Variety in messaging angles
- [ ] Keywords included naturally
- [ ] Clear CTAs present

**Ad Strength**:
- [ ] "Good" or "Excellent" ad strength
- [ ] Multiple RSAs per ad group for testing
- [ ] Poor-performing ads paused

**Ad Relevance**:
- [ ] Ads match keyword intent
- [ ] Landing pages match ad promises
- [ ] Extensions complement ads

### 5. Extensions Audit

**Required Extensions**:
- [ ] Sitelinks (4+ active)
- [ ] Callouts (4+ active)
- [ ] Structured snippets (2+ active)

**Recommended Extensions**:
- [ ] Call extensions (if phone leads valuable)
- [ ] Location extensions (if local business)
- [ ] Price extensions (if applicable)
- [ ] Image extensions (where available)

**Extension Quality**:
- [ ] Extensions relevant and updated
- [ ] No outdated promotions
- [ ] Mobile-specific extensions where needed

### 6. Conversion Tracking Audit

**Tracking Setup**:
- [ ] Google Ads conversion tracking OR imported GA4 goals
- [ ] All valuable actions tracked
- [ ] Conversion values assigned accurately
- [ ] Enhanced conversions enabled

**Conversion Settings**:
- [ ] Attribution model appropriate (data-driven preferred)
- [ ] Conversion window matches sales cycle
- [ ] View-through conversions evaluated

**Data Quality**:
- [ ] Conversions firing correctly (test regularly)
- [ ] No duplicate conversions
- [ ] Primary vs secondary actions distinguished

### 7. Audience Audit

**Remarketing**:
- [ ] Remarketing lists created and populated
- [ ] RLSA campaigns or bid adjustments active
- [ ] Customer lists uploaded (Customer Match)

**Audience Targeting**:
- [ ] In-market audiences tested
- [ ] Affinity audiences tested (awareness)
- [ ] Similar audiences used where available

**Audience Exclusions**:
- [ ] Converters excluded from acquisition campaigns
- [ ] Irrelevant audiences excluded

### 8. Landing Page Audit

**Relevance**:
- [ ] Landing pages match ad intent
- [ ] Specific pages for specific ad groups (not all to homepage)
- [ ] Message match between ad and page

**Quality**:
- [ ] Pages load quickly (under 3 seconds)
- [ ] Mobile-friendly design
- [ ] Clear CTAs above fold
- [ ] Trust signals present

### 9. Budget & Bidding Audit

**Budget Allocation**:
- [ ] Budget weighted toward best performers
- [ ] No profitable campaigns limited by budget
- [ ] Poor performers have reduced budget

**Bid Strategy Performance**:
- [ ] Smart bidding has sufficient data
- [ ] Target CPA/ROAS being achieved
- [ ] Manual bids optimized if used

**Wasted Spend**:
- [ ] Search terms report reviewed
- [ ] Negative keywords blocking waste
- [ ] Display placements reviewed (if applicable)

### 10. Competitive Analysis

**Auction Insights**:
- [ ] Impression share reviewed
- [ ] Overlap rate with competitors understood
- [ ] Position above rate analyzed

**Competitive Position**:
- [ ] Bidding competitive on key terms
- [ ] Ad copy differentiated from competitors
- [ ] Unique value propositions highlighted

## Output: Audit Report

```markdown
## Google Ads Account Audit Report

**Account**: [name]
**Audit Period**: [date range]
**Auditor**: [name]
**Date**: [date]

---

### Executive Summary

**Overall Account Health**: [Score /100]

| Category | Score | Priority |
|----------|-------|----------|
| Account Structure | X/10 | [High/Med/Low] |
| Campaign Settings | X/10 | [High/Med/Low] |
| Keywords | X/10 | [High/Med/Low] |
| Ad Copy | X/10 | [High/Med/Low] |
| Extensions | X/10 | [High/Med/Low] |
| Conversion Tracking | X/10 | [High/Med/Low] |
| Audiences | X/10 | [High/Med/Low] |
| Landing Pages | X/10 | [High/Med/Low] |
| Budget & Bidding | X/10 | [High/Med/Low] |
| Competitive Position | X/10 | [High/Med/Low] |

**Estimated Monthly Waste**: $[amount]
**Estimated Improvement Potential**: [X]% increase in conversions

---

### Critical Issues (Fix Immediately)

| Issue | Impact | Fix |
|-------|--------|-----|
| [Issue] | $[waste]/month | [Specific action] |
| [Issue] | [Impact] | [Specific action] |

---

### High Priority Recommendations

1. **[Recommendation]**
   - Current: [state]
   - Recommended: [change]
   - Expected Impact: [outcome]

2. **[Recommendation]**
   - Current: [state]
   - Recommended: [change]
   - Expected Impact: [outcome]

---

### Category Deep Dives

#### Account Structure
[Detailed findings and recommendations]

#### Campaign Settings
[Detailed findings and recommendations]

#### Keywords
[Detailed findings with specific keyword examples]

#### Ad Copy
[Detailed findings with specific ad examples]

#### Extensions
[Detailed findings]

#### Conversion Tracking
[Detailed findings - critical for accuracy]

#### Audiences
[Detailed findings and opportunities]

#### Landing Pages
[Detailed findings with specific page issues]

#### Budget & Bidding
[Detailed findings with specific numbers]

#### Competitive Position
[Detailed findings from auction insights]

---

### Quick Wins (Implement This Week)

1. [Quick fix with immediate impact]
2. [Quick fix with immediate impact]
3. [Quick fix with immediate impact]

### 30-Day Optimization Plan

**Week 1**: [Focus area]
**Week 2**: [Focus area]
**Week 3**: [Focus area]
**Week 4**: [Focus area]

### 90-Day Strategic Recommendations

1. [Longer-term improvement]
2. [Longer-term improvement]
3. [Longer-term improvement]

---

### Appendix

- Wasted spend keywords list
- Recommended negative keywords
- Ad copy suggestions
- Extension recommendations
```

## Common Issues Found in Audits

### Structure Issues
- All keywords in one campaign
- No separation of brand vs non-brand
- Display mixed with Search

### Settings Issues
- Search Partners ON wasting budget
- Wrong location targeting setting
- No ad schedule despite clear patterns

### Keyword Issues
- Broad match without smart bidding
- No negative keywords
- Duplicate keywords across campaigns

### Tracking Issues
- Missing conversion tracking
- Duplicate conversions inflating data
- Wrong attribution model

## Questions to Ask Before Audit

1. What are your primary business goals?
2. What's your target CPA or ROAS?
3. What's your monthly budget?
4. Who are your main competitors?
5. Any recent changes to the account?
6. What's worked well historically?
