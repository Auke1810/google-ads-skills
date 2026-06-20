# Input Data — GAQL or CSV

The script accepts either source and auto-detects which.

## Option A — GAQL JSON (consistent with the other audit skills)

Run this query and put the result rows under a `search_terms` key.

```sql
SELECT
  search_term_view.search_term,
  segments.search_term_match_type,
  campaign.name,
  ad_group.name,
  metrics.clicks,
  metrics.impressions,
  metrics.cost_micros,
  metrics.conversions,
  metrics.conversions_value
FROM search_term_view
WHERE segments.date DURING LAST_30_DAYS
```

Assemble:

```json
{
  "currency": "EUR",
  "date_range": "LAST_30_DAYS",
  "search_terms": [
    {
      "searchTermView": {"searchTerm": "buy running shoes online"},
      "segments": {"searchTermMatchType": "BROAD"},
      "campaign": {"name": "Non-Brand"},
      "metrics": {"clicks": 120, "impressions": 2000, "costMicros": "240000000",
                  "conversions": 12, "conversionsValue": 1800}
    }
  ]
}
```

Cost is micros (the script divides by 1,000,000); leave it as-is.

## Option B — Search Terms CSV (straight from the UI)

In Google Ads: **Reports → Predefined reports (Details) → Search terms**, or the
Search terms view → download as CSV. Hand the file to the script directly:

```bash
python3 classify_terms.py search-terms.csv --target-cpa 25
```

The parser handles what the UI export actually produces:
- the title/date **preamble rows** above the header,
- the **totals footer** row,
- **either number locale** (`1,234.56` or `1.234,56`) — detected from the file,
- currency symbols / a `Currency code` column.

It needs at least a `Search term` column plus `Clicks`, `Cost`, and
`Conversions`; `Conv. value`, `Campaign`, `Ad group`, and `Match type` are used
when present.

## Targets

Pass `--target-cpa` and/or `--target-roas` to judge tiers against your goals.
Without them, the script uses the report's **own blended CPA and conversion rate**
as the benchmark — so it still produces a sensible split on raw data, it just
grades "good vs. the account average" instead of "good vs. your target."
