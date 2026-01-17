---
name: google-ads-shopping-feed
description: Audit Google Shopping product feed titles and descriptions for issues that hurt performance. Use when optimizing Merchant Center feeds, troubleshooting disapprovals, or improving Shopping ad quality.
---

# Google Shopping Feed Auditor

Check your product titles and descriptions for issues that hurt Shopping performance.

## When to Use

- Optimizing Google Merchant Center feeds
- Troubleshooting product disapprovals
- Improving Shopping campaign performance
- Preparing feeds for new product launches
- Fixing low impression share issues

## Input Requirements

Provide product feed data including:
- Product title
- Description
- Product type / Category
- Brand
- GTIN/MPN/SKU
- Price
- Image URL (for visual audit)
- Any current disapproval messages

## Audit Framework

### 1. Title Audit

**Title Structure (Optimal)**:
```
[Brand] + [Product Name] + [Key Attributes] + [Model/SKU]
```

**Character Limits**:
- Maximum: 150 characters
- Recommended: 70-100 characters (visible in most placements)

**Title Checklist**:
- [ ] Brand name included (required for most categories)
- [ ] Product type clear from title
- [ ] Key attributes present (color, size, material, gender)
- [ ] No promotional text ("Sale", "Free Shipping", "Best")
- [ ] No excessive capitalization
- [ ] No keyword stuffing
- [ ] Spelling is correct
- [ ] Most important info in first 70 characters

**Common Title Issues**:

| Issue | Example | Fix |
|-------|---------|-----|
| Missing brand | "Men's Running Shoes" | "Nike Men's Running Shoes" |
| Missing attributes | "Nike Shoes" | "Nike Air Max 90 Men's Running Shoes Black" |
| Promo text | "SALE! Nike Shoes 50% Off" | "Nike Air Max 90 Running Shoes" |
| All caps | "NIKE AIR MAX RUNNING SHOES" | "Nike Air Max Running Shoes" |
| Keyword stuffed | "Shoes Running Shoes Nike Shoes Athletic" | "Nike Air Max Running Shoes" |

### 2. Description Audit

**Character Limits**:
- Maximum: 5,000 characters
- Recommended: 500-1,000 characters

**Description Checklist**:
- [ ] Accurate product information
- [ ] Key features and benefits included
- [ ] No HTML tags (unless explicitly supported)
- [ ] No promotional language
- [ ] No links to other websites
- [ ] No competitor mentions
- [ ] Proper formatting (paragraphs, bullets if supported)

**Description Structure**:
```
[Opening hook - what is the product]
[Key features - 3-5 bullet points or sentences]
[Specifications - size, material, dimensions]
[Use case - who it's for, when to use]
```

### 3. Category/Product Type Audit

- [ ] Google Product Category correctly mapped
- [ ] Product type uses full breadcrumb path
- [ ] Category matches actual product
- [ ] No generic categories when specific exists

**Example Product Type Path**:
```
Bad: Apparel
Good: Apparel & Accessories > Clothing > Activewear > Athletic Shirts
```

### 4. Image Audit

- [ ] Main image on white/neutral background
- [ ] Product fills 75-90% of image
- [ ] No watermarks or promotional overlays
- [ ] No placeholder images
- [ ] Minimum 100x100 pixels (800x800 recommended)
- [ ] No multiple products (unless bundle)

### 5. Required Attributes Check

**Universal Requirements**:
- id (unique identifier)
- title
- description
- link (product page URL)
- image_link
- price
- availability
- brand (or MPN/GTIN for unbranded)

**Category-Specific**:
- Apparel: gender, age_group, color, size
- Electronics: GTIN required
- Media: GTIN, condition

## Output: Feed Audit Report

```markdown
## Shopping Feed Audit Report

**Products Analyzed**: [count]
**Audit Date**: [date]
**Overall Health Score**: [X/100]

---

### Critical Issues (Fix Immediately)

These cause disapprovals or major performance problems:

| Product ID | Issue | Current | Recommended |
|------------|-------|---------|-------------|
| [SKU] | [issue] | "[current]" | "[fixed]" |
| ... | | | |

**Disapproval Risk**: [X] products

---

### High Priority (Significant Impact)

These hurt Quality Score and visibility:

| Product ID | Issue | Impact |
|------------|-------|--------|
| [SKU] | [issue] | [expected improvement] |
| ... | | |

---

### Medium Priority (Optimization)

Nice to fix for better performance:

| Issue Type | Affected Products | Recommendation |
|------------|------------------|----------------|
| [issue pattern] | [X] products | [bulk fix suggestion] |
| ... | | |

---

### Title Rewrites

**Before → After examples**:

Product: [SKU]
- Before: "[current title]"
- After: "[optimized title]"
- Changes: [what was improved]

[Repeat for top priority products]

---

### Description Improvements

Product: [SKU]
- Issue: [what's wrong]
- Recommended: "[improved description snippet]"

---

### Category Mapping Issues

| Product | Current Category | Recommended |
|---------|-----------------|-------------|
| [SKU] | [current] | [better match] |

---

### Summary Statistics

| Metric | Count | % of Feed |
|--------|-------|-----------|
| Titles under 50 chars | X | X% |
| Missing brand in title | X | X% |
| Description under 100 chars | X | X% |
| Wrong product type | X | X% |
| Image issues | X | X% |

---

### Quick Wins

1. [Batch fix that improves many products at once]
2. [Simple change with high impact]
3. [Template improvement for consistency]
```

## Title Optimization by Category

### Apparel
```
[Brand] [Gender] [Product Type] [Style/Fit] [Color] [Size if relevant]
Example: Nike Women's Running Shorts Tempo Dri-FIT Black
```

### Electronics
```
[Brand] [Product Line] [Model] [Key Spec] [Capacity/Size]
Example: Apple MacBook Pro 14-inch M3 Pro Chip 18GB RAM 512GB SSD
```

### Home & Garden
```
[Brand] [Product Type] [Material] [Size/Dimensions] [Color/Pattern]
Example: Cuisinart Stainless Steel Cookware Set 12-Piece Silver
```

### Beauty
```
[Brand] [Product Line] [Product Type] [Variant] [Size]
Example: CeraVe Hydrating Facial Cleanser Normal to Dry Skin 16 oz
```

## Common Policy Violations

1. **Promotional text in titles**: No "Sale", "Discount", "Free Shipping"
2. **Misleading information**: Price/availability must match landing page
3. **Counterfeit products**: No replicas or knockoffs
4. **Adult content**: Must be properly categorized
5. **Prohibited products**: Check Google's policies

## Questions to Ask

1. What product categories are you selling?
2. Do you have brand approval for branded products?
3. Are you selling internationally (language/currency)?
4. What feed management tool do you use?
5. Are there specific products with disapprovals?
