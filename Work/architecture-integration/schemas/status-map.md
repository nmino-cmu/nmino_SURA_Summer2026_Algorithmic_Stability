# Status map (ART-INT)

**Authority:** ART-INT-00. Do not overload names across layers.

## Layers

| Layer | Enums | Retry? | New package version? |
|-------|-------|--------|----------------------|
| A transport | `OK` \| `FAILED` \| `EXHAUSTED` | YES if FAILED | No |
| A attempt B intake | `PENDING` \| `ACCEPTED_DRAFT` \| `REJECTED` \| `N/A` | No auto-retry on REJECTED | REJECTED may revise → new seal |
| A batch | `OPEN` \| `COMPLETED_ALL_ACCEPTED` \| `COMPLETED_MIXED` \| `COMPLETED_ALL_REJECTED` \| `ABORTED` | Partial per M-A06-BATCH | — |
| B intake | `PENDING` \| `ACCEPTED_DRAFT` \| `REJECTED` | Idempotent replay OK | Content change → new crp_digest |
| B admissibility | `ADMISSIBLE` \| `INADMISSIBLE` | — | — |
| B audit | `PASS` \| `FAIL` \| `IRRELEVANT` \| `ESCALATE_HUMAN` | No | Often new CRP after FAIL |
| B CX | `FULL` \| `PARTIAL` \| `SCOPE_LIMIT` | — | — |
| B obligation | `OPEN` \| `DISCHARGED` \| `WAIVED_HUMAN` \| `FAILED` \| `SUPERSEDED` | — | — |
| B maturity | `OPEN` \| `CONJECTURE` \| `PARTIAL_RESULT` \| `RESULT` \| `SUPERSEDED` | — | — |
| B Lean (derived) | `NOT_READY_FOR_LEAN` \| `LEAN_STATEMENT` \| `LEAN_CORE` \| `LEAN_FULL` \| `LEAN_BLOCKED` \| `LEAN_STALE` | Remanifest | Never store as writable label; recompute from `lean_manifest_digest` |
| A close_reason | ART-A-03 list incl. `completed_mixed_outcomes` | — | — |

## Crosswalk

| Event | A sees | B sees | Feedback field |
|-------|--------|--------|----------------|
| Transport fail | transport_result=FAILED | nothing | none |
| Intake accept | b_intake_result=ACCEPTED_DRAFT | ACCEPTED_DRAFT | intake_status |
| Intake reject | REJECTED | REJECTED + reason_codes | reason_codes |
| Audit pass | via export | verdict PASS | audit_verdict |
| Audit fail | via export | FAIL | audit_verdict |
| CX partial | via export | refutation_type PARTIAL | counterexamples |
| Maturity partial | via export | PARTIAL_RESULT | maturity_by_claim |
| Infra fail | transport or limitations | — | verifier_limitations |

**I-INT-ST-01:** `PARTIAL` (CX) ≠ `PARTIAL_RESULT` (maturity) ≠ missing audit PARTIAL (audit has no PARTIAL).  
**I-INT-ST-02:** `ESCALATE_HUMAN` / revision guidance → A may open revise path; not automatic B APPLY.
