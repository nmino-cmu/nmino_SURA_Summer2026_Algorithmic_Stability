# Repair Blocker Ledger (Authoritative)

**Artifact ID:** `ART-RBL`  
**Normative status:** `ACTIVE_NORMATIVE`  
**Package:** `ARCH-0.3-REPAIR` · **NON-RELEASE**  
**Updated:** Package Sol gate PASS 2026-07-24; awaiting HUMAN DESIGN_FINAL (ART-25b release_digest)

A blocker closes only when its governing architecture is defined, integrated, cross-checked, and independently reviewed — not when merely scheduled.

| ID | Title | Status | Governing iteration | Notes |
|----|-------|--------|---------------------|-------|
| B-OBJ-DUAL-01 | Digest-native ART-07b vs legacy ID-native dialect | **PARTIAL** | 2–14 progressive | ACTIVE paths digest-native (ART-21b/25b); appendix prose residual OK at seal |
| B-MUTATION-KERNEL-01 | No single authoritative mutation boundary | **CLOSED** | 3 | ART-06b ITER3.2 ACTIVE |
| B-PROMO-BOOL-01 | Caller-supplied promotion predicates | **CLOSED** | 3, 5 | ART-13b ITER5.7 ACTIVE |
| B-HARDSTOP-FENCE-01 | Hard-stop not linearizable fence | **CLOSED** | 3, 10 | ART-06b commit fence + ART-17b restore |
| B-IDENTITY-01 | Unauthenticated identity/independence | **CLOSED** | 4 | ART-04c ITER4.6 ACTIVE |
| B-AUDIT-BIND-01 | Audits unbound to immutable intent/evidence | **CLOSED** | 6 | ART-11b ITER6.20 ACTIVE |
| B-STATUS-COUPLE-01 | Research maturity can exceed proof floor | **CLOSED** | 2, 4, 5 | CERTIFY + RESULT APPLY couple |
| B-BRIDGE-PROOF-01 | Unproved bridge fills inference slot | **PARTIAL** | 2, 4 | CERTIFY reachable; residual dual dialect |
| B-DEMOTION-WAVE-01 | Demotion not durable/crash-resumable | **CLOSED** | 7 | ART-16b ITER7.9 ACTIVE (Sol deferred) |
| B-RECOVERY-PREFIX-01 | Checkpoint accepts incomplete prefix | **CLOSED** | 10 | ART-17b ITER10.2 ACTIVE (Sol deferred) |
| B-LEAN-CLOSURE-01 | Lean not Claim/closure-bound | **CLOSED** | 8 | ART-10b ITER8.9 ACTIVE |
| B-RELEASE-FALSEPASS-01 | Historical PASS implies readiness | **CLOSED** | 14 | ART-25b I-REL-11; Sol package gate PASS 2026-07-24 |
| B-RELEASE-IDENTITY-01 | No immutable release identity | **CLOSED** | 14 | ART-25b ITER14.1; Sol package gate PASS 2026-07-24 |

## Breaker evidence

- `adversarial_review_artifacts/INDEPENDENT_BREAKER_AUDIT_2026-07-23.md` — **not** a final audit; evidence only.
- Prior: `INDEPENDENT_BREAKER_AUDIT.md`
