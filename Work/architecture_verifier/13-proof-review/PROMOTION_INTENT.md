# 13b — Promotion Intent and Proof-Carrying Axis Application (Normative)

**Artifact ID:** `ART-13b`  
**Version:** `ARCH-0.3-REPAIR-ITER5.7`  
**Normative status:** `ACTIVE_NORMATIVE`  
**Depends on:** ART-07b · ART-07c · ART-06b · ART-04c · ART-15 · ART-01 · ART-14 · ART-11b · ART-11c  
**Package:** `ARCH-0.3-REPAIR` · **NON-RELEASE**  
**Authority:** Design material. Material post-freeze edits require a new revision.  
**Self-contained:** This file is the sole normative text for ART-13b; prior ITER5.x drafts are non-normative.

## Purpose

Proof-carrying `RESEARCH_MATURITY` raises: content-addressed `PromotionIntent` + Commit-time recompute. Sole apply path: `APPLY_PROMOTION` via `I.Commit`. Caller `*_ok` forbidden. Demotion/`SUPERSEDED` = Iter7. Audit↔intent bind = Iter6.

---

## 1. Axis

| Order | Value |
|-------|--------|
| 0 | `OPEN` (default if no record) |
| 1 | `CONJECTURE` |
| 2 | `PARTIAL_RESULT` |
| 3 | `RESULT` |

Store: `ResearchMaturityRecord`. `SUPERSEDED` is **not** writable via APPLY (Iter7).  
ART-01 `major_milestone` promotion targets: `{PARTIAL_RESULT, RESULT}` only. `PROVED_ON_PAPER` / `LEAN_*` non-operational.

---

## 2. PromotionPolicy

```text
PromotionPolicy
  policy_digest = H(policy_id, from_value, to_value, required_proof_floor,
                    requires_gate_ids_sorted, authorized_role_ids_sorted,
                    required_basis_kinds_sorted)
  policy_id
  from_value
  to_value
  required_proof_floor                # UNPROVED | INFORMAL | CERTIFIED_INFORMAL
  requires_gate_ids[]                 # additive only
  authorized_role_ids[]
  required_basis_kinds[]              # ⊂ {CERTIFICATION_RECORD, PROOF_ATTACHMENT}
```

**I-POL-01:** Only genesis rows below are valid. Unknown digest ⇒ `POLICY_MISMATCH`.  
**I-POL-02:** `to_value` strictly greater than `from_value` in §1. No downward, no self, no `SUPERSEDED`.  
**I-POL-03:** `to_value=RESULT` ⇒ floor `CERTIFIED_INFORMAL` and `required_basis_kinds={CERTIFICATION_RECORD}`.  
**I-POL-04:** Immutable; replacement = new id/digest.  
**I-POL-05:** Policy gates cannot suppress I-AP-10 mandatory gates.

### Genesis registry (exhaustive package seed)

| policy_id | from → to | floor | policy gates | roles | required_basis_kinds |
|-----------|-----------|-------|--------------|-------|----------------------|
| `RM_OPEN_CONJECTURE` | OPEN→CONJECTURE | UNPROVED | ∅ | VERIFICATION_ORCHESTRATOR | ∅ |
| `RM_CONJ_PARTIAL` | CONJECTURE→PARTIAL_RESULT | INFORMAL | ∅ | VERIFICATION_ORCHESTRATOR | `{PROOF_ATTACHMENT}` |
| `RM_PARTIAL_RESULT` | PARTIAL_RESULT→RESULT | CERTIFIED_INFORMAL | ∅ | VERIFICATION_ORCHESTRATOR | `{CERTIFICATION_RECORD}` |
| `RM_OPEN_RESULT` | OPEN→RESULT | CERTIFIED_INFORMAL | ∅ | VERIFICATION_ORCHESTRATOR | `{CERTIFICATION_RECORD}` |
| `RM_CONJ_RESULT` | CONJECTURE→RESULT | CERTIFIED_INFORMAL | ∅ | VERIFICATION_ORCHESTRATOR | `{CERTIFICATION_RECORD}` |

`policy_digest = H(…)` over each row’s schema fields. Mandatory ART-15 gates are **not** listed — recomputed at Commit (I-AP-10).

---

## 3. PromotionIntent

```text
PromotionIntent
  intent_digest = H(intent_schema_id, target_claim_digest, policy_digest, basis_digests_sorted)
  intent_schema_id
  target_claim_digest
  policy_digest
  basis_digests[]
```

**I-PI-01:** Identity = `intent_digest`.  
**I-PI-02:** No ART-06b §6 caller-boolean names / authorizing `*_ok` in intent or APPLY payload.  
**I-PI-03:** `basis_digests` covers each kind in `policy.required_basis_kinds` (≥1 each); extras forbidden.

---

## 4. Commands

### APPLY_PROMOTION
```text
payload =
  promotion_intent
  # human decisions NOT in payload — EffectiveDecision derived from pre-state log (I-AP-10b / I-AP-09)
```
**I-AP-AUTH-01:** Caller ACTIVE; binding live; `role_id ∈ policy.authorized_role_ids`.

### SET_EIO_VETO / CLEAR_EIO_VETO
```text
SET_EIO_VETO.payload   = { claim_digest }
CLEAR_EIO_VETO.payload = { claim_digest }
```
Caller RoleBinding.role_id = `EIO` (ART-04c matrix). Effects upsert `EioVetoRecord{claim_digest, active}`.  
Missing record ≡ never vetoed. Veto **generation** = `event_seq` of latest successful SET that left `active=true` (from MutationEvent log).

### RECORD_EIO_ASSESSMENT
```text
payload = { intent_digest, outcome }   # ALLOW | BLOCK; claim DERIVED from intent.target_claim_digest
```
Caller role_id = `EIO`. Upserts `EioAssessmentRecord{intent_digest, outcome}`. Authoritative ordering = event log.

---

## 5. APPLY Commit recompute

Let `P` = genesis policy for `intent.policy_digest`. Let `cur` = current maturity (default `OPEN`). Let `from=P.from_value`, `to=P.to_value`.

**I-AP-00 (idempotent):** If `cur=to` and latest successful APPLY for this claim has the same `intent_digest` ⇒ ACCEPTED with empty Research effects. If `cur=to` otherwise ⇒ `FROM_MISMATCH`.  
**I-AP-01:** Else require `cur=from`; else `FROM_MISMATCH`.  
**I-AP-02:** P registered; I-POL-02 holds; else `POLICY_MISMATCH`.  
**I-AP-03:** `DerivedProofFloor(target) ≥ P.required_proof_floor` under `UNPROVED < INFORMAL < CERTIFIED_INFORMAL`; else `PROOF_FLOOR_INSUFFICIENT`.  
**I-AP-PO:** If any live ART-07b `ProofObligation` with `originating_claim_digest=target` and `blocks_promotion=true` has `status ∈ {OPEN, FAILED}` ⇒ `OBLIGATION_UNRESOLVED` (I-PO-03). A claim with unresolved blocking obligations is not certifiable / not APPLY-eligible.
**I-AP-05 (basis bind):**  
- Each required kind’s digests resolve to that kind.  
- `PROOF_ATTACHMENT`: unique valid attachment for `target_claim_digest`.  
- `CERTIFICATION_RECORD`: cited digest is a CertificationRecord for which ART-04c `I-CERTIFY-01` holds **for this target using that record** at pre-state.  
Else `BASIS_INVALID`.  

**DerivedBasisProposers(intent, S):** for each `basis_digest` in intent:  
- if CERTIFICATION_RECORD R: principal of the MutationEvent that first introduced `R`’s `proof_evidence_digest` (ART-04c I-CERTIFY-01 derived proposer).  
- if PROOF_ATTACHMENT A: principal of the MutationEvent that first introduced `A.proof_evidence_digest`.  
Empty basis (e.g. OPEN→CONJECTURE) ⇒ empty set (I-AR-04 vacuously true).
**I-AP-06:** If any ART-07b FULL Counterexample (archived or not) has I-CX-01 hitting `intent.target_claim_digest`, require ART-16b I-DW-21: current maturity SUPERSEDED **and** COMPLETE FULL_CX DemotionWave with target ∈ seeds whose `trigger_digest` is that `cx_digest` **or** `H("CX_EXPAND", cx_digest, *)`; else `CX_BLOCKS_PROMOTION`.  
**I-AP-07:** Non-noop success writes exactly one maturity upsert to `to`. No floor/ControlState/inference-endpoint writes.

**I-AP-08 ValidationPreimageAPPLY.v7** (closed; no command mirrors):
```text
schema_id = "ART13b.ValidationPreimageAPPLY.v7"
cur_maturity
derived_proof_floor
required_gate_ids_sorted[]
basis_ok
utility_ok
eio_assessment_ok
eio_veto_clear
idempotent_noop
major_milestone
audit_ok                              # ART-11b: true iff non-major or I-BIND-01 holds
audit_digest                          # A*.audit_digest or ⊥
cycle_ok                              # ART-08d: true iff non-major or DerivedCycleMilestoneOk
dd_ok                                 # ART-11c: true iff ¬data-independence/FIXED or (I-DDV-01 ∧ I-DDV-11)
psi_ok                                # ART-11c: true iff ¬requires_DATA_DEP_PSI or I-PSI-02
model_prov_ok                         # ART-11c: true iff no I-MP-20-stale evidence in basis
roles_invoked_ok                      # ART-04d: true iff I-OM-10 RoleCeiling PASS
```

**EffectiveDecision(gate_id, target_digest):** latest committed HumanDecision with that `gate_id` and `target_digest` (max event_seq). Require `decision=approve` and unexpired at Commit seq; else fail. (No caller-supplied decision digests.)

**I-AP-09 (veto):** If `EioVetoRecord.active=true` for target claim: EffectiveDecision(`OVERRIDE_EIO`, `H(intent_digest, veto_intro_event_seq)`) must succeed; else `EIO_VETO`.

**I-AP-10 RequiredGates:**
```text
novelty_hit = (to > CONJECTURE) ∨ (major_milestone(claim,to) ∧ novelty_alignment(claim) ≥ PLAUSIBLE_NOVELTY)

RequiredGates(claim, P, to) =
  set(P.requires_gate_ids)
  ∪ { PLAUSIBLE_NOVELTY_LABEL, NOVELTY_TRACK_ACK }     if novelty_hit
  ∪ { INFERENCE_THEOREM_CLAIM }                         if major_milestone ∧ inference_facing(claim)
  ∪ { SELECTED_OBJECT_CHANGE }                          if major_milestone ∧ policy_facing(claim)
  ∪ utility_gates(claim, to)
```

`utility_gates`: if `to > CONJECTURE` and not `utility_compat_resolved(claim)`:  
- if `stability_NA_utility(claim)` ⇒ `{N/A_UTILITY_ACK}`  
- else ⇒ `{UTILITY_WAIVER}`

**Closed predicates**
- `major_milestone(claim,to)` — ART-01 with operational targets `{PARTIAL_RESULT, RESULT}` plus facing/novelty clauses.  
- `inference_facing` — ART-01.  
- `policy_facing(claim)` — `claim.chain_segment = selection_stability` ∧ `subject_ref.object_class = POLICY`.  
- `novelty_alignment(claim)` — Commit-held novelty label side record; absent ⇒ below PLAUSIBLE (no novelty_hit from alignment alone).  
- `utility_compat_resolved` — ∃ `UTILITY_CONSTRAINT` dep U with UtilityCompat `link_kind ∈ {PROVED_INEQUALITY, WAIVER_HUMAN}`.  
- `stability_NA_utility` — `chain_segment=selection_stability` ∧ Commit-held N/A utility marker for claim.

**I-AP-10b:** For every `g ∈ RequiredGates`, EffectiveDecision(`g`, `intent_digest`) must succeed; else `GATE_REQUIRED`.
**I-AP-10c (N/A_UTILITY_ACK authority):** When that gate is required, the effective HD’s principal MUST have live `INTEGRATION_AUDITOR` RoleBinding at decision’s introducing seq; else `GATE_REQUIRED`.

**I-AP-12 (EIO assessment — all APPLY):** Latest `EioAssessmentRecord` for `intent_digest` MUST have `outcome=ALLOW` and no later `BLOCK` for that intent; else `EIO_REQUIRED`. Combined with I-AP-09.  
**I-AP-13 (demotion fence):** While ART-16b is DRAFT_REPAIR or ACTIVE_NORMATIVE: any DemotionWave with `cursor < len(work_items)` ⇒ non-noop APPLY fails `DEMOTION_WAVE_OPEN` (ART-16b I-DW-20).

**I-AP-11 (audit bind):** While ART-11b is DRAFT_REPAIR or ACTIVE_NORMATIVE in this package, `major_milestone(claim,to)` ⇒ ART-11b I-BIND-01.  
**I-AP-14 (cycle bind):** While ART-08d is DRAFT_REPAIR or ACTIVE_NORMATIVE, `major_milestone(claim,to)` ⇒ ART-08d DerivedCycleMilestoneOk else `CYCLE_PHASE_REQUIRED`.  
**I-AP-15 (provenance bind):** While ART-11c is DRAFT_REPAIR or ACTIVE_NORMATIVE: `dd_ok` / `psi_ok` / `model_prov_ok` per ART-11c §6; else `DD_BLOCKED` | `DATA_DEP_PSI_REQUIRED` | `MODEL_PROV_STALE`. Evidence refs: ART-11c I-EV-01 else `EVIDENCE_PROV_FAIL`.  
**I-AP-16 (role ceiling):** While ART-04d is DRAFT_REPAIR or ACTIVE_NORMATIVE: major APPLY ⇒ ART-04d I-OM-10 else `ROLE_CEILING`.

**I-BOOL-02:** Maturity axis writes only via APPLY_PROMOTION; ART-16b `ADVANCE_DEMOTION_WAVE`; or ART-16b I-DW-30/33 seed SUPERSEDE on `RECORD_COUNTEREXAMPLE` (FULL) / `START_DEMOTION_WAVE` / I-DW-33; else `AXIS_WRITE_FORBIDDEN`.

---

## 6. Side tables

```text
EioVetoRecord         { claim_digest, active }
EioAssessmentRecord   { intent_digest, outcome }  # ALLOW|BLOCK; claim derived from intent
```

---

## 7. Failures

`FROM_MISMATCH | POLICY_MISMATCH | PROOF_FLOOR_INSUFFICIENT | OBLIGATION_UNRESOLVED | BASIS_INVALID | CX_BLOCKS_PROMOTION | AXIS_WRITE_FORBIDDEN | GATE_REQUIRED | EIO_VETO | EIO_REQUIRED | AUDIT_REQUIRED | AUDIT_FAIL | AUDIT_STALE | AUDIT_INDEPENDENCE | AUDIT_EVIDENCE_MISSING | DISCONFIRM_MISSING | UNKNOWN_AUDIT_QUESTION | CYCLE_PHASE_REQUIRED | DEMOTION_WAVE_OPEN | DD_BLOCKED | DATA_DEP_PSI_REQUIRED | MODEL_PROV_STALE | EVIDENCE_PROV_FAIL | DD_HIDDEN_READ | DD_CORE_MISMATCH | ROLE_CEILING`

---

## 8. Traces

```text
TRACE-5A  PARTIAL→RESULT + bound cert + gates + EIO ALLOW → RESULT
TRACE-5B  RESULT + INFORMAL floor → PROOF_FLOOR_INSUFFICIENT
TRACE-5C  *_ok payload → CALLER_BOOLEAN_FORBIDDEN
TRACE-5D  stale from → FROM_MISMATCH
TRACE-5E  wrong cert digest → BASIS_INVALID
TRACE-5F  non-APPLY maturity write → AXIS_WRITE_FORBIDDEN
TRACE-5H  retry same intent → noop
TRACE-5I  veto without generation-bound effective OVERRIDE → EIO_VETO
TRACE-5J  downward policy → POLICY_MISMATCH
TRACE-5K  past CONJECTURE without NOVELTY_TRACK_ACK → GATE_REQUIRED
TRACE-5M  OPEN→CONJECTURE with novelty≥PLAUSIBLE without novelty gates → GATE_REQUIRED
TRACE-5N  older approve + later deny (gate or OVERRIDE) → GATE_REQUIRED / EIO_VETO
TRACE-5O  OVERRIDE old veto gen after new SET → EIO_VETO
TRACE-5P  APPLY without EioAssessment ALLOW for intent → EIO_REQUIRED
TRACE-5Q  past CONJECTURE without utility resolve/waiver → GATE_REQUIRED
TRACE-5R  N/A_UTILITY_ACK from non-INTEGRATION_AUDITOR → GATE_REQUIRED
```

---

## 9. Deferred / legacy

Audit bind (6); demotion (7); Lean (8); FSM S09 (9); restore (10); release (14).  
ART-09/13 prose / caller booleans non-authoritative. ART-11 PASS ≠ promotion.
