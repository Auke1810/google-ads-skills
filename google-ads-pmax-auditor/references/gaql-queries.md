# GAQL Query Pack — Performance Max

Run these for the campaign(s) you're auditing, assemble the result rows into one
JSON file, and hand it to `scripts/analyze_pmax.py`. The script reads the
**REST/JSON camelCase** shape (what the API and client libraries return). The
`SELECT` fields map 1:1 to what the script looks for — don't drop fields.

`asset_group_asset` is the workhorse: it returns each asset's content, its
`field_type` (which slot), and Google's `performance_label` in a single query, so
no manual joining is needed.

## 1. asset groups → `asset_groups`

```sql
SELECT
  asset_group.id,
  asset_group.name,
  asset_group.status,
  asset_group.ad_strength,
  campaign.name
FROM asset_group
WHERE campaign.advertising_channel_type = 'PERFORMANCE_MAX'
  AND asset_group.status != 'REMOVED'
```

## 2. asset group assets (content + label) → `asset_group_assets`

```sql
SELECT
  asset_group.id,
  asset_group_asset.field_type,
  asset_group_asset.performance_label,
  asset_group_asset.status,
  asset.text_asset.text,
  asset.image_asset.full_size.url,
  asset.image_asset.full_size.width_pixels,
  asset.image_asset.full_size.height_pixels,
  asset.youtube_video_asset.youtube_video_id
FROM asset_group_asset
WHERE asset_group_asset.status != 'REMOVED'
```

`performance_label` is `PENDING` / `LEARNING` until the asset group has enough
data, then `LOW` / `GOOD` / `BEST`. On a brand-new (pre-launch) campaign these
will all be pending — that's expected; see the pre-launch vs. live note in
SKILL.md.

## 3. search themes / audience signals → `search_themes`

```sql
SELECT
  asset_group.id,
  asset_group_signal.search_theme.text
FROM asset_group_signal
```

(The script only needs to know which asset groups have a signal; the theme text
helps you judge relevance.)

## 4. campaign settings → `campaigns`

```sql
SELECT
  campaign.name,
  campaign.url_expansion_opt_out
FROM campaign
WHERE campaign.advertising_channel_type = 'PERFORMANCE_MAX'
```

## 5. conversion actions → `conversion_actions`

```sql
SELECT
  conversion_action.name,
  conversion_action.status,
  conversion_action.primary_for_goal,
  conversion_action.value_settings.default_value
FROM conversion_action
```

## Assembling the input

```json
{
  "campaign": "PMax - Footwear",
  "currency": "EUR",
  "date_range": "LAST_30_DAYS",
  "asset_groups":        [ /* query 1 */ ],
  "asset_group_assets":  [ /* query 2 */ ],
  "search_themes":       [ /* query 3 */ ],
  "campaigns":           [ /* query 4 */ ],
  "conversion_actions":  [ /* query 5 */ ]
}
```

A row keeps the nested GAQL shape, e.g. an `asset_group_assets` text row:

```json
{
  "assetGroup": {"id": "100"},
  "assetGroupAsset": {"fieldType": "HEADLINE", "performanceLabel": "LOW"},
  "asset": {"textAsset": {"text": "Premium Running Shoes"}}
}
```

…and an image row (the script fetches `url` to verify it resolves and read real
dimensions; `widthPixels`/`heightPixels` are used as a fallback if the fetch is
skipped with `--no-fetch` or fails):

```json
{
  "assetGroup": {"id": "100"},
  "assetGroupAsset": {"fieldType": "MARKETING_IMAGE", "performanceLabel": "GOOD"},
  "asset": {"imageAsset": {"fullSize": {"url": "https://...", "widthPixels": "1200", "heightPixels": "628"}}}
}
```
