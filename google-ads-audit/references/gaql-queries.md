# GAQL Query Pack

These are the exact [GAQL](https://developers.google.com/google-ads/api/docs/query/overview)
queries that pull every dataset the audit needs. Run them however you have
account access — the official `google-ads` client library, the REST endpoint, or
the Query Builder in the Google Ads UI — then assemble the results into one JSON
file and hand it to `scripts/analyze_account.py`.

The script reads the **REST/JSON camelCase** shape (what `googleads.googleapis.com`
returns and what the client libraries serialize to). The `SELECT` fields below
map 1:1 to the keys the script looks for, so don't drop fields.

Adjust `LAST_30_DAYS` to your audit window (e.g. `LAST_90_DAYS`) — keep it
consistent across all queries.

## 1. campaigns → `campaigns`

```sql
SELECT
  campaign.name,
  campaign.advertising_channel_type,
  campaign.bidding_strategy_type,
  campaign.network_settings.target_search_network,
  campaign.network_settings.target_content_network,
  campaign_budget.amount_micros,
  metrics.cost_micros,
  metrics.conversions,
  metrics.clicks,
  metrics.impressions,
  metrics.search_budget_lost_impression_share,
  metrics.search_rank_lost_impression_share
FROM campaign
WHERE segments.date DURING LAST_30_DAYS
  AND campaign.status = 'ENABLED'
```

## 2. keywords → `keywords`

```sql
SELECT
  campaign.name,
  ad_group.name,
  ad_group_criterion.keyword.text,
  ad_group_criterion.keyword.match_type,
  ad_group_criterion.quality_info.quality_score,
  ad_group_criterion.status,
  metrics.cost_micros,
  metrics.conversions,
  metrics.clicks
FROM keyword_view
WHERE segments.date DURING LAST_30_DAYS
  AND ad_group_criterion.status != 'REMOVED'
```

## 3. search terms → `search_terms`

```sql
SELECT
  search_term_view.search_term,
  metrics.cost_micros,
  metrics.conversions,
  metrics.clicks
FROM search_term_view
WHERE segments.date DURING LAST_30_DAYS
```

## 4. ads → `ads`

```sql
SELECT
  ad_group.id,
  ad_group.name,
  ad_group_ad.ad_strength,
  ad_group_ad.status
FROM ad_group_ad
WHERE segments.date DURING LAST_30_DAYS
  AND ad_group_ad.status != 'REMOVED'
```

## 5. conversion actions → `conversion_actions`

Config, not performance — no date segment or metrics.

```sql
SELECT
  conversion_action.name,
  conversion_action.status,
  conversion_action.type,
  conversion_action.primary_for_goal,
  conversion_action.value_settings.default_value
FROM conversion_action
```

## Assembling the input file

Put each query's result rows under the matching key. Every dataset is optional —
the script skips checks it has no data for and reports which checks ran — but the
audit is only as complete as the data you provide. Lead with **search_terms**,
**keywords**, and **conversion_actions**: those drive the wasted-spend figure and
the tracking verdict, which are the highest-value findings.

```json
{
  "account": "Example NV",
  "currency": "EUR",
  "date_range": "LAST_30_DAYS",
  "campaigns":          [ /* rows from query 1 */ ],
  "keywords":           [ /* rows from query 2 */ ],
  "search_terms":       [ /* rows from query 3 */ ],
  "ads":                [ /* rows from query 4 */ ],
  "conversion_actions": [ /* rows from query 5 */ ]
}
```

A row keeps the nested GAQL shape exactly, e.g. a campaigns row:

```json
{
  "campaign": {"name": "Brand", "advertisingChannelType": "SEARCH",
               "biddingStrategyType": "TARGET_CPA",
               "networkSettings": {"targetSearchNetwork": true, "targetContentNetwork": false}},
  "campaignBudget": {"amountMicros": "30000000"},
  "metrics": {"costMicros": "450000000", "conversions": 42, "clicks": 900,
              "impressions": 12000, "searchBudgetLostImpressionShare": 0.31,
              "searchRankLostImpressionShare": 0.08}
}
```

### Running via the official client (sketch)

```python
# google-ads client returns protobuf; serialize each row to a dict and collect.
from google.protobuf.json_format import MessageToDict
rows = [MessageToDict(r._pb) for r in ga_service.search(customer_id=cid, query=QUERY)]
```

Money fields come back as micros strings — the script divides by 1,000,000, so
leave them as-is.
