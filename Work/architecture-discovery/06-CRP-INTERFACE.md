# ART-A-06 — CRP Projection, Seal, and Submit Interface (System A)

**Artifact ID:** `ART-A-06`  
**Version:** `ARCH-0.3-REPAIR-DUAL.2`  
**Normative status:** `FROZEN`  
**Frozen:** `2026-07-25` (re-audited `2026-07-25b`)  
**Owner:** Research Discovery Assistant (ART-01D)  
**Depends on:** ART-A-02 · ART-A-03 · ART-A-04 · ART-CRP (read-only) · ART-INT-00 (wire/envelope/batch cardinality)  
**Does not modify:** ART-CRP fields; Verification Architecture; FSM transition table

## Purpose

Deterministic IR→DraftCRP projection; seal-set consumption; **SubmissionBatch** / partial-success / idempotent retry contracts (A-local). Cross-system seal envelope, wire canon, feedback, and B fan-out: **ART-INT-00**.

## Non-goals

- Alter ART-CRP · invent IR at pack time · B DeriveEffects · redefine Gate 3 authorization timing (A-03) · redefine VerifierFeedbackExport (ART-INT)

## Principles

**I-A06-01** Packager purity (A-02 I-A02-06).  
**I-A06-02** Compile all Gate-3 candidates before Gate 3 (A-02 I-A02-11).  
**I-A06-03** Seal only GateRecord.seal_set DraftCRP.version_ids (authorization: A-03).  
**I-A06-04** Sole B mutation: SealedCRPSnapshot → I.DiscoverySubmit → SUBMIT_CANDIDATE_PACKAGE.  
**I-A06-05** This section is authoritative for **A-local** projection maps, batch identity, partial outcomes, and retry-without-resubmit-accepted.  
**I-A06-06** Seal envelope / SubmissionEnvelope / `sealed_digest≡crp_digest`: ART-INT crp-wire.  
**I-A06-07** `profile_hint` normalization: ART-INT profile-map.  
**I-A06-08** Wire serialization: ART-21b via ART-INT I-INT-40.

## M-A06-PROJ — Projection table

| CRP payload field | IR sources |
|-------------------|------------|
| definitions[] | DefinitionDraft |
| assumptions[] | AssumptionDraft |
| claims[] | TheoremCandidate, ConjectureCandidate |
| proof_sketches[] | ProofSketch |
| bridge_proposals[] | BridgeProposalDraft |
| mechanism_proposals[] | MechanismProposal (iff ART-CRP profile requires) |
| examples[] | ExampleCard |
| falsifiers[] | FalsificationTarget, SoftFalsifierDraft (drafts) |
| counterexample_claims[] | Soft-attack drafts only |
| certificate_drafts[] | CertificateDraft |
| literature_refs[] | LiteratureNode / NoveltyAssessment |
| declared_reads[] | VerifierPrior / library digests |
| free_text_notes? | optional |

Profile: PortfolioMember.profile_hint → CRP profile per ART-INT profile-map. No mechanism invention from operators alone (ART-CRP I-CRP-03).  
ExampleCard.`perturbation_mechanism_id` → `mechanism_proposals[]` alias per ART-INT crp-wire (not a B field).

## Compile

`compile(branch_id) → DraftCRP | CompileError` requiring P-A04-COH-*. Missing content ⇒ CompileError. Payload shape: ART-INT S-INT-DRAFT.

## Seal input contract

Authorized `seal_set` from Gate 3 (A-03). Assistant seals exactly those DraftCRP.version_ids (P-A04-SEAL-01) into S-INT-SEAL / SubmissionEnvelope (ART-INT).

## M-A06-BATCH — Submit batch & partial outcomes

| ID | Rule |
|----|------|
| **M-A06-BATCH-01** | One `SubmissionBatch` per Gate-3 seal wave (schema S-A04-BATCH). |
| **M-A06-BATCH-02** | One `logical_submission_id` / `idempotency_key` per sealed digest (`=` `crp_digest`). |
| **M-A06-BATCH-03** | **Partial success:** batch may contain mix of ACCEPTED_DRAFT and REJECTED / transport_exhausted. |
| **M-A06-BATCH-04** | **Retry:** reuse keys; **do not** resubmit members already ACCEPTED_DRAFT; only retry FAILED transport (or policy-allowed) pending members. |
| **M-A06-BATCH-05** | Transport failure ≠ B intake rejection; B REJECTED is not auto-retried as success. |
| **M-A06-BATCH-06** | Material IR change ⇒ new draft → new Gate 3 → new seal → new logical ids (new batch or new membership). |
| **M-A06-BATCH-07** | Session close with mixed outcomes uses A-03 `completed_mixed_outcomes`. |
| **M-A06-BATCH-08** | Events: Submitted / SubmitRejected / SubmitTransportFailed / SubmitIdempotentReplay per attempt. |
| **M-A06-BATCH-09** | B has no `batch_id`; fan-out = N independent `SUBMIT_CANDIDATE_PACKAGE` (ART-INT I-INT-10). |

## Illegal

Pack stale tips without recompile; seal CompileError; submit unsealed; submit outside seal_set; resubmit accepted member during partial retry; Gate3-less reseal after IR change.

## Failures

CompileError; PACKAGE_INADMISSIBLE/REJECTED on attempt; transport failure retried per M-A06-BATCH-04.

## Changelog

2026-07-25: Initial.  
2026-07-25b: SubmissionBatch, partial success, no-resubmit-accepted, M-A06-* IDs.  
2026-07-25c: Consistency amendment — defer wire/envelope/profile/mechanism alias to ART-INT; M-A06-BATCH-09.
