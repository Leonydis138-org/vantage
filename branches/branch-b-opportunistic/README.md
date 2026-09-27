# Branch B — Opportunistic

Scout scans trends, underserved keywords, and new affiliate programs outside the Authority niche. Each candidate niche becomes a test cluster; winners graduate to mini-sites, losers go to maintenance (never deleted without CEO approval).

## Status
`Growing` — no test clusters launched yet. First Scout scan done 2026-09-25 (see `docs/scout-log.md`); 3 candidates logged, all low-confidence pending real keyword data, none approved yet.

## Structure
```
clusters/<cluster-id>/    one folder per test niche
  content/                articles for that cluster
  README.md               hypothesis, target keywords, launch date, review date (4-6 weeks out)
```

## Lifecycle
1. Scout proposes cluster → `decision_queue` entry `new_opportunity`.
2. CEO approves → cluster folder created, quota assigned by Allocator.
3. 4-6 weeks of content + measurement.
4. Allocator scores the cluster → proposes "graduate to mini-site" or "move to maintenance" via `decision_queue`.
5. CEO approves the call.
