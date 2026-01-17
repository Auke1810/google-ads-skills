---
name: google-ads-pmax-auditor
description: Audit Performance Max campaign assets and settings to identify issues and optimization opportunities. Use when reviewing PMax campaigns, grading asset quality, or troubleshooting poor campaign performance.
---

# Google Ads Performance Max Auditor

Grade your Performance Max assets and get specific recommendations for improvement.

## When to Use

- Setting up a new Performance Max campaign
- Troubleshooting underperforming PMax campaigns
- Reviewing asset quality and coverage
- Optimizing existing campaigns for better results

## Input Requirements

Provide:
1. **Asset Group Details**:
   - Headlines (up to 15)
   - Long headlines (up to 5)
   - Descriptions (up to 5)
   - Images (various sizes)
   - Logos
   - Videos (if any)
2. **Campaign Settings**:
   - Final URL
   - Audience signals
   - Goals/conversions tracked
   - Budget and bidding
3. **Performance Data** (if available):
   - Asset performance ratings from Google
   - Conversion data
   - Search categories report

## Audit Framework

### 1. Asset Quantity Check

| Asset Type | Minimum | Recommended | Maximum |
|------------|---------|-------------|---------|
| Headlines | 3 | 11-15 | 15 |
| Long Headlines | 1 | 5 | 5 |
| Descriptions | 2 | 4-5 | 5 |
| Images (landscape) | 1 | 5-10 | 20 |
| Images (square) | 1 | 5-10 | 20 |
| Images (portrait) | 0 | 3-5 | 20 |
| Logos (square) | 1 | 2 | 5 |
| Logos (landscape) | 0 | 1 | 5 |
| Videos | 0 | 1-5 | 5 |

### 2. Asset Quality Grading

**Headlines (Score each 1-5)**:
- [ ] Includes primary keyword naturally
- [ ] Unique value proposition clear
- [ ] Variety of angles (features, benefits, urgency)
- [ ] No redundancy between headlines
- [ ] Proper capitalization (Title Case)

**Long Headlines (Score each 1-5)**:
- [ ] Expands on short headlines
- [ ] Complete thought that works standalone
- [ ] Includes call-to-action when appropriate
- [ ] 90 character limit utilized well

**Descriptions (Score each 1-5)**:
- [ ] Complements headlines (doesn't repeat)
- [ ] Clear CTA included
- [ ] Benefits over features
- [ ] Varied messaging angles

**Images**:
- [ ] High quality, not pixelated
- [ ] Brand consistent
- [ ] Product/service clearly shown
- [ ] No text overlays (or minimal)
- [ ] Variety of compositions

### 3. Settings Audit

**Audience Signals**:
- [ ] Custom segments defined
- [ ] First-party data uploaded (customer lists)
- [ ] Website visitor audiences included
- [ ] Interest/affinity audiences added
- [ ] Demographics refined (if applicable)

**URL Expansion**:
- [ ] Final URL set correctly
- [ ] URL expansion reviewed (on/off based on goals)
- [ ] Excluded URLs added if needed

**Conversion Tracking**:
- [ ] Primary conversion action set
- [ ] Conversion values accurate
- [ ] Enhanced conversions enabled
- [ ] Attribution model appropriate

## Output: Audit Report

```markdown
## Performance Max Audit Report

**Campaign**: [name]
**Audit Date**: [date]
**Overall Grade**: [A/B/C/D/F]

---

### Asset Quantity Score: [X/100]

| Asset Type | Count | Target | Status |
|------------|-------|--------|--------|
| Headlines | X | 15 | [Met/Not Met] |
| Long Headlines | X | 5 | [Met/Not Met] |
| ... | | | |

**Missing Assets**: [list]

---

### Asset Quality Score: [X/100]

#### Headlines Analysis
- **Strong Headlines**: [list]
- **Weak Headlines**: [list with specific issues]
- **Missing Angles**: [suggestions]

#### Image Analysis
- **Quality Issues**: [list]
- **Missing Formats**: [landscape/square/portrait]
- **Recommendations**: [specific guidance]

---

### Settings Score: [X/100]

**Audience Signals**:
- [Issue or OK status]

**Tracking**:
- [Issue or OK status]

---

### Priority Fixes (Do These First)

1. **[HIGH]** [Issue] - [How to fix]
2. **[HIGH]** [Issue] - [How to fix]
3. **[MEDIUM]** [Issue] - [How to fix]

### Quick Wins

- [Small improvement that's easy to implement]
- [Another quick optimization]

### Advanced Optimizations

- [Longer-term improvement suggestion]
- [Testing recommendation]
```

## Common PMax Issues

### Asset Issues
- **Repetitive headlines**: Headlines too similar, limiting ad combinations
- **Missing CTAs**: No clear action words in descriptions
- **Poor image variety**: Same image cropped different ways
- **No video assets**: Missing out on YouTube placements

### Settings Issues
- **Weak audience signals**: Relying only on Google's automation
- **Wrong conversion action**: Optimizing for wrong goal
- **Budget too low**: Not enough data for machine learning
- **URL expansion on**: Traffic going to wrong pages

### Structure Issues
- **Too many asset groups**: Diluting performance data
- **Mixed intents**: Products/services that shouldn't compete
- **No negative keywords**: Wasting spend on brand terms in shopping

## Questions to Ask

1. What is the primary goal of this campaign?
2. Who is your ideal customer?
3. What makes your offer unique vs competitors?
4. Do you have existing customer lists to upload?
5. Are there any pages that shouldn't receive traffic?
