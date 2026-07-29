# Integration AUDIT_LOG

**Started:** 2026-07-25  
**Method:** Adversarial integration audit + self-repair  
**Prior A/B PASSes:** non-evidence

## Assumptions (locked)

1. `sealed_digest ≡ crp_digest`  
2. `SubmissionBatch` is A-only; B stores no `batch_id`  
3. `I.DiscoverySubmit` builds one SUBMIT per sealed package  
4. Feedback export is read-only; Orch mints VerifierPrior  
5. Interface math notation applies to CRP / PO / FeedbackExport only  

## BLOCKING-0

| ID | Defect | Repair | Status |
|----|--------|--------|--------|
| B0 | No authoritative integration specification | Created `architecture-integration/00-A-B-INTEGRATION.md` + schemas | **CLOSED** |

## Round findings → repairs

| Sev | ID | Defect | Repair | Status |
|-----|----|--------|--------|--------|
| BLOCKING | B1 | No integration owner | ART-INT-00 | CLOSED |
| BLOCKING | B2 | Missing DraftCRP/SealedCRPSnapshot schemas; seal↔CRP envelope | ART-INT crp-wire + A-04 S-A04-DRAFT/SEAL + A-06 | CLOSED |
| BLOCKING | B3 | No VerifierFeedbackExport | ART-INT feedback-export + ART-24 | CLOSED |
| MAJOR | M1 | Batch vs per-package | ART-INT §2; A-06 M-A06-BATCH-09; ART-CRP I-CRP-12 | CLOSED |
| MAJOR | M2 | Digest/idempotency underspecified | I-INT-20/21; ART-CRP I-CRP-11 | CLOSED |
| MAJOR | M3 | profile_hint ambiguity | ART-INT profile-map; A-06 pointer | CLOSED |
| MAJOR | M4 | Status crosswalk missing | ART-INT status-map | CLOSED |
| MAJOR | M5 | A not bound to ART21b wire | ART-INT I-INT-40; A-06 I-A06-08 | CLOSED |
| MAJOR | M6 | perturbation_mechanism_id vs mechanism_proposals | ART-INT crp-wire + field-map | CLOSED |
| MAJOR | M7 | Engine stub submit/seal contradiction | ART-A-NOV / ART-A-ATP prohibited lists | CLOSED |
| MAJOR | M8 | Roster vs module naming | A-04e I-A04e-04 aliases | CLOSED |
| MINOR | m1 | transport_result ellipsis | A-03 `OK\|FAILED\|EXHAUSTED` | CLOSED |
| EDITORIAL | e1 | Legacy ART-08 verifier prose | Deferred (non-authoritative) | OPEN (editorial) |
| EDITORIAL | e2 | Thin OBLIGATION_ONLY fixtures | Deferred | OPEN (editorial) |

## Audit rounds

| Round | Focus | Result |
|-------|-------|--------|
| 1 Structural | Missing owner/schemas | FAIL → repaired |
| 2 Authority | Dual ownership / engine stubs | FAIL → repaired |
| 3 Schema | Draft/Seal/Envelope/Feedback | PASS after ART-INT |
| 4 Identifier | batch_id / sealed_digest | PASS |
| 5 Serialization | ART21b bind | PASS |
| 6 Submission | Fan-out + idempotency | PASS |
| 7 Feedback | Export object | PASS |
| 8 Notation | Shared table | PASS |
| 9 Traces | TR-INT-01…25 | PASS (design-level) |
| 10 Cross-doc | References to ART-INT | PASS |
| 11 Self-repair | Amendments logged | PASS |
| 12 Re-audit | Zero BLOCKING/MAJOR | **PASS** |

## Files modified

See FINAL_AUDIT.md.
