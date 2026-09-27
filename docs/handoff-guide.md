# VANTAGE — How To Run (Plain Guide)

*Last updated 2026-09-27, at Build Order step 6/7 complete (dashboard wired). This is the one doc you hand to a future you, a VA, or anyone else who needs to pick this up.*

## What this is
An AI-agent-driven revenue system with three branches (Authority content, Opportunistic Scout niches, Micro-SaaS tools) and an Allocator that reweights weekly quota based on performance. You (CEO) are the trigger and the approver — nothing customer-facing, nothing that spends money, and nothing that joins a program or kills a branch happens without you saying yes in the **Decision Queue**.

## Where everything lives
```
agents/            one prompt file per agent — point Claude Code at the relevant one when you ask it to "run Scout" etc.
branches/          the three branches' content, templates, and code
dashboard/index.html   "Bridge" — the single-file dashboard, open it in any browser
scripts/           allocator.py (done), check_links.py + build_site.py (still stubs)
data.json          the live state file — Bridge reads this, agents write to it
.github/workflows/ scheduled/automated jobs (allocator runs weekly on its own)
docs/build-spec.md      the original full spec — source of truth if anything here seems off
docs/data-schema.md     what every field in data.json means
```

## Current build status (honest as of 2026-09-27)
- ✅ Branch A: 8-article backlog, article 1/8 drafted (SIP trunking), **awaiting your fact-check** before it goes through SEO/AEO editing.
- ✅ Branch B: Scout logged 3 candidate niches, all sitting in the Decision Queue unapproved (`dq_003`–`dq_005`). No cluster has been created — Scout's own read is to fold 2 of these into Branch A rather than open a new niche.
- ✅ Branch C: free VoIP calculator (bandwidth/subnet/SLA tools) is built and works locally, but is **not deployed anywhere** yet.
- ✅ Allocator: `scripts/allocator.py` scores each branch weekly and rebalances quota. Runs automatically via GitHub Actions every Monday, or manually — see below.
- ✅ Bridge dashboard: auto-loads `data.json` when hosted, polls every 5 minutes, shows where its data came from and when it last synced.
- ⬜ Nothing is publicly live yet — the domain/Cloudflare/bank/KYC setup (`dq_001`) hasn't been done, so Pages deploy is still a stub and there's no real traffic or revenue data.

## One-time human setup (do these before real revenue can start)
1. **Register the domain** (~$10–15/yr) — any registrar, point it at Cloudflare.
2. **Cloudflare account** — free — connect the domain, enable Pages + Workers + Web Analytics. Once you have `CLOUDFLARE_API_TOKEN` and `CLOUDFLARE_ACCOUNT_ID`, add them as GitHub repo secrets and uncomment the real deploy step in `.github/workflows/pages-deploy.yml`.
3. **GitHub account** — free — this repo lives here already; Actions run here (2,000 free minutes/month).
4. **Google Search Console** — free — verify the domain once Pages is live. This is what gives Scout and the Allocator real traffic numbers instead of zeros.
5. **Bank account** for payouts (Paddle/Stripe will pay out here).
6. **Paddle** (recommended over Stripe here — handles global VAT/tax automatically) — sign up, complete KYC. Real identity/business verification, no way around it. Blocks Branch C's paid tier.
7. **Affiliate programs** — Scout shortlists candidates (Awin, Impact, CJ, direct programs, Amazon Associates SA if eligible). You apply/approve each one from the Decision Queue; some need the bank/KYC info above first.

All of this is tracked as `dq_001` in the Decision Queue until it's done.

## Running the system day to day
1. Open **Claude Code** (or this same agent) pointed at this repo.
2. **Check the Decision Queue first, every time** — open `dashboard/index.html` in a browser (double-click it, or visit the hosted URL once Pages is live). Approve or reject anything waiting.
   - Approve/Reject in the dashboard is a **local preview only** — it does not touch the repo by itself (by design, so nothing changes without a human commit). When you've made decisions, click **Export Report**, replace `data.json` at the repo root with the downloaded file, then:
     ```
     git add data.json
     git commit -m "CEO: resolve decision queue"
     git push
     ```
   - The dashboard shows an amber banner whenever there's an unresolved local decision, so you can't miss this step.
3. Tell Claude Code which agent(s) to run, e.g.:
   - *"Run Scout for Branch A and Branch B, then update data.json."*
   - *"Run Writer on the next backlog item for Branch A."*
   - *"Run Allocator and Accountant, then Analyst/Reporter for this week's report."*
4. Claude Code reads the relevant `agents/*.md` prompt, does the work, writes files, commits, and pushes.
5. GitHub Actions handles the mechanical stuff on schedule (see `.github/workflows/`) — you don't need to trigger those manually. The Allocator runs every Monday at 06:00 UTC and commits its own `data.json` update.
6. To run the Allocator yourself outside its schedule:
   ```
   python3 scripts/allocator.py --dry-run   # preview only, writes nothing
   python3 scripts/allocator.py             # writes data.json in place
   ```
   Then commit/push as normal. It only reweights quota between branches that already have real traffic/revenue data — a branch with no data yet (like Branch C right now) is left untouched rather than penalized.
7. Review the weekly report (`docs/reports/weekly-<date>.md`, once Analyst/Reporter starts producing them) and clear the Decision Queue again.

## Cadence (realistic)
- **Daily**: quick Decision Queue check (2 min) — open the dashboard, approve/reject, export+commit if anything changed.
- **2–4x/week**: a real "thinking" run (Scout, Writer, or a batch of several agents) — 15–45 min of your attention, most of it is the agent working, not you typing.
- **Weekly**: Allocator (automatic) + Accountant + Analyst/Reporter cycle — mostly automatic, you just review the output.

## What never happens without you
- Joining an affiliate program (Affiliate Ops never auto-joins — written into `agents/affiliate-ops.md`)
- Sending anything to a customer/user (Support never auto-sends — written into `agents/support.md`)
- Zeroing a branch's quota or archiving it (Allocator floors quota at 1/week and never archives — enforced in `scripts/allocator.py`; a real decline only logs a `kill_recommendation` for you to act on)
- Any spend beyond the ~$10–15/yr domain and whatever free tiers you've already signed up for

## What this system will not do
- Generate meaningful revenue in week one — it's a compounding content/tooling play.
- File your taxes — Accountant preps summaries, your human accountant files.
- Run with truly zero attention — you're the trigger and the approver, always.

## Open items waiting on you right now
- `dq_001` — human-only setup (domain, bank, Paddle/Stripe KYC, Cloudflare, Search Console) — blocks everything going live and blocks real analytics data.
- `dq_002` — whether to add a freelance IT/VoIP consulting CTA to Branch A articles.
- `dq_003`–`dq_005` — three Branch B candidate niches Scout flagged; its own recommendation is to fold two into Branch A instead of opening a new Branch B cluster, but nothing proceeds without your sign-off.
- The Branch A SIP trunking draft (`branches/branch-a-authority/content/sip-trunking-setup-what-goes-wrong.md`) needs your fact-check before it goes through the SEO/AEO Editor.

## If something breaks
- `data.json` must stay valid JSON — if the dashboard shows nothing, run `python3 -c "import json; json.load(open('data.json'))"` to check for a syntax error before anything else.
- The dashboard is a single static HTML file with no build step — if it looks broken, it's almost always a JS or `data.json` issue, not a build/deploy issue.
- Every automation is a plain Python script under `scripts/` — readable, no hidden magic, safe to read before trusting.
