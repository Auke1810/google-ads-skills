---
name: landing-page-auditor
description: Audit landing pages for conversion optimization, identifying issues that cause ad traffic to bounce. Use when diagnosing poor conversion rates, reviewing pages before ad campaigns, or optimizing existing landing pages.
---

# Landing Page Auditor

Find why your ad traffic isn't converting and fix the landing page issues killing your ROAS.

## When to Use

- High traffic but low conversions
- Reviewing pages before launching ads
- Diagnosing high bounce rates
- Improving Quality Score (Google Ads)
- Optimizing for better CPA/ROAS

## The Problem

**Great ads + bad landing page = wasted spend**

Industry average landing page conversion rates:
- Lead gen: 2-5%
- E-commerce: 2-3%
- SaaS: 3-7%

Top performers: 2-3x these numbers

## Input Requirements

Provide:
1. **Landing Page URL**: The page to audit
2. **Traffic Source**: Google, Meta, TikTok, etc.
3. **Campaign Goal**: Leads, purchases, signups
4. **Target Audience**: Who's landing on this page
5. **Current Metrics**: Conversion rate, bounce rate, time on page
6. **Ad Creative**: What promise brought them here

## Audit Framework (10 Categories)

### 1. Message Match Audit

**The #1 conversion killer: broken promises**

- [ ] Headline matches ad headline/promise
- [ ] Visual continuity from ad to page
- [ ] Same offer mentioned in ad appears on page
- [ ] Tone and voice consistent
- [ ] Target audience feels "this is for me"

**Test**: Read ad → land on page → does it feel like continuation?

### 2. Above-the-Fold Audit

**You have 3-5 seconds to convince them to stay**

- [ ] Clear headline stating value proposition
- [ ] Supporting subheadline with specifics
- [ ] Hero image/video reinforces message
- [ ] Primary CTA visible without scrolling
- [ ] No distracting navigation stealing attention

**Above-the-fold checklist**:
| Element | Present | Effective |
|---------|---------|-----------|
| Headline | [Y/N] | [Y/N] |
| Subheadline | [Y/N] | [Y/N] |
| Hero visual | [Y/N] | [Y/N] |
| CTA button | [Y/N] | [Y/N] |
| Value prop clear | [Y/N] | [Y/N] |

### 3. Value Proposition Audit

- [ ] Clear what you're offering
- [ ] Clear who it's for
- [ ] Clear why it's better than alternatives
- [ ] Specific benefits (not vague claims)
- [ ] Unique differentiator stated

**Value Prop Formula**:
```
[Product] helps [audience] achieve [outcome] by [unique mechanism]
```

### 4. CTA Audit

**Primary CTA**:
- [ ] One clear primary action
- [ ] Button text is specific (not "Submit" or "Click Here")
- [ ] Button stands out visually (contrast)
- [ ] CTA appears multiple times on long pages
- [ ] Mobile CTA is thumb-friendly

**CTA Button Hierarchy**:
| Type | Example | Use |
|------|---------|-----|
| Action + Benefit | "Get My Free Quote" | Primary CTA |
| Action Only | "Sign Up" | Secondary |
| Vague | "Submit" | Never use |

### 5. Trust & Credibility Audit

- [ ] Social proof present (testimonials, reviews)
- [ ] Trust badges (security, payment, certifications)
- [ ] Company credentials visible
- [ ] Real customer photos (not stock)
- [ ] Press mentions or logos
- [ ] Case studies or results

**Trust Elements Checklist**:
| Element | Present | Placement |
|---------|---------|-----------|
| Testimonials | [Y/N] | [Location] |
| Star ratings | [Y/N] | [Location] |
| Customer logos | [Y/N] | [Location] |
| Security badges | [Y/N] | [Location] |
| Guarantee | [Y/N] | [Location] |

### 6. Form/Checkout Audit

**For Lead Gen**:
- [ ] Minimum fields required
- [ ] Form above fold or easily accessible
- [ ] Clear privacy assurance
- [ ] No unnecessary friction
- [ ] Mobile-optimized form

**For E-commerce**:
- [ ] Guest checkout available
- [ ] Multiple payment options
- [ ] Clear shipping info
- [ ] Easy cart modifications
- [ ] Progress indicator

**Form Field Analysis**:
| Field | Necessary | Remove? |
|-------|-----------|---------|
| [Field] | [Y/N] | [Y/N] |

### 7. Page Speed Audit

**Speed = Conversions**
- 1 second delay = 7% conversion loss
- 40% abandon if >3 seconds

- [ ] Page loads under 3 seconds
- [ ] Images optimized/compressed
- [ ] No render-blocking resources
- [ ] Mobile speed acceptable
- [ ] Core Web Vitals passing

**Speed Metrics**:
| Metric | Current | Target |
|--------|---------|--------|
| Load Time | [X]s | <3s |
| LCP | [X]s | <2.5s |
| FID | [X]ms | <100ms |
| CLS | [X] | <0.1 |

### 8. Mobile Experience Audit

**60%+ traffic is mobile**

- [ ] Responsive design works
- [ ] Text readable without zooming
- [ ] Buttons large enough to tap
- [ ] Forms easy to complete
- [ ] No horizontal scrolling
- [ ] CTA visible on mobile viewport

### 9. Content & Copy Audit

**Readability**:
- [ ] Short paragraphs (2-3 sentences)
- [ ] Bullet points for scanning
- [ ] Clear hierarchy (H1, H2, H3)
- [ ] Simple language (8th grade reading level)
- [ ] No jargon unless audience expects it

**Persuasion Elements**:
- [ ] Benefits over features
- [ ] Specific numbers and results
- [ ] Emotional triggers present
- [ ] Objections addressed
- [ ] Urgency/scarcity (if authentic)

### 10. Technical & UX Audit

- [ ] No broken links or images
- [ ] All buttons/forms work
- [ ] Pop-ups don't block content
- [ ] Exit intent used appropriately
- [ ] No auto-playing audio
- [ ] Accessible (contrast, alt text)

## Output: Landing Page Audit Report

```markdown
## Landing Page Audit Report

**URL**: [landing page URL]
**Audit Date**: [date]
**Traffic Source**: [platform]
**Goal**: [conversion action]

---

### Overall Conversion Score: [X/100]

| Category | Score | Priority |
|----------|-------|----------|
| Message Match | X/10 | [High/Med/Low] |
| Above the Fold | X/10 | [High/Med/Low] |
| Value Proposition | X/10 | [High/Med/Low] |
| CTA Effectiveness | X/10 | [High/Med/Low] |
| Trust & Credibility | X/10 | [High/Med/Low] |
| Form/Checkout | X/10 | [High/Med/Low] |
| Page Speed | X/10 | [High/Med/Low] |
| Mobile Experience | X/10 | [High/Med/Low] |
| Content & Copy | X/10 | [High/Med/Low] |
| Technical/UX | X/10 | [High/Med/Low] |

**Estimated Conversion Impact**: [current]% → [potential]%

---

### Critical Issues (Fix First)

| Issue | Impact | Fix |
|-------|--------|-----|
| [Issue] | [High/Med] | [Solution] |
| [Issue] | [High/Med] | [Solution] |

---

### Above-the-Fold Analysis

**Current State**:
[Description of what appears above fold]

**Issues**:
1. [Issue]
2. [Issue]

**Recommended Changes**:
1. [Specific change]
2. [Specific change]

---

### Message Match Analysis

**Ad Promise**: "[What the ad says]"
**Landing Page Delivers**: [Yes/No/Partially]

**Gap Identified**:
[Description of mismatch]

**Fix**:
[How to align message]

---

### CTA Analysis

**Current CTA**: "[Button text]"
**Visibility**: [Good/Poor]
**Clarity**: [Good/Poor]

**Recommended CTA**: "[New button text]"
**Recommended Placement**: [Where]

---

### Trust Elements Analysis

**Present**:
- [Element]
- [Element]

**Missing**:
- [Element] - Impact: [why important]
- [Element] - Impact: [why important]

---

### Speed Analysis

| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| Load Time | [X]s | <3s | [Pass/Fail] |
| Mobile Speed | [X]s | <3s | [Pass/Fail] |

**Speed Fixes**:
1. [Specific fix]
2. [Specific fix]

---

### Mobile Analysis

**Current Experience**: [Good/Needs Work/Poor]

**Issues Found**:
1. [Issue with screenshot description]
2. [Issue with screenshot description]

---

### Copy Recommendations

**Headline**:
- Current: "[current headline]"
- Recommended: "[improved headline]"

**Subheadline**:
- Current: "[current]"
- Recommended: "[improved]"

**CTA Button**:
- Current: "[current]"
- Recommended: "[improved]"

---

### A/B Test Recommendations

**Test 1**: [Element to test]
- Variant A: [Description]
- Variant B: [Description]
- Hypothesis: [Expected outcome]

**Test 2**: [Element to test]
- Variant A: [Description]
- Variant B: [Description]
- Hypothesis: [Expected outcome]

---

### Implementation Priority

**Week 1 (Quick Wins)**:
1. [Change] - Expected impact: [X]%
2. [Change] - Expected impact: [X]%

**Week 2-3 (Medium Effort)**:
1. [Change]
2. [Change]

**Week 4+ (Larger Changes)**:
1. [Change]
2. [Change]
```

## Common Landing Page Mistakes

### Mistake 1: Sending Traffic to Homepage
**Fix**: Create dedicated landing pages for each campaign

### Mistake 2: Too Many CTAs
**Fix**: One primary action per page

### Mistake 3: Feature Dumping
**Fix**: Lead with benefits, support with features

### Mistake 4: No Social Proof
**Fix**: Add testimonials near CTA

### Mistake 5: Slow Load Time
**Fix**: Optimize images, minimize scripts

### Mistake 6: Weak Headlines
**Fix**: Specific outcome + target audience

## Questions to Ask

1. What's the current conversion rate?
2. What does your ad say/show?
3. What action should visitors take?
4. Who is your target audience?
5. What objections might they have?
6. What makes you different from competitors?
