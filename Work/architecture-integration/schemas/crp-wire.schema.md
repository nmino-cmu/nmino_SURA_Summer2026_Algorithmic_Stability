# CRP wire schemas (ART-INT)

**Authority:** ART-INT-00 for boundary shapes. ART-CRP owns B admissibility & DeriveEffects. ART-A-04 owns A ArtifactVersion envelope. ART-21b owns canonicalization.

## S-INT-DRAFT — DraftCRP.payload

Unsealed; `artifact_class=DraftCRP`; owner CRP_PACKAGER.

```text
DraftCRPPayload
  schema_version              # "ARTINT.DRAFT.v1"
  branch_id
  member_id?
  profile_hint                # same enum as CRP profile (ART-CRP)
  math_scope_pin_digest
  tip_pins[]                  # version_ids compiled
  dep_closure_digest
  payload                     # same shape as ART-CRP §2 (may be incomplete → CompileError)
  compile_ok: true
  missing_required[]?         # empty when compile_ok
  prior_draft_version_id?
  created_at                  # ISO-8601 UTC
```

**CompileError.payload** (`artifact_class=CompileError`):

```text
CompileErrorPayload
  schema_version              # "ARTINT.DRAFT.v1"
  branch_id
  member_id?
  profile_hint?
  error_codes[]               # e.g. COHERENCE | MISSING_FIELD | PROFILE_MISMATCH
  message
  missing_required[]?
  created_at
```

## S-INT-SEAL — SealedCRPSnapshot.payload

Immutable; owner RESEARCH_DISCOVERY_ASSISTANT.

```text
SealedCRPSnapshotPayload
  schema_version              # "ARTINT.SEAL.v1"
  draft_crp_version_id
  sealed_digest               # = crp_digest
  crp                         # full CandidateResearchPackage preimage (ART-CRP §1 fields + payload)
  gate_record_id
  sealed_at                   # ISO-8601 UTC
```

**I-INT-SEAL-01:** `crp` MUST satisfy ART-CRP field requirements for its `profile` before seal.  
**I-INT-SEAL-02:** `sealed_digest = H("ARTCRP.v1", …)` per ART-CRP (ART-21b packing).

## S-INT-ENV — SubmissionEnvelope

Wire object passed to `I.DiscoverySubmit` / Commit payload.

```text
SubmissionEnvelope
  schema_version              # "ARTINT.ENV.v1"
  crp                         # CandidateResearchPackage (ART-CRP)
  idempotency_key             # = crp.crp_digest
  a_session_id?               # optional telemetry; B MUST ignore for math
  a_batch_id?                 # optional telemetry; B MUST ignore
  a_attempt_id?               # optional telemetry; B MUST ignore
```

**I-INT-ENV-01:** B validates `crp` only for admissibility; unknown A telemetry keys with `a_` prefix MAY be stripped; unknown non-telemetry keys ⇒ `UNKNOWN_FIELD` / `CRP_SCHEMA`.

## CandidateResearchPackage (reference)

Authoritative field list: ART-CRP §1–2. Required envelope fields at seal:

- `author_kind`, `author_principal_digest`, `author_binding_digest?`, `profile`, `math_scope_pin_digest`, `payload`, `sealed_at`, `prior_crp_digest?`

## Mechanism alias

| A field | Wire |
|---------|------|
| ExampleCard.`perturbation_mechanism_id` | If set: include matching `mechanism_proposals[]` entry with `local_id`; else omit |
| MechanismProposal IR | `mechanism_proposals[]` |
| Phase A / OBLIGATION_ONLY | `mechanism_proposals` MAY be `[]` |

B has **no** `perturbation_mechanism_id` field.
