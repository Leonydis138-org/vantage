# `data.json` Schema

The Bridge dashboard reads this file directly (fetched relative to `dashboard/index.html`, or pasted in via the dashboard's "Load data.json" control). Every agent that updates state writes back into this same structure.

## Top-level keys

### `meta`
- `generated_at` (ISO 8601 timestamp) — last time this file was regenerated
- `schema_version` (string)
- `system_status` — `bootstrapping | live | paused`
- `_allocator_prev_snapshot` (object, internal) — written by `scripts/allocator.py`. Per-branch `revenue_30d`/`traffic_30d` from the last run, used to compute growth % on the next run. Not read by the dashboard; safe to ignore when reasoning about state manually.

### `revenue`
- `currency` (string, e.g. `"USD"`)
- `week`, `month`, `all_time` (numbers)
- `trend_pct_30d` (number, +/-)
- `by_source` (array of `{ source: string, amount: number }`)

### `branches` (array)
Each item:
- `id` — `branch_a | branch_b | branch_c`
- `name` (string)
- `status` — `Active | Growing | Maintenance`
- `quota_per_week` (number)
- `traffic_30d`, `clicks_30d`, `conversions_30d`, `revenue_30d` (numbers)
- `score` (number, 0-1, from Allocator formula)
- `notes` (string)

### `decision_queue` (array)
Each item:
- `id` (string)
- `type` — `new_opportunity | affiliate_program_review | support_reply | kill_recommendation | setup`
- `title` (string)
- `detail` (string)
- `requires` — `ceo_approval`
- `created_at` (ISO 8601)

### `activity_feed` (array, newest first recommended)
Each item:
- `timestamp` (ISO 8601)
- `agent` (string — agent name)
- `action` (string, plain language)

### `report`
- `last_weekly_summary` — string (Markdown) or `null`

## Update convention
Agents append/update this file as part of their run (via Claude Code writing to the repo). Never remove `decision_queue` entries — mark them resolved by moving to an (optional) `decision_queue_resolved` array instead, so there's an audit trail.
