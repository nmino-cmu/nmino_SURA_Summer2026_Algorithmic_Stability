# ART-A-07 — Persistence, Replay, Recovery, and Migration (System A)

**Artifact ID:** `ART-A-07`  
**Version:** `ARCH-0.3-REPAIR-DUAL.2`  
**Normative status:** `FROZEN`  
**Frozen:** `2026-07-25` (re-audited `2026-07-25b`)  
**Owner:** Research Discovery Assistant (ART-01D)  
**Depends on:** ART-A-02 · ART-A-03 · ART-A-04 · ART-A-05 · ART-A-06  
**Does not modify:** DS13 reopen ban; active prior-into-closed ban

## Purpose

Durable session store, control replay, crash recovery, late-feedback import, ART-08 migration.

## Non-goals

- Reopen DS13→DS12 · active VerifierPrior into CLOSED · B checkpoint design

## Principles

**I-A07-01** IR + SessionEvent durable for audit after close.  
**I-A07-02** Control replay from events + slice completions + cited version_ids.  
**I-A07-03** Late feedback = A-03 I-A03-12 + A-04 S-A04-PRIOR.  
**I-A07-04** A-03 supersedes ART-08 for new sessions.

## Persistence

Durable: ArtifactVersion, lifecycle, Branch, DepLink, SessionEvent, SessionPolicy, SubmissionBatch, SubmissionAttempt, GateRecord, portfolio/draft/seal artifacts.

## Replay

1. Replay SessionEvents in order.  
2. Validate slice completion version_ids exist.  
3. Recompute barrier digests; mismatch → integrity failure (DS91 if unrecoverable).  
4. Do not require regenerating engine math.

## Recovery rules

| ID | Case | Action |
|----|------|--------|
| R-A07-01 | Crash mid-slice (DS03/DS05) | Abort slice ABORTED; restart slice or refine |
| R-A07-02 | Crash mid-Gate | Remain in gate; regenerate GateRequest from IR |
| R-A07-03 | Crash during DS08 compile | Re-run compile for incomplete members only; no invention; barrier before DS09 |
| R-A07-04 | Crash after submit dispatch before receipt persist | Resume via SubmissionAttempt idempotency (A-06); do not double-accept |
| R-A07-05 | Crash mid-batch with some accepts | On resume skip ACCEPTED_DRAFT members (M-A06-BATCH-04) |
| R-A07-06 | Corrupted log | DS91 if unrecoverable |

## Late feedback / archival

As A-03 §11.2; provenance fields A-04 S-A04-PRIOR.

## ART-08 migration

| Legacy | New |
|--------|-----|
| ART-08 S00–S16 mix | A-03 DS* + B post-intake |
| ART-08b | DS02 + ART-08b |
| ART-08c cards | A-02 owners → A-06 |
| S09 CX | Soft Attack A-local; B owns authoritative CX |

## Illegal

DS13→DS12; active prior into CLOSED; delete SessionEvent history; treat feedback as certification.

## Changelog

2026-07-25: Initial.  
2026-07-25b: R-A07-03/04/05 crash cases; batch-aware resume.
