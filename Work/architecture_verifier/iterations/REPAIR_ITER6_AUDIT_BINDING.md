# Repair Iteration 6 — Audit Policy and Intent Binding

**ART-11b version:** `ARCH-0.3-REPAIR-ITER6.20`  
**Normative status:** `ACTIVE_NORMATIVE`  
**Normative draft:** [../11-integration-audit/AUDIT_BINDING.md](../11-integration-audit/AUDIT_BINDING.md)  
**Depends on:** ART-07b · ART-07c · ART-06b · ART-04c · ART-13b · ART-01  
**Package:** `ARCH-0.3-REPAIR` · **NON-RELEASE**

## A. Executive summary

Intent-bound AuditRecord + DisconfirmLog; RECORD_AUDIT carries promotion_intent; major non-noop APPLY requires latest AuditRecord for intent to be PASS and fresh (EvidenceClosure Claim digests + live I-CX-01 at APPLY); later FAIL supersedes PASS; attestation ponytail for non-machine Qs.

## B–C. Addressed / deferred

Addressed: B-AUDIT-BIND-01 (intent bind; superseding FAIL; CX evidence freshness; BRIDGE in closure; live CX re-check).  
Deferred: omitted Qs → 7/9/11; demotion (7); Lean (8); FSM (9); restore (10); release (14).

## Q. Migration matrix

ART-11b → ACTIVE_NORMATIVE. ART-11 remains PENDING_MIGRATION (descriptive). Consumers ART-03/16/17 warned; 11b wins.

## U. Independent review findings

| Review | Status | Evidence |
|--------|--------|----------|
| Combined Sol A–D | **PASS** | `adversarial_review_artifacts/REPAIR_ITER6.20_REVIEW_combined.txt` |

Prior waves ITER6.0–6.19 FAIL archived. No open Critical/High on ITER6.20.

## W. Blocker ledger update

B-AUDIT-BIND-01 **CLOSED**. B-DEMOTION-WAVE-01 remains **OPEN** (Iter7).

## X. Iteration 6 completion decision

**YES — COMPLETE.** ART-11b `ARCH-0.3-REPAIR-ITER6.20` is `ACTIVE_NORMATIVE`.

## Y. Authorization to begin Iteration 7

**AUTHORIZED.** Package **NON-RELEASE**; `IMPLEMENTATION_BLOCK` ACTIVE; blueprint / implementation planning still **no**.

## Draft history (abbrev)

6.15–6.20: EvidenceClosure Claim-only + PE.claim_digest/lemmas + BRIDGE + live CX@APPLY.
