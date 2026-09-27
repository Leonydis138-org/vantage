# Branch C — Micro-SaaS

First tool: VoIP bandwidth / subnet / SLA calculator. Free to use, Paddle/Stripe-gated Pro upgrade, plus affiliate placements for relevant hardware/hosting.

## Status
`Maintenance` — free-tier calculator built (2026-09-25), not deployed yet. Worker backend is a stub (returns 501 on Pro-tier routes) pending Paddle/Stripe KYC.

## Structure
```
frontend/index.html   VoIP Bandwidth + Subnet/CIDR + SLA calculator (single static file, no build step, no login)
worker/index.js        Cloudflare Worker stub — /health only; Pro-tier routes return 501 until KYC + feature list confirmed
worker/wrangler.toml   Worker deploy config (not yet deployed)
README.md              this file
```

## What's built vs. not
- Free calculator: bandwidth (codec/ptime/overhead-aware), subnet/CIDR, SLA uptime — all client-side JS, deployable today as a static page.
- Affiliate placeholder slot (`{{AFFILIATE:networking-hardware}}`) wired into the page, not yet pointing at a real program.
- Not deployed to Cloudflare Pages yet (needs Cloudflare account connected — human-only step).
- Pro tier (saved calculations, PDF export, bulk mode) — feature list still TBD with CEO, Worker routes are 501 stubs.
- Paddle/Stripe checkout — blocked on KYC (human-only step, tracked in `data.json` → `decision_queue` `dq_001`).

## Planned free vs. pro split
- **Free:** full calculator functionality, no login.
- **Pro (Paddle/Stripe):** saved calculations, PDF export, bulk/batch mode — final list TBD with CEO.

## Dependencies
- Paddle/Stripe KYC completed (human-only step).
- Cloudflare Worker route configured.
