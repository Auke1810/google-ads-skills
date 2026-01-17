---
name: meta-ads-pixel-auditor
description: Audit Meta Pixel and Conversions API setup to identify tracking gaps and fix iOS 14.5+ data loss. Use when troubleshooting conversion tracking, setting up new pixels, or diagnosing attribution issues.
---

# Meta Pixel & CAPI Auditor

Diagnose tracking gaps and fix the iOS 14.5+ data loss that's hurting your campaign performance.

## When to Use

- Conversion numbers don't match actual sales
- Campaign optimization seems off
- Setting up a new Meta Pixel
- Onboarding new client accounts
- After iOS updates or tracking changes
- ROAS reporting seems inaccurate

## The iOS 14.5+ Problem

**What happened**: Apple's App Tracking Transparency (ATT) lets users opt out of tracking. 80-90% opt out.

**Impact on Meta Ads**:
- 30-40% of conversions not tracked
- Delayed conversion reporting (up to 72 hours)
- Limited to 8 conversion events per domain
- Less data for optimization = worse performance

**Solution**: Meta Pixel + Conversions API (CAPI) together = maximum data recovery

## Input Requirements

Provide:
1. **Pixel ID**: Found in Events Manager
2. **Website URL**: For testing events
3. **Events Manager Screenshots**: Showing event setup
4. **Conversion Events Used**: What you're tracking
5. **Current Issues**: What's not working

## Audit Framework

### 1. Pixel Installation Check

**Basic Installation**:
- [ ] Pixel base code installed on all pages
- [ ] Pixel ID is correct
- [ ] No duplicate pixels causing double-firing
- [ ] Pixel loads before page content

**Installation Methods**:
| Method | Reliability | Recommendation |
|--------|-------------|----------------|
| Manual code | High | Best for custom sites |
| Partner integration | Medium-High | Good for Shopify, WooCommerce |
| Google Tag Manager | Medium | Watch for timing issues |
| Plugin | Varies | Check plugin quality |

**Test with Meta Pixel Helper**:
- Chrome extension shows pixel firing
- Checks for errors
- Shows events and parameters

### 2. Standard Events Audit

**E-commerce Essential Events**:
```
PageView → ViewContent → AddToCart → InitiateCheckout → Purchase
```

- [ ] PageView fires on all pages
- [ ] ViewContent fires on product pages
- [ ] AddToCart fires when items added
- [ ] InitiateCheckout fires at checkout start
- [ ] Purchase fires on confirmation (with value)

**Lead Generation Events**:
```
PageView → ViewContent → Lead (or CompleteRegistration)
```

- [ ] Lead event fires on form submission
- [ ] CompleteRegistration for signups
- [ ] Contact event for contact forms

**Event Parameters**:
- [ ] `value` parameter included (required for ROAS)
- [ ] `currency` parameter set correctly
- [ ] `content_ids` for dynamic ads
- [ ] `content_type` for catalog matching

### 3. Conversions API (CAPI) Audit

**CAPI Status**:
- [ ] CAPI is implemented (not just Pixel)
- [ ] Server events showing in Events Manager
- [ ] Event match quality score visible

**Event Match Quality**:
| Score | Status | Action |
|-------|--------|--------|
| Poor (<5) | Critical | Add more parameters |
| OK (5-7) | Needs work | Improve matching |
| Good (7-9) | Acceptable | Minor optimization |
| Great (9-10) | Excellent | Maintain |

**Required CAPI Parameters for Matching**:
- [ ] `em` (email) - hashed
- [ ] `ph` (phone) - hashed
- [ ] `fn` (first name) - hashed
- [ ] `ln` (last name) - hashed
- [ ] `external_id` (customer ID) - hashed
- [ ] `client_ip_address`
- [ ] `client_user_agent`
- [ ] `fbc` (click ID from URL)
- [ ] `fbp` (browser ID from cookie)

### 4. Deduplication Check

**The Problem**: Pixel + CAPI both fire = double counting

**Solution**: Event deduplication via `event_id`

- [ ] Same `event_id` sent from Pixel AND CAPI
- [ ] Events Manager shows deduplicated events
- [ ] No duplicate conversions in reporting

**How to Test**:
1. Trigger a conversion
2. Check Events Manager
3. Should see ONE event, not two
4. "Deduplicated" indicator visible

### 5. Event Configuration in Events Manager

**Aggregated Event Measurement (AEM)**:
- [ ] Domain verified
- [ ] 8 events prioritized correctly
- [ ] Highest-value event ranked #1 (usually Purchase)

**Event Priority Order** (example for e-commerce):
1. Purchase
2. InitiateCheckout
3. AddToCart
4. ViewContent
5. Lead
6. Search
7. PageView
8. (spare slot)

**Configuration Settings**:
- [ ] Value optimization enabled (if tracking value)
- [ ] Correct attribution window set
- [ ] Standard vs custom events appropriate

### 6. Attribution Settings Audit

**Attribution Window**:
- [ ] 7-day click (standard, recommended)
- [ ] 1-day view (optional, adds view-through)
- [ ] Consistent across campaigns for fair comparison

**Post-iOS Reality**:
- Data modeled for opted-out users
- Some delay in reporting (up to 72 hours)
- Aggregated data, less granular

### 7. Data Quality Check

**Events Manager Diagnostics**:
- [ ] No "inactive" events
- [ ] No error messages
- [ ] Event count matches expected volume
- [ ] No sudden drops in events

**Common Errors**:
| Error | Cause | Fix |
|-------|-------|-----|
| "Invalid currency" | Wrong currency code | Use ISO 4217 (USD, EUR) |
| "Missing parameter" | Required param not sent | Add missing parameter |
| "Duplicate events" | No deduplication | Add event_id |
| "Low match quality" | Missing customer data | Add email, phone, etc. |

## Output: Pixel Audit Report

```markdown
## Meta Pixel & CAPI Audit Report

**Pixel ID**: [ID]
**Domain**: [URL]
**Audit Date**: [date]

---

### Overall Tracking Health: [X/100]

| Component | Status | Score |
|-----------|--------|-------|
| Pixel Installation | [OK/Issue] | X/10 |
| Standard Events | [OK/Issue] | X/10 |
| CAPI Implementation | [OK/Issue] | X/10 |
| Deduplication | [OK/Issue] | X/10 |
| Event Configuration | [OK/Issue] | X/10 |
| Event Match Quality | [Score] | X/10 |

**Estimated Data Loss**: [X]% of conversions not tracked
**Potential Recovery**: [X]% with fixes below

---

### Critical Issues (Fix Immediately)

| Issue | Impact | Fix |
|-------|--------|-----|
| [Issue] | [% data loss] | [How to fix] |
| [Issue] | [Impact] | [How to fix] |

---

### Event Status

| Event | Pixel | CAPI | Dedupe | Match Quality |
|-------|-------|------|--------|---------------|
| Purchase | [Y/N] | [Y/N] | [Y/N] | [Score] |
| InitiateCheckout | [Y/N] | [Y/N] | [Y/N] | [Score] |
| AddToCart | [Y/N] | [Y/N] | [Y/N] | [Score] |
| ViewContent | [Y/N] | [Y/N] | [Y/N] | [Score] |

---

### CAPI Implementation Details

**Current Status**: [Not implemented / Partial / Full]

**Event Match Quality Breakdown**:
- Email matching: [Y/N]
- Phone matching: [Y/N]
- Name matching: [Y/N]
- External ID: [Y/N]
- Click ID (fbc): [Y/N]
- Browser ID (fbp): [Y/N]

**Recommendations to Improve Match Quality**:
1. [Specific recommendation]
2. [Specific recommendation]

---

### Event Priority Configuration

**Current Priority**:
1. [Event 1]
2. [Event 2]
...

**Recommended Priority**:
1. [Event 1] - [reason]
2. [Event 2] - [reason]
...

---

### Implementation Roadmap

**Phase 1: Quick Fixes (This Week)**
1. [Fix with instructions]
2. [Fix with instructions]

**Phase 2: CAPI Setup (Week 2)**
1. [Step]
2. [Step]

**Phase 3: Optimization (Week 3-4)**
1. [Step]
2. [Step]

---

### Testing Checklist

After implementing fixes, verify:
- [ ] Test purchase shows in Events Manager
- [ ] Event shows as deduplicated
- [ ] Match quality improved
- [ ] No errors in diagnostics
- [ ] Campaign reporting reflects changes
```

## CAPI Implementation Options

### Option 1: Partner Integrations (Easiest)
- Shopify: Native integration
- WooCommerce: Official plugin
- WordPress: PixelYourSite or similar

### Option 2: Google Tag Manager Server-Side
- More control
- Requires GTM server container
- Medium technical difficulty

### Option 3: Direct API Implementation
- Maximum control
- Requires developer
- Best for custom platforms

## Common Issues & Fixes

### Issue: Low Event Match Quality
**Fix**: Send more customer parameters (email, phone) hashed via CAPI

### Issue: Duplicate Events
**Fix**: Implement event_id matching between Pixel and CAPI

### Issue: Events Not Firing
**Fix**: Check Pixel Helper for errors, verify code placement

### Issue: Wrong Conversion Values
**Fix**: Ensure value and currency parameters are correct

### Issue: Delayed Reporting
**Reality**: This is normal post-iOS 14.5 - wait 72 hours for full data

## Questions to Ask

1. What platform is your website built on?
2. Are you using any pixel management plugins?
3. What conversion events are most important?
4. Do you have developer resources available?
5. Are you seeing discrepancies between Meta and actual sales?
