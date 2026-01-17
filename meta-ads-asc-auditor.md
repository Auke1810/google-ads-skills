---
name: meta-ads-asc-auditor
description: Audit Meta Advantage+ Shopping Campaigns for setup mistakes and optimization opportunities. Use when troubleshooting ASC performance, reviewing campaign structure, or setting up new Advantage+ campaigns.
---

# Meta Advantage+ Shopping Campaign Auditor

Catch setup mistakes in your Advantage+ Shopping Campaigns before they cost you money.

## When to Use

- Setting up new Advantage+ Shopping Campaigns
- Troubleshooting underperforming ASC campaigns
- Reviewing existing campaign structure
- Deciding between ASC and manual campaigns
- Optimizing ASC performance

## Input Requirements

Provide:
1. **Campaign Settings**: Budget, bid strategy, optimization goal
2. **Creative Assets**: Number and types of creatives
3. **Audience Settings**: Existing customer definitions, exclusions
4. **Catalog Setup**: Product sets, catalog structure
5. **Performance Data**: ROAS, CPA, spend (if campaign is running)
6. **Business Context**: Industry, average order value, customer lifetime value

## ASC Setup Checklist

### 1. Campaign Foundation

**Required Settings**:
- [ ] Conversion event properly configured
- [ ] Pixel firing on all key events (ViewContent, AddToCart, Purchase)
- [ ] Conversion API (CAPI) connected for redundancy
- [ ] Attribution window appropriate for your sales cycle

**Budget Check**:
- [ ] Daily budget ≥ $50 (minimum for learning)
- [ ] Recommended: Daily budget ≥ 10x target CPA
- [ ] Budget not capped artificially low

### 2. Audience Setup

**Existing Customer Definition**:
- [ ] Customer list uploaded (emails/phones)
- [ ] Website purchasers audience created
- [ ] 180-day lookback window (maximum)

**Existing Customer Budget Cap**:
- [ ] Cap set appropriately (usually 0-30%)
- [ ] Not leaving money on table by capping too low
- [ ] Not wasting budget on existing customers

**Common Mistake**: Setting 0% existing customer cap when you have good repeat purchase rate

### 3. Creative Setup

**Minimum Requirements**:
- [ ] At least 5-10 unique creative concepts
- [ ] Mix of formats (static, video, carousel)
- [ ] Varied aspect ratios (1:1, 4:5, 9:16)

**Best Practices**:
- [ ] 10-20 total creative assets
- [ ] 2-3 completely different concepts/angles
- [ ] Including UGC-style creative
- [ ] Product-focused and lifestyle shots

**Red Flags**:
- [ ] All creatives look the same
- [ ] Only one format type
- [ ] Creatives older than 4-6 weeks (fatigue risk)

### 4. Product Catalog

**Structure**:
- [ ] All products included (unless intentional exclusion)
- [ ] Product sets created for different categories
- [ ] Pricing accurate and updated
- [ ] Inventory status accurate

**Product Feed Quality**:
- [ ] Titles descriptive and keyword-rich
- [ ] Images high quality, white background
- [ ] Descriptions complete
- [ ] All required fields populated

### 5. Account-Level Settings

**Attribution**:
- [ ] 7-day click (standard for most)
- [ ] View-through attribution considerations understood
- [ ] Same attribution across campaigns for fair comparison

**Placement Expansion**:
- [ ] Advantage+ placements ON (required for ASC)
- [ ] Not fighting the algorithm with placement restrictions

## Common ASC Mistakes

### Mistake 1: Budget Too Low
**Issue**: Daily budget under $50 or less than 5x CPA
**Impact**: Campaign never exits learning, performance volatile
**Fix**: Increase to minimum $50/day or 10x target CPA

### Mistake 2: Wrong Existing Customer Definition
**Issue**: Only including email list, missing website purchasers
**Impact**: Treating repeat customers as new, skewing data
**Fix**: Create comprehensive existing customer audience

### Mistake 3: Existing Customer Cap at 0%
**Issue**: Forcing 0% cap when repeat purchases are valuable
**Impact**: Missing out on high-ROAS repeat purchase revenue
**Fix**: Start at 15-20%, adjust based on business model

### Mistake 4: Existing Customer Cap Too High
**Issue**: 50%+ budget going to existing customers
**Impact**: Not enough new customer acquisition
**Fix**: Lower cap to 20-30% unless repeat purchase is primary goal

### Mistake 5: Creative Fatigue
**Issue**: Same creatives running for months
**Impact**: Declining performance, frequency too high
**Fix**: Refresh creative every 4-6 weeks, add variety

### Mistake 6: Single Creative Concept
**Issue**: All ads are variations of same concept
**Impact**: Not testing what actually resonates
**Fix**: Test 3-4 completely different angles

### Mistake 7: Fighting the Algorithm
**Issue**: Excessive exclusions, narrow constraints
**Impact**: Algorithm can't optimize, worse performance
**Fix**: Trust Advantage+ automation, give it room

### Mistake 8: Wrong Optimization Event
**Issue**: Optimizing for AddToCart instead of Purchase
**Impact**: Lots of carts, few sales
**Fix**: Optimize for final conversion event

### Mistake 9: Attribution Mismatch
**Issue**: Different attribution windows across campaigns
**Impact**: Can't compare performance fairly
**Fix**: Standardize attribution settings

### Mistake 10: Ignoring Learning Phase
**Issue**: Making changes before 50 conversions
**Impact**: Resetting learning, poor optimization
**Fix**: Wait for learning to complete before adjusting

## Output: ASC Audit Report

```markdown
## Advantage+ Shopping Campaign Audit

**Campaign**: [name]
**Audit Date**: [date]
**Overall Health**: [Good/Needs Work/Critical Issues]

---

### Critical Issues (Fix Now)

| Issue | Current | Recommended | Impact |
|-------|---------|-------------|--------|
| [issue] | [value] | [target] | [why it matters] |

---

### Setup Score by Category

| Category | Score | Status |
|----------|-------|--------|
| Campaign Foundation | X/10 | [emoji] |
| Audience Setup | X/10 | [emoji] |
| Creative Assets | X/10 | [emoji] |
| Product Catalog | X/10 | [emoji] |

---

### Detailed Findings

**Campaign Foundation**
- [Finding with specific recommendation]
- [Finding with specific recommendation]

**Audience Setup**
- Existing customer definition: [status]
- Budget cap: [current]% → Recommend: [target]%
- Reasoning: [why this cap makes sense]

**Creative Assets**
- Total assets: [count]
- Format mix: [breakdown]
- Age of oldest creative: [days]
- Recommendation: [specific guidance]

**Product Catalog**
- Products in catalog: [count]
- Products active: [count]
- Issues found: [list]

---

### Performance Diagnosis (if data provided)

**Current Metrics**:
- ROAS: [X] (Target: [X])
- CPA: $[X] (Target: $[X])
- Frequency: [X]

**Likely Causes of Underperformance**:
1. [Diagnosis with evidence]
2. [Diagnosis with evidence]

---

### Action Plan

**Immediate (This Week)**:
1. [Highest priority fix]
2. [Second priority]

**Short-term (Next 2 Weeks)**:
1. [Optimization]
2. [Testing]

**Ongoing**:
1. [Maintenance task]
2. [Monitoring focus]

---

### ASC vs Manual Campaign Decision

Based on your situation:
- [Recommendation: Use ASC / Use Manual / Test Both]
- Reasoning: [why this approach for your business]
```

## When ASC Works Best

- Established pixel with good conversion data
- Broad audience targeting preferred
- Looking to scale acquisition
- Have sufficient creative variety
- Budget to support learning phase

## When Manual Might Be Better

- Very niche audience requirements
- Limited budget (under $50/day)
- Complex funnel needing specific event optimization
- Testing very specific hypotheses
- New pixel with limited data

## Questions to Ask

1. What's your target CPA or ROAS?
2. How important is new customer acquisition vs repeat purchases?
3. What's your customer lifetime value?
4. When did you last refresh creative?
5. Are you running other Meta campaigns alongside ASC?
