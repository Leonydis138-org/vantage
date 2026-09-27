# VANTAGE — Autonomous Revenue System

Owner/CEO: Juan-Louw Greyling

Three-branch content + micro-SaaS revenue engine, run mostly by AI agents with the CEO as trigger and approver. Full spec in [`docs/build-spec.md`](docs/build-spec.md).

## Status: Build Order complete (7 of 7) — running day to day

- ✅ Repo structure
- ✅ Agent prompt docs (`agents/`)
- ✅ Dashboard shell — Bridge (`dashboard/index.html`)
- ✅ Stub `data.json`
- ✅ GitHub Actions stubs
- ✅ Branch A backlog/content pipeline (8-article backlog, article 1/8 drafted, awaiting CEO fact-check)
- ✅ Branch B Scout scanning + mini-site template (3 candidate niches logged, none approved yet — `dq_003`–`dq_005`)
- ✅ Branch C micro-SaaS tool built (free VoIP calculator) — not deployed, Worker/Paddle stubbed
- ✅ Allocator scoring + weekly GitHub Action wired (`scripts/allocator.py`)
- ✅ Live dashboard wiring — Bridge auto-loads `data.json` over http(s) with polling + a source/last-sync indicator; Approve/Reject on the Decision Queue is a **local preview only** and shows an on-screen banner telling the CEO to export and commit before it's real. No auto-write-back to the repo by design — matches the "no agent/dashboard action changes the repo without an explicit human commit" rule. Still blocked on Cloudflare Pages deploy (`dq_001`, needs Cloudflare account) to actually go live on a public URL.
- ✅ Handoff guide — [`docs/handoff-guide.md`](docs/handoff-guide.md) rewritten with current build status, day-to-day run steps, the dashboard's export→commit flow, and the open Decision Queue items blocking full launch.

**Skeleton phase complete. What's left is running the agents day to day and clearing the Decision Queue** — see [`docs/handoff-guide.md`](docs/handoff-guide.md).

## Structure

```
agents/                 one prompt file per agent (Scout, Writer, SEO/AEO Editor, Marketing/Social,
                         Affiliate Ops, Product/Dev, Support, Accountant, Allocator, Analyst/Reporter)
branches/
  branch-a-authority/   VoIP/telecoms/networking/ITSM authority content
  branch-b-opportunistic/  Scout-driven test niches
  branch-c-micro-saas/  VoIP calculator tool
dashboard/
  index.html            "Bridge" — single self-contained HTML dashboard, cyberpunk theme
docs/
  build-spec.md         full build spec (source of truth)
  data-schema.md        data.json schema reference
  handoff-guide.md       plain-language "how to run" guide
  branch-a-notes.md     CEO's practitioner notes go here (empty placeholder for now)
scripts/                automation scripts (not yet implemented — see scripts/README.md)
.github/workflows/      GitHub Actions stubs (allocator, pages deploy, link check)
data.json               live state the dashboard reads (revenue, branches, decision queue, activity feed)
```

## Quick start

1. Read [`docs/handoff-guide.md`](docs/handoff-guide.md) for the full human setup checklist (domain, bank, Paddle KYC, affiliate signups).
2. Open `dashboard/index.html` directly in a browser (or host it on Cloudflare Pages) to see the Bridge dashboard — it auto-loads `data.json` if served over http(s), or use the "Load data.json" button for local `file://` viewing.
3. Drop your VoIP/telecoms/ITSM practitioner notes into `docs/branch-a-notes.md`.
4. Point Claude Code at this repo and start running agents per `docs/handoff-guide.md`.

## Not

- No meaningful revenue expected week one.
- Not zero-touch — CEO triggers runs and clears the Decision Queue.
- Not a tax filer — Accountant preps summaries only.
- Never auto-sends customer replies without approval.
