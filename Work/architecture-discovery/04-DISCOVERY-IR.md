# ART-A-04 — Discovery IR Schemas (System A)

**Artifact ID:** `ART-A-04`  
**Version:** `ARCH-0.3-REPAIR-DUAL.2`  
**Normative status:** `FROZEN`  
**Frozen:** `2026-07-25` (re-audited `2026-07-25b`)  
**Owner:** Research Discovery Assistant (ART-01D)  
**Depends on:** ART-A-00 · ART-A-02 (ownership) · ART-A-03 (lifecycle timing refs) · ART-INT-00 (boundary schemas, read-only)  
**Does not modify:** Ownership table in ART-A-02; ART-CRP; Verification Architecture

## Purpose

Field-level schemas and checkable predicates for Discovery IR and workflow payloads.

## Non-goals

- Reassign class owners · invent engines · redefine CRP · redefine FSM transitions · redefine A↔B wire (ART-INT-00)

## Principles

**I-A04-01** Schemas refine ART-A-02; conflict → ART-A-02 wins on ownership, this doc on field shape.  
**I-A04-02** Payload immutability / lifecycle split = ART-A-02 I-A02-10.  
**I-A04-03** Package coherence = ART-A-02 §1.3.1 (predicates `P-A04-COH-*`).  
**I-A04-04** Precedence: this section owns **A-local field schemas and IR/portfolio predicates**; A-03 owns FSM; A-05 owns invocation execution; A-06 owns projection/submit batch rules; **ART-INT-00 owns cross-system wire/feedback**.

## Schemas

### S-A04-AV — ArtifactVersion

```text
lineage_id, version_id, artifact_class, session_id, owner_module, created_at, parents[], payload
```

### S-A04-LC — ArtifactLifecycleRecord

```text
lifecycle_record_id, subject_kind, subject_id, state, at, cause_ref?, prev_lifecycle_record_id?
```

### S-A04-BR — Branch / S-A04-DL — DepLink

As ART-A-02 structural records (tip_pins[], link_kind enum).

### S-A04-EV — SessionEvent

```text
event_id, session_id, event_kind, at, payload  # no mathematical claim bodies
```

### S-A04-SLICE — DiscoverySlice payload

Shape cited by ART-A-03; **execution fields** interpreted by ART-A-05. Not a taxonomy class.

### S-A04-POLICY — SessionPolicy (SessionPolicyProfile)

```text
policy_version_id
session_id
approved_before_gate3: bool
gate3_waiver_seal_resolver?: enum(HUMAN_ONLY | DETERMINISTIC_PROFILE)
deterministic_seal_rule?: structured  # only if DETERMINISTIC_PROFILE; must yield DraftCRP.version_id[]
allow_same_session_continue_after_ds12: bool  # default false
unrecoverable_transport_to_ds91: bool
created_at
```

Owner: DISCOVERY_ORCHESTRATOR (ART-A-02).

### S-A04-GATE-REQ — GateRequest (packet to human)

```text
request_id, session_id, gate_number: 1|2|3
inputs_digest
scope_binding_version_id?
proposed_scope_change?
novelty_assessment_refs[]?
portfolio_frontier_id?
draft_crp_version_ids[]?
compile_error_ids[]?
session_policy_ref?
```

### S-A04-GATE-DEC — GateRecord / decision

```text
gate_id, gate_number, request_id?
decision: approve|revise|reject|defer|waive|skipped
seal_set?: DraftCRP.version_id[]   # Gate 3 complete only; successful drafts only
session_policy_ref?: version_id
rationale?
at
```

### S-A04-BATCH — SubmissionBatch / S-A04-ATT — SubmissionAttempt

Field lists as ART-A-03 §11.1; normative A-local batch behavior ART-A-06. Cross-system fan-out / B cardinality: ART-INT-00 §2.

### S-A04-DRAFT — DraftCRP / CompileError payloads

**Authority for field shape at pack time:** ART-INT `S-INT-DRAFT` (`architecture-integration/schemas/crp-wire.schema.md`).  
A-local `ArtifactVersion` envelope remains S-A04-AV (`artifact_class ∈ {DraftCRP, CompileError}`).

### S-A04-SEAL — SealedCRPSnapshot payload

**Authority for sealed boundary bytes:** ART-INT `S-INT-SEAL`.  
`sealed_digest` MUST equal ART-CRP `crp_digest` (ART-INT I-INT-20).

### S-A04-PRIOR — VerifierPrior

```text
prior_version_id, session_id
source_session_id              # may equal session_id for in-session intake
sealed_digest?
receipt_ref?
export_ref?
content_digest                 # read-only B material digest
active: bool                   # false for archival-only linkage
```

**I-A04-PRIOR-01:** `active=true` requires `sealed_digest` or `receipt_ref` (or both).  
**I-A04-PRIOR-02:** `active=true` forbidden when target session is CLOSED.

### S-A04-PF — PortfolioMember / PortfolioFrontier

As ART-A-02 §6 plus estimates; dominated_member_ids[] retained.

## Predicates

**P-A04-COH-01…07** — ART-A-02 §1.3.1 conjuncts 1–7; any false ⇒ not package-coherent.

**P-A04-DISTINCT-01** — Two PortfolioMembers are meaningfully distinct iff they differ in at least one of: primary claim lineage tip, mechanism lineage tip (if any), operator-class binding, or chain_segment / profile_hint; cosmetic renames alone fail.

**P-A04-PARETO-01** — Member A dominates B iff novelty_estimate ≥ B and survivability_estimate ≥ B and at least one strict inequality (advisory estimates only). Dominated ids listed in `dominated_member_ids[]`; not deleted.

**P-A04-SEAL-01** — `seal_set` entries MUST resolve to DraftCRP versions with successful compile; CompileError ids forbidden.

## Legal / illegal

| Legal | Illegal |
|-------|---------|
| Mint per A-02 owner | Mutate version_id payload |
| Append lifecycle | Reassign owner_module |
| Active prior with provenance | Active prior into CLOSED session |

## Failures

Referential integrity → Orch; DS91 only per A-03 allowlist.

## Consistency map

Ownership → A-02 · FSM → A-03 · Slice execution → A-05 · Projection/batch → A-06 · Persistence → A-07 · **A↔B interface → ART-INT-00**

## Changelog

2026-07-25: Initial freeze.  
2026-07-25b: SessionPolicyProfile, GateRequest/Decision, VerifierPrior provenance, Pareto/distinct predicates, schema IDs.  
2026-07-25c: Consistency amendment — DraftCRP/SealedCRPSnapshot payload schemas via ART-INT crp-wire (S-A04-DRAFT/SEAL).
