#!/usr/bin/env python3
"""
VANTAGE Allocator — weekly branch scoring + quota reallocation.

Implements the formula from docs/build-spec.md:
    score = revenue_growth_30d * 0.5 + traffic_growth_30d * 0.3 + conversion_rate * 0.2
(all inputs normalized 0-1 before weighting)

Reads/writes data.json in place. Safe to run with all-zero data (bootstrapping
phase) — it will not crash, will not zero any quota, and will not archive
anything on its own. See agents/allocator.md guardrails.

Usage:
    python3 scripts/allocator.py                 # run for real, writes data.json
    python3 scripts/allocator.py --dry-run        # print what would change, no write
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = REPO_ROOT / "data.json"

QUOTA_FLOOR = 1  # never go below this — "maintenance" floor, never zero
QUOTA_CEILING = 6  # sane cap so one branch doesn't eat the whole week

# Rolling baselines used to normalize raw 30d numbers into 0-1 before weighting.
# These are deliberately conservative placeholders for the bootstrapping phase
# (everything is 0 right now) — Allocator should tighten these once 60-90 days
# of real traffic/revenue history exists. Documented here, not hidden in math.
BASELINE = {
    "revenue_growth_pct_cap": 100,   # +100% 30d growth = normalized 1.0
    "traffic_growth_pct_cap": 100,   # +100% 30d growth = normalized 1.0
    "conversion_rate_cap": 0.10,     # 10% conversion rate = normalized 1.0
}


def clamp01(x):
    return max(0.0, min(1.0, x))


def compute_score(branch, prev_branch):
    """
    revenue_growth_30d and traffic_growth_30d are % growth vs. the previous
    snapshot of this same branch in data.json (so the script is self-contained
    and doesn't need an external analytics call to run). conversion_rate is
    conversions_30d / clicks_30d (0 if no clicks yet).
    """
    prev_revenue = prev_branch["revenue_30d"] if prev_branch else 0
    prev_traffic = prev_branch["traffic_30d"] if prev_branch else 0

    revenue_growth_pct = pct_growth(prev_revenue, branch["revenue_30d"])
    traffic_growth_pct = pct_growth(prev_traffic, branch["traffic_30d"])

    clicks = branch.get("clicks_30d", 0)
    conversions = branch.get("conversions_30d", 0)
    conversion_rate = (conversions / clicks) if clicks > 0 else 0.0

    revenue_growth_norm = clamp01(revenue_growth_pct / BASELINE["revenue_growth_pct_cap"])
    traffic_growth_norm = clamp01(traffic_growth_pct / BASELINE["traffic_growth_pct_cap"])
    conversion_rate_norm = clamp01(conversion_rate / BASELINE["conversion_rate_cap"])

    score = (
        revenue_growth_norm * 0.5
        + traffic_growth_norm * 0.3
        + conversion_rate_norm * 0.2
    )
    return round(clamp01(score), 4)


def pct_growth(prev, curr):
    if prev <= 0:
        # No prior baseline: treat any positive current value as full-strength
        # growth signal, zero as no growth. Avoids division by zero.
        return 100.0 if curr > 0 else 0.0
    return ((curr - prev) / prev) * 100.0


def reallocate_quota(branches_with_scores):
    """
    Simple rank-based reallocation: highest score gets more quota next week,
    lowest score drops toward the floor. Never below QUOTA_FLOOR, never above
    QUOTA_CEILING. Change per step is small and gradual (+/-1) — this is a
    weekly nudge, not a reset, so a single bad week doesn't wipe a branch's
    quota out.
    """
    ranked = sorted(branches_with_scores, key=lambda b: b["score"], reverse=True)
    n = len(ranked)
    all_tied = len({round(b["score"], 4) for b in ranked}) <= 1
    for i, b in enumerate(ranked):
        current = b["quota_per_week"]
        if all_tied:
            # No signal yet (e.g. bootstrapping phase, everything at 0) —
            # don't arbitrarily reward whichever branch happens to sort first.
            new_quota = current
        elif n > 1 and i == 0:
            new_quota = min(current + 1, QUOTA_CEILING)
        elif n > 1 and i == n - 1:
            new_quota = max(current - 1, QUOTA_FLOOR)
        else:
            new_quota = current  # middle of the pack: hold steady
        b["new_quota"] = new_quota
    return ranked


def status_for(score, current_status):
    """
    Score -> status label. Deliberately hysteresis-free and simple for now —
    a branch only moves to Maintenance on a low score, never below via any
    other path, and nothing here archives anything.
    """
    if score >= 0.5:
        return "Active"
    if score >= 0.2:
        return "Growing"
    return "Maintenance"


def main():
    dry_run = "--dry-run" in sys.argv

    if not DATA_PATH.exists():
        print(f"ERROR: {DATA_PATH} not found", file=sys.stderr)
        sys.exit(1)

    data = json.loads(DATA_PATH.read_text())

    # Snapshot of branch state *before* this run, used as the "previous"
    # baseline for growth-rate math. We keep it in meta so re-runs are
    # comparable; on the very first run there's no prior snapshot (script
    # treats that as prev=0, per pct_growth()).
    prev_snapshot = data.get("meta", {}).get("_allocator_prev_snapshot", {})

    branches = data["branches"]
    scored = []
    for branch in branches:
        prev = prev_snapshot.get(branch["id"])
        score = compute_score(branch, prev)
        scored.append({**branch, "score": score})

    ranked = reallocate_quota(scored)

    changes = []
    for b in ranked:
        old_quota = b["quota_per_week"]
        new_quota = b["new_quota"]
        old_status = b["status"]
        new_status = status_for(b["score"], old_status)

        has_any_data = b["traffic_30d"] or b["clicks_30d"] or b["revenue_30d"]
        skipped_no_data = not has_any_data
        if skipped_no_data:
            # No real traffic/conversions/revenue collected yet (bootstrapping
            # phase) — score is legitimately 0, but that's "no signal", not
            # "this branch is failing". Don't touch quota/status or raise a
            # kill_recommendation off a score with zero underlying data.
            new_quota = old_quota
            new_status = old_status

        changes.append({
            "id": b["id"],
            "name": b["name"],
            "score": b["score"],
            "old_quota": old_quota,
            "new_quota": new_quota,
            "old_status": old_status,
            "new_status": new_status,
            "skipped_no_data": skipped_no_data,
        })

    if dry_run:
        print("DRY RUN — no changes written.\n")
        for c in changes:
            if c["skipped_no_data"]:
                print(f"{c['name']:45s} score={c['score']:.3f}  no data yet — quota/status unchanged")
            else:
                print(
                    f"{c['name']:45s} score={c['score']:.3f}  "
                    f"quota {c['old_quota']} -> {c['new_quota']}  "
                    f"status {c['old_status']} -> {c['new_status']}"
                )
        return

    # Apply changes back into the real branches array, preserving order/ids.
    by_id = {c["id"]: c for c in changes}
    for branch in branches:
        c = by_id[branch["id"]]
        branch["score"] = c["score"]

        if c["skipped_no_data"]:
            continue

        branch["quota_per_week"] = c["new_quota"]

        # Never silently archive/zero a branch. If the formula would drop a
        # branch to Maintenance for the first time, log a decision_queue
        # entry for CEO visibility rather than just changing the status
        # value quietly. Status still updates (Maintenance is a normal,
        # reversible state) — only *archiving* needs approval, and this
        # script never sets an "Archived" status at all.
        if c["new_status"] == "Maintenance" and c["old_status"] != "Maintenance":
            data["decision_queue"].append({
                "id": f"dq_allocator_{branch['id']}_{int(datetime.now(timezone.utc).timestamp())}",
                "type": "kill_recommendation",
                "title": f"{branch['name']} dropped to Maintenance this week",
                "detail": (
                    f"Allocator score {c['score']:.3f} moved this branch to Maintenance "
                    f"floor quota ({c['new_quota']}/wk). This is informational — quota is "
                    f"never zeroed and nothing is archived automatically. Flagging so CEO "
                    f"can decide whether to intervene (new content angle, more time, or "
                    f"eventually consider archiving — archiving always needs separate "
                    f"explicit approval)."
                ),
                "requires": "ceo_approval",
                "created_at": datetime.now(timezone.utc).isoformat(),
            })
        branch["status"] = c["new_status"]

    # Save this run's branch state as next run's "previous" baseline.
    data.setdefault("meta", {})["_allocator_prev_snapshot"] = {
        b["id"]: {"revenue_30d": b["revenue_30d"], "traffic_30d": b["traffic_30d"]}
        for b in branches
    }
    data["meta"]["generated_at"] = datetime.now(timezone.utc).isoformat()

    summary_lines = []
    for c in changes:
        if c.get("skipped_no_data"):
            summary_lines.append(f"{c['name']}: no traffic/revenue data yet — quota/status unchanged")
        else:
            summary_lines.append(
                f"{c['name']}: score {c['score']:.3f}, quota {c['old_quota']}→{c['new_quota']}, "
                f"status {c['old_status']}→{c['new_status']}"
            )
    data["activity_feed"].insert(0, {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "agent": "Allocator",
        "action": "Weekly scoring run. " + " | ".join(summary_lines),
    })

    DATA_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    print("data.json updated:")
    for line in summary_lines:
        print(" -", line)


if __name__ == "__main__":
    main()
