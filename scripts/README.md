# Scripts

Automation scripts referenced by `.github/workflows/*`:

- `allocator.py` — **implemented.** Weekly scoring per the formula in `docs/build-spec.md`: `score = revenue_growth_30d*0.5 + traffic_growth_30d*0.3 + conversion_rate*0.2`. Reads/writes `data.json` in place. Growth is computed against the previous run's snapshot (stored in `data.json` → `meta._allocator_prev_snapshot`), so it doesn't need an external analytics call to run. Skips quota/status changes entirely for any branch with zero traffic/clicks/revenue (no real signal yet — avoids punishing a branch just because it hasn't launched). Never sets quota to 0 (floor is 1/week) and never archives — a drop to `Maintenance` status only logs a `kill_recommendation` decision_queue entry for CEO visibility. Run `python3 scripts/allocator.py --dry-run` to preview without writing.
- `check_links.py` — affiliate link health check (Build Order step 3+). Not yet implemented.
- `build_site.py` — renders `branches/*/content/*.md` (status: ready-to-publish) to static HTML for Pages deploy (Build Order step 2). Not yet implemented.

Test the allocator locally any time:
```
python3 scripts/allocator.py --dry-run
```
