---
title: "SIP Trunking Setup: What Actually Goes Wrong (And How to Fix It)"
meta_description: "A VoIP network engineer's honest breakdown of the SIP trunking failures that actually show up in support calls — one-way audio, registration drops, NAT issues — and how to fix each one."
target_keyword: "sip trunking setup guide"
branch: "branch_a"
cluster_id: null
word_count: 1450
status: "needs-review"
author_note: "Drafted from docs/branch-a-notes.md — CEO to fact-check before ready-to-publish."
---

# SIP Trunking Setup: What Actually Goes Wrong (And How to Fix It)

Most SIP trunking guides read like they were written by someone who's never actually been on a support call at 8am because a client's phones stopped ringing. I have. Between working SIP trunk support at Wavenet, running 3rd line support for network and telecoms systems, and years before that touching PBX systems from Panasonic to NEC, the "textbook" SIP setup and the "what actually breaks" SIP setup are two different documents. This is the second one.

If you're setting up SIP trunking for the first time — or troubleshooting one that's already misbehaving — here's what actually goes wrong, in the order I've seen it go wrong most often.

## 1. One-way or no-way audio (the classic)

This is the single most common SIP trunk complaint I've fielded. The call connects, you can see it's "active" on both ends, and one side — or both — hears nothing.

**What's actually happening:** almost always a NAT traversal problem. SIP separates signaling (the call setup, over SIP itself) from media (the actual audio, over RTP). Your firewall or router can happily let the SIP signaling through and still block or mishandle the RTP media stream, because it's a separate connection with its own port range.

**What to check first:**
- Is your router doing SIP ALG (Application Layer Gateway)? Turn it off. SIP ALG has a well-earned reputation for "helpfully" rewriting SIP headers in ways that break more than they fix. I've lost count of how many one-way audio tickets got resolved by disabling SIP ALG on a consumer-grade or SMB router.
- Confirm your RTP port range (commonly something like 10000–20000, but check your PBX/provider docs) is actually open and forwarded, not just the SIP signaling port (5060/5061).
- If you're behind a NAT and not using a session border controller (SBC), check whether your PBX supports and is configured for STUN, or whether the provider needs you to set an explicit external IP for SIP rewriting.

## 2. Trunk registration drops randomly

Everything works for a few hours or days, then the trunk just... stops registering. No obvious trigger.

**What's actually happening:** this is very often a keepalive/timeout mismatch between your firewall's connection tracking timeout and your SIP registration interval. Your firewall silently drops the "idle" UDP session before the next registration refresh, the provider stops seeing you as registered, and inbound calls start failing until the next registration cycle kicks in (or doesn't).

**What to check first:**
- Compare your firewall's UDP session timeout against your SIP client's registration expiry/re-register interval. If the firewall timeout is shorter, you'll get exactly this symptom.
- Where possible, switch the trunk to TCP or TLS instead of UDP — TCP connections are generally tracked more reliably by firewalls and NAT devices, and TLS gets you encryption as a bonus.
- If you're on a carrier-side static IP trunk (no registration), confirm nothing changed on your public IP — a surprising number of "random" registration failures I've chased down turned out to be a dynamic IP that quietly rotated.

## 3. Choppy audio / jitter under load

Calls are fine one at a time, but the moment there are 4-5 concurrent calls, audio starts breaking up.

**What's actually happening:** bandwidth or QoS, almost every time. VoIP is not bandwidth-hungry per call, but it is extremely latency- and jitter-sensitive. If your WAN link is being saturated by anything else — backups, large file transfers, video calls on other systems — voice packets get delayed or dropped even if there's technically "enough" bandwidth on paper.

**What to check first:**
- Do the actual math: each concurrent call using G.711 needs roughly 80-100kbps with overhead; G.729 needs less (~30-40kbps) but costs you audio quality. Multiply by your realistic concurrent call count and compare against your actual available upload bandwidth, not the number on the ISP's marketing page.
- Set up QoS/traffic shaping on your router to prioritize SIP and RTP traffic ahead of everything else. This alone fixes a large chunk of "it's fine until someone starts a backup" tickets.
- If you're on a shared/contended business connection, this is where a proper SLA with guaranteed bandwidth (not just "up to X Mbps") actually matters — see the section below on carrier SLAs.

## 4. Caller ID or outbound number showing wrong (or "Unknown")

Calls connect fine, but the number showing on the other end is wrong, blank, or flagged as spam.

**What's actually happening:** usually a mismatch between the "From" header your PBX is sending and what the carrier expects, or a STIR/SHAKEN attestation issue if you're dealing with a carrier in a market enforcing caller ID authentication. This has gotten more common, not less, over the last few years as carriers tightened up spam/robocall enforcement.

**What to check first:**
- Confirm the outbound caller ID number set in your PBX exactly matches a number actually provisioned and verified on the trunk with your carrier — not just "a number that used to work."
- Ask your carrier directly whether they're enforcing STIR/SHAKEN attestation and what's needed on your end to get full (A-level) attestation instead of partial.
- If multiple extensions present different caller IDs, confirm each one is individually authorized on the trunk — some carriers require this explicitly, others don't, and assuming the wrong one is a common setup mistake.

## 5. It worked in testing, broke in production

The trunk passed every test call cleanly. Then real call volume hit and things started failing.

**What's actually happening:** test calls almost never replicate real concurrency, real network contention, or real failover conditions. This is the gap between "the trunk works" and "the trunk works under load," and it's the reason I don't consider a SIP trunk deployment done until it's survived a real business day, not a test call.

**What to check first:**
- Load-test with actual expected concurrent call counts before go-live, not just one or two test calls.
- Confirm failover behavior explicitly — if your primary SIP trunk connection drops, does the PBX actually fail over to a backup trunk/route, or does it just... stop? I've seen failover configured but never actually tested, which is functionally the same as not having it.
- Document the SLA you were promised versus what you're actually seeing, from day one — not after the third outage. This is the single biggest thing I'd tell anyone signing a new VoIP carrier contract: get the SLA in writing, and actually track uptime against it.

## The pattern, if you're in a hurry

Almost every SIP trunk problem I've been called in on falls into one of these buckets: **NAT/firewall misconfiguration**, **bandwidth/QoS under real load**, or **a mismatch between what was tested and what production actually looks like**. If you're troubleshooting a live issue, check those three first — you'll close most tickets before you even get to the exotic stuff.

If you're setting up a new trunk, build in the check for all three before go-live, not after the first angry call.

{{AFFILIATE:sip_gateway_hardware}}

{{AFFILIATE:voip_carrier_sa}}
