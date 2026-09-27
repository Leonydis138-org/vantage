# VANTAGE — Build Spec (source of truth)

Owner/CEO: Juan-Louw Greyling | Sept 2026

## Ground Truth
- Not 100% unattended+free. CEO triggers thinking runs via Claude Code (existing subscription) daily then a few times a week. Mechanical tasks are free/automated.
- Domain costs ~$10–15/yr.
- Legal one-time human steps: bank account, payment KYC, affiliate signups.

## Model: 3 branches + allocator
- **A — Authority Niche:** VoIP/telecoms, networking, IT/ITSM. Seeded by Juan-Louw's practitioner notes. Affiliate hardware, hosting, VoIP, B2B SaaS.
- **B — Opportunistic:** Scout scans trends, underserved keywords, new programs. Test clusters; winners become mini-sites, losers archived (with CEO approval).
- **C — Micro-SaaS:** one useful tool (VoIP bandwidth/subnet/SLA calculator). Free host; Paddle/Stripe pro upgrade + affiliates. Low ongoing effort.
- **Allocator:** weekly scores branches, shifts quota; underperformers go to maintenance, not deleted.

## Agents
Scout, Writer, SEO/AEO Editor, Marketing/Social, Affiliate Ops, Product/Dev, Support, Accountant, Allocator, Analyst/Reporter — see `/agents/*.md` for full prompts.

## Stack (free-tier)
- Hosting: Cloudflare Pages
- Compute: GitHub Actions (2k min/mo free)
- Thinking: Claude Code, run by CEO, writes to this repo
- Storage: Markdown + `data.json` in this GitHub repo
- SaaS backend: Cloudflare Workers (100k req/day free)
- Payments: Paddle (handles global tax; KYC is human-only)
- Analytics: Google Search Console + Cloudflare Web Analytics
- Data: `data.json` (this repo) — could mirror to a Sheet later
- Social: native APIs / Buffer free tier
- Affiliates: Awin, Impact, CJ, direct SaaS programs; verify Amazon Associates South Africa eligibility

## Dashboard "Bridge"
Single self-contained HTML file (`dashboard/index.html`), cyberpunk theme, reads `data.json`.
1. Command summary: revenue week/month/all-time, trend, status
2. Branch cards: status (Active/Growing/Maintenance), traffic, clicks, conversions, revenue, quota
3. Decision queue: affiliate programs, support replies, kill recommendations
4. Activity feed: plain-language agent actions
5. Report export: weekly summary

## Allocator logic
```
score = revenue_growth_30d * 0.5 + traffic_growth_30d * 0.3 + conversion_rate * 0.2
```
Top branches get higher quota. Bottom goes to a floor (e.g. 1/month maintenance), never zero. Archiving only with explicit CEO approval. Branch B scores each test niche after 4-6 weeks: graduate or maintain.

## CEO Report
Short plain weekly summary (email via Resend, or dashboard export): revenue by source; what changed and why; agent actions; decision queue; honest outlook.

## Human-only setup
1. Register domain.
2. Bank account for payouts.
3. Paddle/Stripe KYC.
4. Apply to affiliate programs (Scout shortlists, CEO applies/approves).
5. Free accounts: GitHub, Cloudflare, Search Console.
6. Run Claude Code to trigger thinking agents; check Decision Queue before each run.
7. Human accountant reviews tax prep docs.

## Build order
1. Skeleton: repo, Actions, agent prompts, dashboard shell + stub `data.json`. ← **you are here**
2. Branch A: backlog from notes, Writer + SEO/AEO, Pages deploy.
3. Branch B: Scout scanning, reusable site template.
4. Branch C: build tool, Worker backend, Paddle checkout.
5. Allocator + ledger: scoring, `data.json` schema, weekly job.
6. Dashboard + report: live data, Decision Queue, export.
7. Handoff: plain "how to run" guide.

## Not
- No meaningful revenue expected in week one.
- Not zero human touch: CEO must trigger runs, clear the queue.
- Not tax filing.
- Never auto-send customer replies without approval.
