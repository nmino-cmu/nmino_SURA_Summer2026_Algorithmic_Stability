# Integration TRACE_MATRIX (ART-INT)

**Authority:** ART-INT-00. Each trace must pass for integration ACCEPTANCE.

| ID | Scenario | Expected terminal | Owner path | Status |
|----|----------|-------------------|------------|--------|
| TR-INT-01 | Normal single-package submit Phase A | ACCEPTED_DRAFT + ≥1 PO | Seal→Submit→Commit | PASS |
| TR-INT-02 | Multiple packages in one batch | N receipts; batch COMPLETED_* | A fan-out | PASS |
| TR-INT-03 | Partial acceptance (1 OK, 1 REJECTED) | COMPLETED_MIXED; no resubmit OK | M-A06-BATCH | PASS |
| TR-INT-04 | Partial rejection only transport on one | Retry that member only | M-A06-BATCH-04 | PASS |
| TR-INT-05 | Transport retry same idempotency_key | Same logical submission | I-INT-21 | PASS |
| TR-INT-06 | Duplicate replay identical bytes | Idempotent accept; no duplicate claims | I-INT-21 | PASS |
| TR-INT-07 | Stale expected_state_head on Commit | STALE_WRITE; A may retry | ART-06b | PASS |
| TR-INT-08 | Unsupported schema_version | UNSUPPORTED_SCHEMA_VERSION / CRP_SCHEMA | I-INT-51 | PASS |
| TR-INT-09 | Phase B missing mechanism | MECHANISM_REQUIRED | I-CRP-05 | PASS |
| TR-INT-10 | Characterization candidate Phase A empty mech | ACCEPTED_DRAFT | I-CRP-02 | PASS |
| TR-INT-11 | Theorem candidate packaged | claims[] intake | profile-map | PASS |
| TR-INT-12 | Multiple verifier runs same package | Distinct verification_run_id exports | I-INT-FB-02 | PASS |
| TR-INT-13 | Feedback before session closure | DS12 VerifierPrior active | I-A03-12 | PASS |
| TR-INT-14 | Feedback after closure | New session import only | I-A03-12 | PASS |
| TR-INT-15 | Infrastructure failure | limitations INFRA_FAILURE; not math FAIL | I-INT-FB-03 | PASS |
| TR-INT-16 | Mixed batch outcome close | completed_mixed_outcomes | A-03 | PASS |
| TR-INT-17 | Duplicate identifiers different content | Different digests; no silent merge | I-INT-ID | PASS |
| TR-INT-18 | Forged receipt_ref | Prior mint rejected | I-INT-61 | PASS |
| TR-INT-19 | Schema mismatch unknown field | CRP_SCHEMA / UNKNOWN_FIELD | I-CAN-03 / ENV | PASS |
| TR-INT-20 | Unknown field telemetry `a_*` | Stripped/ignored; not fail | I-INT-ENV-01 | PASS |
| TR-INT-21 | Legacy ART-08 package | LEGACY_CYCLE_INTAKE only; new sessions refuse | I-CRP-20 / I-INT-52 | PASS |
| TR-INT-22 | Profile mismatch hint | CompileError PROFILE_MISMATCH | I-INT-PR-01 | PASS |
| TR-INT-23 | Revision cycle after REJECTED | New prior_crp_digest + Gate3 + seal | I-INT-53 | PASS |
| TR-INT-24 | Resealed after IR change | New crp_digest; old not mutated | I-INT-23 | PASS |
| TR-INT-25 | Successful completion to certified export | APPLY path B-only; A prior from export | I-CRP-10 | PASS |

**Adversarial blocks (Round 2):**

| Attack | Blocking rule |
|--------|---------------|
| Unsealed submit | I-INT-22 · A-06 Illegal |
| Change sealed after Gate3 | I-INT-23 |
| Reuse ID different content | digest identity |
| Replay changed content | I-INT-21 |
| Forge IntakeReceipt | I-INT-61 |
| Import wrong-package feedback | I-INT-63 · I-A04-PRIOR-01 |
| Mixed batch assume atomic B | I-INT-10 |
| Bypass profile | ART-CRP admissibility |
| Omit required mechanism | I-CRP-05 |
| Null/empty ambiguity | ART-21b omit-absent |
| Feedback mutates IR | I-INT-02 · I-INT-34 |
| Bypass sole write path | I-INT-01 · I-A02-08 |
| Engine calls submit/seal | I-INT-64 |
