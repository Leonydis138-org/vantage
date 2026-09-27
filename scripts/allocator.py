// VANTAGE Allocator — weekly branch scoring job.
// Runs against the real D1 database over Cloudflare's HTTP API using CF_API_TOKEN.
// Implements the scoring rule from VANTAGE-business-build-spec.md Section 5:
//   score = (revenue_growth_30d * 0.5) + (traffic_growth_30d * 0.3) + (conversion_rate * 0.2)
// Top scorer's quota increases (capped at 5/week). Bottom scorer's quota drops toward
// a floor of 1/week — never to 0 ("fade, don't kill"). No branch is ever archived here;
// archival stays a human decision via the Decision Queue.

const ACCOUNT_ID = process.env.CF_ACCOUNT_ID;
const API_TOKEN = process.env.CF_API_TOKEN;
const DATABASE_ID = process.env.D1_DATABASE_ID || "9eed1616-7546-4855-a150-11a92fb7621c";

if (!ACCOUNT_ID || !API_TOKEN) {
  console.error("Missing CF_ACCOUNT_ID or CF_API_TOKEN environment variables.");
  process.exit(1);
}

const D1_URL = `https://api.cloudflare.com/client/v4/accounts/${ACCOUNT_ID}/d1/database/${DATABASE_ID}/query`;

async function d1Query(sql, params = []) {
  const res = await fetch(D1_URL, {
    method: "POST",
    headers: {
      "Authorization": `Bearer ${API_TOKEN}`,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ sql, params })
  });
  const json = await res.json();
  if (!json.success) {
    throw new Error(`D1 query failed: ${JSON.stringify(json.errors)}`);
  }
  return json.result[0].results;
}

async function main() {
  console.log("VANTAGE Allocator — starting weekly run");

  // Self-initializing history table — no manual migration step needed.
  await d1Query(`
    CREATE TABLE IF NOT EXISTS branch_history (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      branch_id TEXT NOT NULL,
      week_start TEXT NOT NULL,
      revenue REAL,
      traffic INTEGER,
      score REAL
    );
  `);

  const branches = await d1Query("SELECT * FROM branches;");
  const weekStart = new Date().toISOString().slice(0, 10);

  const scored = [];

  for (const b of branches) {
    const prevRows = await d1Query(
      "SELECT * FROM branch_history WHERE branch_id = ? ORDER BY id DESC LIMIT 1;",
      [b.id]
    );
    const prev = prevRows[0];

    const revenueGrowth = prev && prev.revenue > 0
      ? (b.revenue_month - prev.revenue) / prev.revenue
      : 0;
    const trafficGrowth = prev && prev.traffic > 0
      ? (b.traffic - prev.traffic) / prev.traffic
      : 0;
    const conversionRate = b.traffic > 0 ? (b.revenue_month > 0 ? 1 : 0) : 0; // placeholder until real conversion tracking exists

    const score = (revenueGrowth * 0.5) + (trafficGrowth * 0.3) + (conversionRate * 0.2);

    scored.push({ ...b, score });

    await d1Query(
      "INSERT INTO branch_history (branch_id, week_start, revenue, traffic, score) VALUES (?, ?, ?, ?, ?);",
      [b.id, weekStart, b.revenue_month, b.traffic, score]
    );

    await d1Query(
      "UPDATE branches SET score = ?, updated_at = datetime('now') WHERE id = ?;",
      [score, b.id]
    );
  }

  // Only reallocate quota if scores actually differ — with everything still at 0
  // (bootstrapping), there's nothing real to rank yet, so leave quotas untouched.
  const scores = scored.map(s => s.score);
  const allEqual = scores.every(s => s === scores[0]);

  let summary;
  if (allEqual) {
    summary = `Allocator ran — all branches scored ${scores[0].toFixed(4)} (no differentiating data yet). Quotas unchanged.`;
  } else {
    const top = scored.reduce((a, b) => (b.score > a.score ? b : a));
    const bottom = scored.reduce((a, b) => (b.score < a.score ? b : a));

    const newTopQuota = Math.min((top.quota_per_week || 0) + 1, 5);
    const newBottomQuota = Math.max((bottom.quota_per_week || 1) - 1, 1); // floor of 1 — fade, don't kill

    await d1Query("UPDATE branches SET quota_per_week = ? WHERE id = ?;", [newTopQuota, top.id]);
    await d1Query("UPDATE branches SET quota_per_week = ? WHERE id = ?;", [newBottomQuota, bottom.id]);

    summary = `Allocator ran — top: ${top.name} (score ${top.score.toFixed(4)}, quota -> ${newTopQuota}/wk). Bottom: ${bottom.name} (score ${bottom.score.toFixed(4)}, quota -> ${newBottomQuota}/wk, floor enforced).`;
  }

  await d1Query(
    "INSERT INTO activity_log (agent, action, timestamp) VALUES ('allocator', ?, datetime('now'));",
    [summary]
  );

  console.log(summary);
  console.log("VANTAGE Allocator — run complete");
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
