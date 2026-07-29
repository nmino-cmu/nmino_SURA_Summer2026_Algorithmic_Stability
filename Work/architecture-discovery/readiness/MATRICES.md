# Architecture Matrices

## Dependency graph

```mermaid
flowchart TB
  A00[ART-A-00] --> A02[ART-A-02]
  A02 --> A03[ART-A-03]
  A02 --> A04[ART-A-04]
  A03 --> A04
  A03 --> A05[ART-A-05]
  A04 --> A05
  A02 --> A06[ART-A-06]
  A03 --> A06
  A04 --> A06
  CRP[ART-CRP read-only] --> A06
  A03 --> A07[ART-A-07]
  A06 --> A07
  A00 --> A08[ART-A-08]
  A02 --> A08
  A03 --> A08
  A04e[ART-A-04e] --> A08
  A04 --> A08
  A05 --> A08
  A06 --> A08
  A07 --> A08
```

## Module → artifact ownership

See ART-A-02 §1.4 (authoritative). Amendments: SessionEvent, SessionPolicy, SubmissionAttempt, **SubmissionBatch** → DISCOVERY_ORCHESTRATOR.

## Interface matrix

| Interface | Direction | Norm |
|-----------|-----------|------|
| I.DiscoverySubmit | A→B | A-06 / ART-CRP |
| I.DiscoveryStatus | A←B | read-only |
| I.LibraryExport | A←B | read-only → VerifierPrior |
| Human Gate 1/2/3 | Human↔A | A-03 |
| Engine invocation | Orch→engines | A-05 |

## FSM transition matrix (summary)

Authoritative: ART-A-03 Mermaid + state tables. Key edges: DS05→DS04; DS07 only if ¬gate1; DS08 before DS09; DS09→DS10 iff sealable_set_nonempty; DS13 orderly; DS91 allowlist.

## A/B interaction matrix

| Action | Allowed? |
|--------|----------|
| SUBMIT_CANDIDATE_PACKAGE via I.DiscoverySubmit | Yes (sealed only) |
| LibraryExport / status / receipts import | Read-only |
| RECORD_COUNTEREXAMPLE / APPLY_PROMOTION / LOCK_CYCLE from A | No |
| Soft Attack as authoritative CX | No |
