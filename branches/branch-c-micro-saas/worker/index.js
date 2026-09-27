/**
 * VANTAGE Branch C — Micro-SaaS Worker backend (stub)
 *
 * Free tier (Cloudflare Workers, 100k req/day): all calculator logic runs
 * client-side in frontend/index.html — this Worker is NOT required for the
 * free calculator to work. It exists for future Pro-tier features:
 *   - Paddle/Stripe webhook receiver (unlocks Pro after payment)
 *   - Saved calculations (needs KV or D1 storage — not provisioned yet)
 *   - Usage analytics beyond Cloudflare Web Analytics
 *
 * STATUS: not deployed. Deploy only after Paddle/Stripe KYC is complete
 * (human-only step, see docs/build-spec.md → "Human-only setup").
 *
 * Nothing in this file executes real payment logic yet — it is a routing
 * skeleton so Product/Dev doesn't have to design this from scratch later.
 */

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);

    if (url.pathname === "/health") {
      return Response.json({ status: "ok", service: "vantage-branch-c-worker" });
    }

    // TODO (post-KYC): verify Paddle webhook signature, mark subscription
    // active, and unlock Pro features for the paying customer's session.
    if (url.pathname === "/webhooks/paddle") {
      return new Response("Not implemented — Paddle KYC not complete yet.", { status: 501 });
    }

    // TODO: saved-calculation storage (needs Cloudflare KV or D1 binding
    // added to wrangler config once Pro tier feature list is confirmed
    // with CEO — see branches/branch-c-micro-saas/README.md).
    if (url.pathname === "/api/save") {
      return new Response("Not implemented — Pro tier not built yet.", { status: 501 });
    }

    return new Response("VANTAGE Branch C Worker — see /health", { status: 200 });
  },
};
