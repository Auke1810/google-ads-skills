---
name: meta-ads-creative-analyzer
description: Score and analyze Meta ad creatives to explain what's working and what's not. Use when reviewing ad performance, understanding creative fatigue, or planning new creative concepts.
---

# Meta Ads Creative Analyzer

Score your Facebook and Instagram ads and understand exactly what's working (and what isn't).

## When to Use

- Reviewing performance of current ads
- Understanding why certain creatives outperform
- Diagnosing creative fatigue
- Planning new creative concepts
- A/B test analysis

## Input Requirements

Provide:
1. **Creative Assets**: Images/videos or descriptions
2. **Ad Copy**: Primary text, headline, description
3. **Performance Data**:
   - CTR (Click-through rate)
   - CPM (Cost per 1000 impressions)
   - CPC (Cost per click)
   - Conversion rate
   - ROAS or CPA
   - Frequency
   - Video metrics (if applicable): ThruPlay rate, avg watch time
4. **Campaign Context**: Objective, audience, placement

## Creative Scoring Framework

### Overall Score Components

| Component | Weight | What It Measures |
|-----------|--------|------------------|
| Scroll-Stop Power | 25% | Does it grab attention? |
| Message Clarity | 20% | Is the value prop clear? |
| Visual Quality | 15% | Production value and appeal |
| Brand Consistency | 10% | Does it match brand identity? |
| CTA Effectiveness | 15% | Does it drive action? |
| Platform Fit | 15% | Is it optimized for placements? |

### Scoring Rubric

**5 - Excellent**: Top 10% performer, clear best practices
**4 - Good**: Above average, minor improvements possible
**3 - Average**: Meets basic requirements, room for growth
**2 - Needs Work**: Underperforming, specific issues identified
**1 - Poor**: Significant problems, recommend replacing

### Performance Benchmarks

| Metric | Poor | Average | Good | Excellent |
|--------|------|---------|------|-----------|
| CTR (Link) | <0.5% | 0.5-1% | 1-2% | >2% |
| CTR (Traffic) | <0.8% | 0.8-1.5% | 1.5-3% | >3% |
| CPM | Varies by audience and objective |
| ThruPlay Rate | <15% | 15-25% | 25-35% | >35% |
| Hook Rate (3s) | <25% | 25-40% | 40-60% | >60% |
| Hold Rate (15s) | <10% | 10-20% | 20-35% | >35% |

*Note: Benchmarks vary significantly by industry, audience, and objective*

## Analysis Components

### 1. Scroll-Stop Analysis

**What makes people stop scrolling**:
- Bold colors or high contrast
- Human faces (especially eyes)
- Movement (video/motion)
- Pattern interrupts
- Curiosity gaps
- Before/after visuals
- Text overlays with hooks

**Red flags**:
- Busy, cluttered visuals
- Stock photo feel
- Generic product shots
- Low contrast colors
- No focal point

### 2. Message Clarity Analysis

**First 3 seconds should answer**:
- What is this?
- Who is it for?
- Why should I care?

**Check for**:
- Value proposition visible immediately
- Benefit-focused (not feature-focused)
- One clear message (not multiple)
- Supporting text reinforces visual

### 3. Visual Quality Assessment

**Evaluate**:
- Resolution (no pixelation)
- Lighting (professional look)
- Composition (rule of thirds, clear focus)
- Brand colors and fonts used
- Text readability on mobile
- Aspect ratio optimized for placement

### 4. CTA Effectiveness

**Strong CTAs**:
- Clear action verb
- Benefit-oriented
- Creates urgency or curiosity
- Matches funnel stage

**Weak CTAs**:
- Generic ("Learn More" with no context)
- Disconnected from creative
- Too aggressive for cold traffic
- No CTA at all

### 5. Video-Specific Analysis

**Hook (0-3 seconds)**:
- Does it start with movement?
- Is there a pattern interrupt?
- Is sound-off optimized (captions)?

**Middle (3-15 seconds)**:
- Is the story progressing?
- Is the product/service shown?
- Are benefits demonstrated?

**End (last 5 seconds)**:
- Clear CTA present?
- Brand reinforcement?
- End card with offer?

## Output: Creative Analysis Report

```markdown
## Creative Analysis Report

**Creative ID/Name**: [identifier]
**Campaign**: [name]
**Analysis Date**: [date]

---

### Overall Score: [X/100]

| Component | Score | Notes |
|-----------|-------|-------|
| Scroll-Stop Power | X/5 | [brief note] |
| Message Clarity | X/5 | [brief note] |
| Visual Quality | X/5 | [brief note] |
| Brand Consistency | X/5 | [brief note] |
| CTA Effectiveness | X/5 | [brief note] |
| Platform Fit | X/5 | [brief note] |

---

### Performance Analysis

**Current Metrics vs Benchmarks**:

| Metric | Actual | Benchmark | Status |
|--------|--------|-----------|--------|
| CTR | X% | X% | [Above/Below] |
| CPM | $X | $X | [Above/Below] |
| CPA | $X | $X | [Above/Below] |
| Frequency | X | <3 | [OK/High] |

**Performance Trend**: [Improving/Stable/Declining]
**Days Active**: [X]
**Fatigue Risk**: [Low/Medium/High]

---

### What's Working

1. **[Element]**: [Why it works and evidence]
2. **[Element]**: [Why it works and evidence]
3. **[Element]**: [Why it works and evidence]

### What's Not Working

1. **[Element]**: [Why it's underperforming and evidence]
2. **[Element]**: [Why it's underperforming and evidence]
3. **[Element]**: [Why it's underperforming and evidence]

---

### Detailed Analysis

**Hook Analysis**:
[Specific feedback on first impression]

**Message Analysis**:
[Feedback on clarity and value proposition]

**Visual Analysis**:
[Feedback on design and quality]

**Copy Analysis**:
[Feedback on primary text, headline, description]

---

### Improvement Recommendations

**Quick Fixes** (test these first):
1. [Specific change with expected impact]
2. [Specific change with expected impact]

**New Variations to Test**:
1. [New concept or angle to try]
2. [Different approach to test against]

**Strategic Changes**:
1. [Bigger shift to consider]

---

### Competitor/Category Context

[How this creative compares to what's common in the space]
[What successful competitors are doing differently]
```

## Creative Fatigue Indicators

**Warning Signs**:
- Frequency > 3 with declining CTR
- Week-over-week CTR decline > 20%
- CPM increasing while CTR decreasing
- Conversion rate dropping
- Negative/repeat comments increasing

**Solutions for Fatigue**:
1. New visual (same message, different execution)
2. New hook (first 3 seconds)
3. New format (static → video, carousel → single)
4. New angle (different benefit emphasized)
5. New audience (same creative, fresh eyes)

## Creative Testing Framework

### What to Test

| Element | Low Effort | High Effort |
|---------|------------|-------------|
| Hook | New first 3 seconds | Entirely new video |
| Visual | Color/filter change | New concept |
| Copy | Headline variation | New messaging angle |
| Format | Aspect ratio | Static vs video |
| CTA | Button text | Offer change |

### Statistical Significance

Before declaring a winner:
- Minimum 1,000 impressions per variant
- At least 100 clicks per variant
- 7+ days of data
- 95% confidence level for conversion-focused campaigns

## Questions to Ask

1. What's the primary objective of this campaign?
2. Who is the target audience?
3. How long has this creative been running?
4. What's your benchmark for success (target CPA/ROAS)?
5. What other creatives are you testing against this?
