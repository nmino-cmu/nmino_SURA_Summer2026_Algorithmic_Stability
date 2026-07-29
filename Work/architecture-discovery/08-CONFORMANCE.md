# ART-A-08 — Conformance (System A)

**Artifact ID:** `ART-A-08`  
**Version:** `ARCH-0.3-REPAIR-DUAL.2`  
**Normative status:** `FROZEN`  
**Frozen:** `2026-07-25` (re-audited `2026-07-25b`)  
**Owner:** Research Discovery Assistant (ART-01D)  
**Depends on:** ART-A-00 · A-02 · A-03 · A-04 · A-04e · A-05 · A-06 · A-07 · ART-CRP  
**Does not modify:** Other normative prose

## Purpose

**Formally enumerated** conformance cases mapped to stable rule IDs. Not a machine-readable manifest unless separately published.

## Non-goals

- Duplicate FSM prose · B ART-21b · invent rules absent from A-00…A-07

## Case catalog (C-A08 / CF-A aliases)

### Ownership / IR

| ID | Requirement | Rule refs |
|----|-------------|-----------|
| CF-A-OWN-01 | One owner per class | A-02 I-A02-01 |
| CF-A-OWN-02 | Non-owner cannot mint foreign | A-02 I-A02-01/03 |
| CF-A-IMM-01 | Payload immutable | A-02 I-A02-10; S-A04-AV |
| CF-A-COH-01 | Coherence false ⇒ CompileError | P-A04-COH-*; I-A06-01 |
| CF-A-PAR-01 | Distinctness / Pareto predicates | P-A04-DISTINCT-01; P-A04-PARETO-01 |

### FSM / gates

| ID | Requirement | Rule refs |
|----|-------------|-----------|
| CF-A-FSM-01 | Only Orch commits transitions | I-A03-02 |
| CF-A-G1-01 | DS05→DS04 when gate1_required | I-A03-08 |
| CF-A-G1-02 | No DS07 while gate1_required | I-A03-08 |
| CF-A-G3-01 | Incomplete waiver stays DS09 | I-A03-09 |
| CF-A-G3-02 | seal_set = DraftCRP.version_id[]; no CompileError | P-A04-SEAL-01; I-A03-09 |
| CF-A-ORD-01 | Pack before Gate 3 | I-A02-11; I-A06-02 |
| CF-A-GATE-01 | GateRequest/Decision schemas | S-A04-GATE-REQ/DEC |

### Slice / concurrency

| ID | Requirement | Rule refs |
|----|-------------|-----------|
| CF-A-SLC-01 | Parallel only in slice | I-A03-06; P-A05-PAR |
| CF-A-SLC-02 | No cross-read without depends_on | P-A05-PAR-02 |
| CF-A-SLC-03 | Predicates after barrier | I-A03-13; A-03 §9.1 |

### Submit / feedback

| ID | Requirement | Rule refs |
|----|-------------|-----------|
| CF-A-SUB-01 | Submit sealed seal_set only | I-A06-03/04 |
| CF-A-SUB-02 | Idempotent retry; no new Draft/Seal/Gate3 | I-A03-10; M-A06-BATCH |
| CF-A-SUB-03 | Transport ≠ B reject | M-A06-BATCH-05 |
| CF-A-SUB-04 | Batch partial success; skip accepted on retry | M-A06-BATCH-03/04 |
| CF-A-SUB-05 | SubmissionBatch identity required | S-A04-BATCH; A-03 DS11 |
| CF-A-FB-01 | No active prior into closed session | I-A04-PRIOR-02; I-A03-12 |
| CF-A-FB-02 | DS13 never reopens | I-A03-12 |
| CF-A-FB-03 | Active prior cites sealed_digest and/or receipt_ref | I-A04-PRIOR-01 |

### Closure / DS91

| ID | Requirement | Rule refs |
|----|-------------|-----------|
| CF-A-91-01 | Empty frontier not DS91 | A-03 DS91 allowlist |
| CF-A-13-01 | SessionClosed.close_reason required | A-03 DS13 |
| CF-A-13-02 | Mixed batch → completed_mixed_outcomes | A-03 close_reason |

### A/B

| ID | Requirement | Rule refs |
|----|-------------|-----------|
| CF-A-B-01 | Sole mutation path | I-A06-04; A-00 |
| CF-A-B-02 | Soft Attack ≠ RECORD_COUNTEREXAMPLE | I-A02-07; I-A05 |

## Trace scenarios (TR-A-01…20)

| ID | Scenario | Primary refs |
|----|----------|--------------|
| TR-A-01 | Normal one package accepted | A-03 happy path; A-06 |
| TR-A-02 | Gate 1 scope revision | DS05→DS04; new ScopeBinding |
| TR-A-03 | Gate 2 novelty quarantine | DS06 |
| TR-A-04 | Partial compile failure | DS08; CompileError visible |
| TR-A-05 | All compiles fail then repair | DS08→DS05→DS07→DS08 |
| TR-A-06 | Gate 3 portfolio revision | DS09→DS07→DS08→DS09 |
| TR-A-07 | Gate 3 discovery revision | DS09→DS05→… |
| TR-A-08 | Gate 3 waiver + explicit seal_set | I-A03-09 |
| TR-A-09 | Soft Attack kills one branch; other survives | DS05 branch-split |
| TR-A-10 | No viable branch | DS13/DS90 not DS91 |
| TR-A-11 | Multiple drafts all accepted | SubmissionBatch |
| TR-A-12 | Multiple drafts mixed intake | completed_mixed_outcomes |
| TR-A-13 | Transport retry; skip accepted | M-A06-BATCH-04; R-A07-05 |
| TR-A-14 | B intake rejection | attempt REJECTED |
| TR-A-15 | Feedback before close | DS12 + S-A04-PRIOR |
| TR-A-16 | Feedback after close | new session / archival |
| TR-A-17 | Cancellation DS90 | DS90 |
| TR-A-18 | Illegal forced transition | TransitionRejected |
| TR-A-19 | Crash during DS08 | R-A07-03 |
| TR-A-20 | Crash after dispatch before receipt persist | R-A07-04 |

## Pass criterion

Claim conformance only if all CF-A-* and TR-A-01…20 are demonstrated against cited rule IDs.

## Changelog

2026-07-25: Initial (14 traces).  
2026-07-25b: Rule-ID mappings; traces 01–20; batch/prior/Pareto cases; formally enumerated (not machine manifest).
