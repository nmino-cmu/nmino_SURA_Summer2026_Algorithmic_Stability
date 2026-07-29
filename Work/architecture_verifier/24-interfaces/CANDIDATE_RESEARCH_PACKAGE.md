# CRP — Candidate Research Package (Normative)

**Artifact ID:** `ART-CRP`  
**Version:** `ARCH-0.3-REPAIR-DUAL.2`  
**Normative status:** `ACTIVE_NORMATIVE`  
**Depends on:** ART-01 · ART-01V · ART-07b · ART-07c · ART-06b · ART-04c · ART-21b · ART-11b · ART-12-CHAR  
**Package:** `ARCH-0.3-REPAIR` · **NON-RELEASE**  
**Self-contained:** Sole normative text for external mathematical intake into System B. Canonical object registration = ART-07b §10A.

## Purpose

`CandidateResearchPackage` (CRP) is the **only** external mathematical intake object for the Verification Architecture. Authors are `HUMAN` or `RESEARCH_DISCOVERY_ASSISTANT`. Speculative contents gain authority only after B `I.Commit` DeriveEffects succeed.

`ponytail:` Legacy mid-flight ART-08d cycles may use `LEGACY_CYCLE_INTAKE` shim until closed (I-CRP-20).

---

## 1. Object

Registered in ART-07b §10A. Digest fields:

```text
CandidateResearchPackage
  crp_digest = H("ARTCRP.v1", author_kind, author_principal_digest,
                 author_binding_digest_or_⊥, profile, math_scope_pin_digest,
                 payload_canonical, prior_crp_digest_or_⊥)
  author_kind                 # HUMAN | RESEARCH_DISCOVERY_ASSISTANT
  author_principal_digest
  author_binding_digest?      # required if ASSISTANT
  profile                     # PHASE_A_CHARACTERIZATION | PHASE_B_STABILIZATION | MIXED
                              # | OBLIGATION_ONLY | BRIDGE_ONLY
  math_scope_pin_digest
  payload                     # see §2
  sealed_at                   # ISO-8601 UTC
  # post-intake (ART-07b): admissibility_state, intake_status, commit_event_seq,
  # contained_object_refs[], emitted_obligation_digests[], intake_receipt_digest

IntakeReceipt
  receipt_digest = H("ARTCRP.IN.v1", crp_digest, event_seq, draft_claim_digests_sorted)
  crp_digest
  event_seq
  draft_claim_digests[]
  obligation_digests[]
  status                      # ACCEPTED_DRAFT | REJECTED
  reason_codes[]?
```

**I-CRP-01:** Sole external mathematical intake for B.  
**I-CRP-04:** Payload fields are drafts until Commit materializes live ART-07b objects (Claims + ProofObligations).

---

## 2. Payload

```text
payload
  definitions[]
  assumptions[]
  claims[]
  proof_sketches[]
  bridge_proposals[]
  mechanism_proposals[]       # OPTIONAL (required only for PHASE_B_STABILIZATION)
  examples[]
  falsifiers[]
  counterexample_claims[]
  certificate_drafts[]
  literature_refs[]
  declared_reads[]
  free_text_notes?
```

**I-CRP-02 Phase A:** If `profile=PHASE_A_CHARACTERIZATION` or `OBLIGATION_ONLY`, `mechanism_proposals` MAY be empty; B MUST NOT reject solely for missing MechanismInstance / Q_ψ / stability cert / inference bridge.  
**I-CRP-03:** Optimization primitives alone do **not** imply a stabilization mechanism.  
**I-CRP-05 Phase B:** `profile=PHASE_B_STABILIZATION` ⇒ ≥1 mechanism_proposal or live MechanismInstance ref.  
**I-CRP-06 MIXED:** Characterization claims may omit mechanisms; `selection_stability` claims follow ART-07b I-CERT-01 at promotion.  
**I-CRP-07 BRIDGE_ONLY:** Claims are bridge-facing; mechanism not required unless a stability claim is included.

---

## 3. Admissibility

**`admissible_package(crp)`** true iff all hold:

1. `math_scope_pin_digest` matches live ART-01/02 Area-1 pin.  
2. `author_kind` auth: HUMAN ACTIVE, or ASSISTANT with live `RESEARCH_DISCOVERY_ASSISTANT` RoleBinding (+ model_prov if MODEL_RUNTIME).  
3. Profile rules I-CRP-02/05/07.  
4. Every claim `chain_segment` ∈ ART-07b segment enum (incl. `characterization`).  
5. Phase A profile ⇒ no mandatory stability-guarantee mechanism fields.  
6. No SIMULATION-only loop writing ResearchState.

False ⇒ `REJECT_CANDIDATE_PACKAGE` / `PACKAGE_INADMISSIBLE`.

---

## 4. Commands & DeriveEffects

**SUBMIT_CANDIDATE_PACKAGE** (`VERIFICATION_ORCHESTRATOR` or `HUMAN_GATE_OPERATOR`):  
Validate admissibility; DeriveEffects MUST:

1. Upsert live `CandidateResearchPackage` (ART-07b §10A) with `intake_status=ACCEPTED_DRAFT`.  
2. Mint draft Claims/defs/assumptions bound to `crp_digest`.  
3. Mint `ProofObligation`s per ART-07b I-PO-01; set `emitted_obligation_digests[]`.  
4. Append `IntakeReceipt` with claim + obligation digests.

**REJECT_CANDIDATE_PACKAGE:** receipt REJECTED; no Research object upserts (except EventLog receipt if policy logs rejects).

**I-CRP-10:** After accept, verification uses B commands only. A does not APPLY.

**I-CRP-11 Idempotent replay (ART-INT I-INT-21):** A second `SUBMIT_CANDIDATE_PACKAGE` whose `crp_digest` equals an already-accepted package and whose payload canonical bytes match MUST NOT mint a second distinct claim set; return the existing `IntakeReceipt` (or equivalent ACCEPTED_DRAFT replay). Changed content ⇒ different `crp_digest` ⇒ new intake.

**I-CRP-12 Batch:** B has no `SubmissionBatch`. Each Command carries one CRP. A fan-out: ART-INT I-INT-10.

**I-CRP-13 Feedback:** Package-scoped read-back for Discovery uses ART-INT `VerifierFeedbackExport` (via `I.LibraryExport` / `I.VerifierFeedbackExport`).

---

## 5. Post-intake verification paths (normative)

**I-CRP-30 Claim-direct path (default):** After ACCEPTED_DRAFT, B MAY run CX / audit / Lean / APPLY on `draft_claim_digests` **without** `LOCK_CYCLE`. Audit profile routes by CRP `profile` (ART-11b §0). Characterization CX uses ART-12-CHAR.

**I-CRP-31 Cycle-bound path (optional):** `LOCK_CYCLE` is **not** required for verification. It is required **only** to use ART-08d cycle commands (`BIND_CYCLE_CARD`, `RECORD_CYCLE_*`, `ADVANCE_CYCLE`). When used, caller = `VERIFICATION_ORCHESTRATOR`; `target_claim_digest` MUST be in the CRP’s draft claims. Discovery `FRONTIER_SCHEDULER` never locks B cycles.

**I-CRP-20 `LEGACY_CYCLE_INTAKE`:** Pre-DUAL open cycles MAY continue without CRP until closed. New cycle-bound work SHOULD bind to an accepted CRP claim digest.

---

## 6. Consumer deltas

| Artifact | Delta |
|----------|-------|
| ART-07b §10A/10B | CRP + IntakeReceipt + ProofObligation registration |
| ART-08d | LOCK_CYCLE optional; VERIFICATION_ORCHESTRATOR only |
| ART-11b / ART-12-CHAR | Profile routing + characterization CX/audit |
| ART-13b | I-AP-PO / `OBLIGATION_UNRESOLVED` |
| ART-21b | CRP + characterization fixtures |

---

## 7. Failures / traces

`PACKAGE_INADMISSIBLE | CRP_SCHEMA | CRP_AUTHOR | CRP_PROFILE | MECHANISM_REQUIRED | OBLIGATION_UNRESOLVED | LEGACY_CYCLE_ONLY`

```text
TRACE-CRP-A  Phase A without mechanism → ACCEPTED_DRAFT + ≥1 ProofObligation
TRACE-CRP-B  Phase B without mechanism → MECHANISM_REQUIRED
TRACE-CRP-C  ASSISTANT without binding → CRP_AUTHOR
TRACE-CRP-D  Human CRP → same intake path as ASSISTANT
TRACE-CRP-E  APPLY with OPEN blocking obligation → OBLIGATION_UNRESOLVED
```
