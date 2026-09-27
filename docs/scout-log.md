# Scout Log

Dated findings from Scout runs. Every "underserved"/"low competition" claim below is cited; anything without real Search Console/keyword-tool data is marked `confidence: low` per `agents/scout.md` guardrails.

---

## 2026-09-25 — Branch B: opportunistic niche scan

No Search Console or paid keyword-tool access yet (human-only setup step, not done). This pass used general web research only — treat all niche picks as **hypotheses to validate**, not confirmed opportunities.

### Candidate 1 — SMB Cybersecurity / Network Security (adjacent to Branch A)
- **Why:** Direct skill overlap with CEO's VoIP/networking background (firewalls, Mikrotik, SLA/uptime work already covered in Branch A). Low content-production cost — same practitioner voice.
- **Affiliate angle:** NordLayer business network security affiliate program (recurring commission, cited: nordlayer.com/affiliates). HackerDNA cybersecurity affiliate roundup lists several recurring-commission programs (30% recurring cited at hackerdna.com/blog/best-cybersecurity-affiliate-programs, TryHackMe at ~5%).
- **Target keywords (unvalidated):** "smb network security checklist", "firewall setup small business", "vpn for remote teams small business"
- **Confidence:** low — no keyword volume/difficulty data, sourced from vendor affiliate pages + one blog roundup, not Search Console.
- **Test hypothesis:** 4-6 weeks, 3-4 articles reusing Branch A's practitioner-voice angle applied to network security, see if organic traffic + affiliate click-through justifies a dedicated cluster.

### Candidate 2 — Smart Home / SMB Physical Security (adjacent to CCTV/access-control notes already in `branch-a-notes.md`)
- **Why:** CEO already has Hikvision/access-control installation experience (see backlog item 6). Physical security affiliate programs pay per-sale, not just SaaS recurring — diversifies income type.
- **Affiliate angle:** Canary (canary.is/affiliates) and Frontpoint (frontpointsecurity.com/affiliate-program) both run consumer-security affiliate programs; FlexOffers aggregates several home-safety programs (flexoffers.com/affiliate-programs/home-safety-affiliate-program).
- **Target keywords (unvalidated):** "hikvision vs consumer smart camera smb", "small office access control system buying guide"
- **Confidence:** low — same caveat as above, generic aggregator sources only.
- **Test hypothesis:** Fold into Branch A backlog item 6 first (it's already an authority-niche article) rather than spin up a separate Branch B cluster yet — cheaper way to test the angle before committing a new niche.

### Candidate 3 — Remote-work IT tooling (helpdesk/ITSM for small remote teams)
- **Why:** Overlaps with Branch A backlog item 5 (SLA structuring) and item 7 (3rd-line support). Recurring SaaS affiliate commissions tend to be higher than one-off hardware sales.
- **Affiliate angle:** general SaaS/ITSM affiliate programs (not yet individually verified — needs Scout follow-up with actual program names + commission terms before this goes to `affiliate_program_review`).
- **Confidence:** low — directionally reasonable but no specific program vetted yet, do not treat as actionable.

### Recommendation to CEO
Candidates 1 and 3 are close enough to Branch A's existing expertise that they may be cheaper to test **as new sections within Branch A** rather than spinning up separate Branch B clusters (which need their own quota, review cycle, and eventual mini-site). Candidate 2 folds directly into an already-planned Branch A article.
**No Branch B cluster is recommended yet** — logged as `decision_queue` entries for CEO to review, but Scout's own read is "not enough signal to commit quota to a standalone Branch B cluster this cycle." Revisit once Search Console is live and real query data exists.

### Next Scout actions
- Get Search Console connected (human-only step) before the next niche-scan cycle — everything above is a directional hypothesis, not a keyword-validated opportunity.
- If CEO wants to proceed anyway, Candidate 1 (SMB network security) is the strongest bet given skill/content-cost overlap.
