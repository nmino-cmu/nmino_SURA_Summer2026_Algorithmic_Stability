# 07b — Canonical Mathematical Objects (Normative)

**Artifact ID:** `ART-07b`  
**Version:** `ARCH-0.3-REPAIR-ITER1.26`  
**Status:** Normative Iteration-1 object model (bridge source_cert = selected_object covering cert).  
**Authority:** Design material. Changes reset Iteration-1 readiness.

## Purpose

Freeze **what mathematical/epistemic objects exist** and **how they are identified**. Free-text narrative is never the authoritative assertion.

## Scope lock

Supports:

- Full chain: `data → F_D scores → Q_ψ → selection → stability certificate → composition → selected object/policy → post-hoc inference`  
- **Phase A characterization** claims (`chain_segment=characterization`) without mandatory MechanismInstance / Q_ψ (ART-CRP / ART-01)

Default: **finite** Λ. Non-finite Λ requires an **authoritative** `HumanDecision` (`CONTINUOUS_LAMBDA`) — **unsatisfiable until Iteration 4** (I-HD-01).

---

## 1. Meta rules

### 1.1 Normative vs explanatory

| Class | Meaning |
|-------|---------|
| **Normative** | Identity, promotion binding, invalidation, audit binding |
| **Explanatory** | Rendering only; never read by promotion/audit/Lean predicates |

### 1.2 Digests

```text
object_digest = H(canonical_serialization(normative_fields))
```

`H` and canonicalization are **ART-21b** I-H-01 / I-CAN-01 (`SHA-256`, `ART21b.CANON.v1`). Registry handles may exist but must bind 1:1 to digests. Digests never hash mutable registry keys.

### 1.3 ClaimRelation

```text
ClaimRelation                         # immutable
  relation_digest
  relation_kind                       # REVISION_OF | SUPERSEDES | EQUIVALENT_TO | RENAMES
  source_claim_digest
  target_claim_digest
  evidence_claim_digest?              # REQUIRED when kind=EQUIVALENT_TO
```

| Kind | CX edge valid when |
|------|--------------------|
| RENAMES | I-REL-02 (equal math fingerprint) |
| EQUIVALENT_TO | I-REL-01 |
| REVISION_OF / SUPERSEDES | **Not a CX closure edge** (provenance only; Iter7 demotion may use them) |

**I-REL-01:** `EQUIVALENT_TO` valid iff evidence Claim has `assertion_schema_id ∈ equivalence_schemas[]`, payload binds both digests exactly, and `DerivedProofFloor(evidence) = CERTIFIED_INFORMAL` (I-PF-04). INFORMAL alone is insufficient.

**I-REL-02:** `RENAMES` valid iff `claim_math_fingerprint(source) = claim_math_fingerprint(target)`. Otherwise invalid; not traversed by CX closure.

---

## 2. Definitions

```text
DefinitionVersion                     # immutable
  def_version_digest
  def_id
  body_schema_id                      # schema_role=DEFINITION_BODY
  body_payload
  body_digest                         # = H(body_schema_id, body_payload)
  symbol_table_schema_id              # schema_role=SYMBOL_TABLE
  symbol_table_payload                # typed map symbol → structured local meaning (I-DEF-03)
  parent_def_version_digest?
  change_summary                      # explanatory
  prose_rendering?                    # explanatory
```

```text
ActiveDefinitionHead                  # mutable via ART-06b I.Commit only
  def_id
  active_def_version_digest
  set_at_event_id
```

```text
DefPin
  def_id
  def_version_digest
  body_digest
  symbols_covered[]                   # ⊆ symbol_table keys; equals required symbol set
```

**I-DEF-01:** Identifier nodes are `{def_id, symbol}`; pins must resolve; inventory = fixed walk over normative math fields.

**I-DEF-02:** Non-historical promotion requires ActiveDefinitionHead match. Historical scope uses side binding (not inside `claim_digest`):

```text
HistoricalScopeBinding                # side table; NOT hashed into claim_digest
  binding_digest                      # = H(claim_digest, historical_scope_dec_digest)
  claim_digest
  historical_scope_dec_digest
```

**I-DEF-02:** For promotion (non-`historical_scoped`), each DefPin’s `def_version_digest` must equal `ActiveDefinitionHead` for that `def_id`. Valid iff ART-04c I-HD-AUTH allows authoritative decisions **and** HumanDecision has `gate_id=HISTORICAL_SCOPE_ACK`, `decision=approve`, `target_digest=claim_digest` when historical_scoped.

**I-DEF-03:** SchemaRegistry admits a schema only if a **structural** check (recursive walk) finds no unconstrained string node carrying mathematical meaning. `forbids_opaque_string_roots` is a derived bit, not an author boolean. Allowed strings: citations/labels/render keys with `explanatory: true`.

---

## 3. Assumption and discharge

```text
Assumption
  assumption_digest
  statement_schema_id                 # schema_role=PROPOSITION
  statement_payload
  kind                                # AXIOM | HYPOTHESIS | MODELING | DATA | GATE_WAIVER
  prerequisite_assumption_digests[]
  definition_pins[]
```

```text
AssumptionUse
  slot_id
  assumption_digest
  role                                # REQUIRED | DISCHARGED
```

```text
DischargeRecord                       # side table; NEVER in claim_digest
  discharge_digest                    # = H(target_claim_digest, slot_id, assumption_digest, discharger_claim_digest)
  target_claim_digest
  slot_id
  assumption_digest
  discharger_claim_digest
```

**I-ASM-01 (computable REQUIRED closure):**  
Let `StmtDigest(A) = H(A.statement_schema_id, A.statement_payload)`.  
`Prereq*(a) = {a} ∪ ⋃_{p ∈ Assumption(a).prerequisite_assumption_digests} Prereq*(p)` (must be finite/acyclic; cycles ⇒ invalid Assumption).  

For Claim C:  
`DirectRequired(C) = ⋃_{u ∈ C.assumptions_used, u.role=REQUIRED} Prereq*(u.assumption_digest)`  
`InheritedRequired(C) = ⋃_{d ∈ C.dependencies} NetRequired(premise(d))`  
`GrossRequired(C) = DirectRequired(C) ∪ InheritedRequired(C)`  

A DischargeRecord r is applicable to C iff r.target_claim_digest=C.claim_digest and r valid per I-ASM-02 and there exists AssumptionUse u on C with u.slot_id=r.slot_id, u.assumption_digest=r.assumption_digest, u.role=DISCHARGED.  

`NetRequired(C) = GrossRequired(C) \ { r.assumption_digest | r applicable to C }`  
`NetRequiredDigest(C) = H(sorted unique digests in NetRequired(C))`  

Every schema-required assumption slot has exactly one AssumptionUse. Duplicate slot_ids invalid. DISCHARGED without applicable DischargeRecord ⇒ invalid Claim.
**I-ASM-02:** Discharge valid iff AssumptionUse role=DISCHARGED; statement=conclusion digests match; discharger ≠ target; `DerivedProofFloor(discharger)=CERTIFIED_INFORMAL`; discharger is LOGICAL/DEFINITIONAL premise; no circular discharge.

**I-ASM-03:** Weakening only via new Assumption + ClaimRelation.

---

## 4. Claim

### 4.1 Encoding

```text
Claim
  claim_digest                        # H(normative fields below — NOT proofs, discharges, historical bindings)
  chain_segment                       # see §4.3
  assertion_schema_id                 # schema_role=ASSERTION
  assertion_payload
  assumptions_used[]
  dependencies[]                      # premise_claim_digest + kind ∈
                                      # {LOGICAL, DEFINITIONAL, BRIDGE, UTILITY_CONSTRAINT}
  mechanism_digest?
  subject_ref
  mathematical_scope                  # scope_schema_id + scope_payload
  continuous_lambda_dec_digest?       # side-effect of I-SCOPE-01; see note
  parameter_domain                    # domain_schema_id + domain_payload
  definition_pins[]
  # historical scope: HistoricalScopeBinding side table only (I-DEF-02)
```

`continuous_lambda_dec_digest` may appear on Claim only as a **reference field** that is included in digest; until Iter4 it cannot validate (I-HD-01), so non-finite Λ Claims are invalid for promotion.

**I-SCOPE-02:** scope and domain schemas required (I-DEF-03).

**I-FP-01 (claim_math_fingerprint):**

```text
ConclusionDigest(payload, schema) = H(conclusion_proposition_schema_id, conclusion_payload)
  where conclusion_payload is the unique schema field flagged conclusion: true
  (schemas without exactly one such field are invalid — SchemaRegistry.requires_conclusion_field)

claim_math_fingerprint = H(
  chain_segment,
  assertion_schema_id,
  ConclusionDigest(assertion_payload, assertion_schema),
  subject_ref.subject_digest,
  mechanism_digest or ⊥,
  parameter_domain_digest,            # full domain including DD bind (I-DD)
  mathematical_scope_digest,          # = H(scope_schema_id, scope_payload)
  guarantee_core or ⊥,                # I-FP-02
  failure_budget_digest or ⊥,         # = H(failure_budget payload) when present
  endpoint_digest or ⊥,               # REQUIRED for certificate_segments ∪ {bridge, inference} — ART-07c
  NetRequiredDigest(C),
  DefPinMultisetDigest(C)
)
```

**I-FP-02:** `guarantee_core = H(failure_budget_digest, neighbor_or_comparison_rel, guarantee_kind)` from fields flagged `guarantee_core: true`; absent ⇒ ⊥.

**I-FP-03 (endpoint projection):** `endpoint_digest` in I-FP-01 is derived per ART-07c §12:  
certificate → `CertificateEndpoint.endpoint_digest`;  
bridge → `H(source_endpoint_digest, target_endpoint_digest)`;  
inference → `InferenceEndpoint.inference_endpoint_digest`; else ⊥.

Annotations side table: `narrative_summary`, `author_notes` (explanatory).

```text
ProofAttachment
  attachment_digest                   # = H(claim_digest, proof_evidence_digest)
  claim_digest
  proof_evidence_digest
```

**I-PF-00:** attachment ↔ evidence claim equality; digests recompute.

### 4.2 Subject and operator

```text
SubjectRef
  subject_schema_id                   # schema_role=SUBJECT
  subject_digest                      # = H(subject_schema_id, subject_payload)
  subject_payload
  object_class                        # DERIVED from SchemaRegistry: subject_schema.object_class
                                      # ∈ {INDEX, POLICY, OTHER} — required on SUBJECT schemas
  selection_operator_digest           # DERIVED from operator projection
```

```text
SelectionOperator
  operator_digest
  operator_schema_id                  # schema_role=OPERATOR
  operator_payload
  definition_pins[]
```

**I-SUB-01/I-OP-01:** digests recompute; bare string operator IDs invalid.

**I-SUB-02:** Segments `perturbation_law`, `selection_application`, `selection_stability`, `perturbation`, `composition` require nonempty operator projection where the segment table says so.

### 4.3 Chain segments (complete front-to-back)

| chain_segment | Required bindings |
|---------------|-------------------|
| `data_regime` | typed data/neighbor regime |
| `score_construction` | exactly one LOGICAL dep on `data_regime`; predecessor from dep; scope+DefPins equal; payload includes `score_family_digest = H(score_family_schema_id, score_family_payload)` |
| `characterization` | no MechanismInstance required; characterization / instability / structural claims; certificate optional |
| `perturbation_law` | exactly one LOGICAL dep on `score_construction`; `score_family_digest` MUST equal predecessor.score_family_digest; mechanism_digest; operator; parameter_domain_digest = mechanism.parameter_domain_digest; scope+DefPins equal predecessor |
| `selection_application` | exactly one LOGICAL dep on `perturbation_law`; `score_family_digest` = predecessor.score_family_digest; subject_ref.subject_digest = ApplyOperatorDigest(operator, mechanism, score_family_digest) where ApplyOperatorDigest is the registered schema projection for that operator; mechanism/domain/scope/DefPins equal predecessor |
| `selection_stability` | exactly one LOGICAL dep on `selection_application`; subject/mechanism/domain/scope/DefPins/score_family_digest equal predecessor; guarantee_kind + failure_budget_digest required |
| `perturbation` | optional dep on `perturbation_law`; guarantee_kind required; certificate only if in `certificate_segments` |
| `composition` | ≥1 input: at least one LOGICAL dep on a certificate-segment Claim; ordered deps; `composition_rule_digest`; EvidenceUse(COMPOSITION_INPUT) DERIVED; rule schema defines output subject/mechanism/domain/scope/DefPins/failure_budget/guarantee_core/score_family from inputs — all must validate |
| `selected_object` | exactly one LOGICAL dep on generator ∈ {composition, selection_stability}; subject/mechanism/domain/scope/DefPins equal generator; covering_cert DERIVED = generator |
| `bridge` | see I-BRIDGE-01 |
| `inference` | exactly one BRIDGE dep; exactly one LOGICAL dep on `selected_object`; subject = selected_object.subject = source cert subject; inference_target; failure_budget_digest present |

**I-CHAIN-01:** Missing prior-segment dependency or failed digest-equality projection ⇒ invalid.

**I-CERT-01:** Stability/perturbation: payload guarantee fields equal Claim-level mechanism, domain, subject; MechanismInstance operator+domain match; shared DefPins agree; `guarantee_kind` ∈ `{NEIGHBOR_INDISTINGUISHABILITY, ORACLE_COMPARISON, OTHER_TYPED}`.

**I-COMP-01:** `composition_rule_digest` → CertificateCompositionRule (schema_role=COMPOSITION_RULE), distinct from SelectionOperator.  
Output endpoint completeness: ART-07c **I-COMP-ENDPOINT-01**.

**I-COMP-02:** ≥1 input cert; each input segment ∈ `certificate_segments` (default `{selection_stability, composition}`). Zero-input composition invalid.

**I-OBJ-SEL-01:** selected_object required on inference path (no direct generator skip).

**I-BRIDGE-01:** Inference Claims: unique BRIDGE premise = bridge Claim digest; covering anchor `source_cert_claim_digest = selected_object.covering_cert`; `subject_ref.subject_digest` equals source cert subject.  
**Inference validity beyond covering/subject (endpoint equality + APPLICABLE evaluator):** ART-07c **I-INF-CLAIM-01** (authoritative).  
**All certificate/bridge endpoint typing, transforms, floors, and composition:** ART-07c.

**I-INF-01:** inference_target is schema_role=INFERENCE_TARGET; never aliased to subject_digest.

```text
CertificateCompositionRule
  rule_digest
  rule_schema_id
  rule_payload
  definition_pins[]
```

### 4.3a Embedded transforms + TransformRule

```text
TransformRecord                       # embedded in bridge payload — ART-07c normative carrier
  transform_kind                      # see ART-07c §7 (includes ENDPOINT_CONSTRUCTION)
  input_digest
  output_digest
  rule_payload
  # proof-bound kinds: LOGICAL premise of bridge with matching TransformApplicationDigest (ART-07c)
```

**I-XFORM-01:** Digests recompute; kind + proof binding per ART-07c §7.  
Legacy standalone `TransformRule` / `rule_digest` / `rule_proof_claim_digest` fields are **non-authoritative**.

### 4.3b EvidenceUse

```text
EvidenceUse
  evidence_use_digest                 # = H(consumer, evidence, mediation, slot_id, bridge?)
  consumer_claim_digest
  evidence_claim_digest
  mediation                           # DIRECT | BRIDGE_TRANSFORM | COMPOSITION_INPUT
  slot_id                             # unique per consumer citation slot
  bridge_claim_digest?                # required for BRIDGE_TRANSFORM
```

**I-CERT-02:** At most one EvidenceUse per `(consumer, slot_id)`. Conflicting mediations for same slot invalid.

**I-CERT-02a DIRECT:** equal subject/mechanism/domain/scope/DefPins/guarantee_core; segment pair allowed; schema accepted.

**I-CERT-02b BRIDGE_TRANSFORM:** bridge.valid; source_cert=evidence; transforms OK; subjects digest-exact;  
consumer endpoint + APPLICABLE per ART-07c **I-CERT-TRANSFER-01** (certificate transfer) or **I-INF-CLAIM-01** (inference).

**I-CERT-02c COMPOSITION_INPUT:** DERIVED from ordered LOGICAL deps of composition Claim; slot_id = dependency index; subjects need not match across inputs.

### 4.4 Data dependence (acyclic)

```text
parameter_domain_core = (domain_schema_id, domain_payload_without_dd)
parameter_domain_core_digest = H(parameter_domain_core)

DataDependenceRecord                  # may be embedded in domain or content-addressed
# DdVerificationRecord — ART-11c (authoritative in ART-11c §1)
  dd_digest                           # = H(derivation_schema_id, derivation_payload, parameter_domain_core_digest)
  derivation_schema_id
  derivation_payload
  bound_core_digest                   # MUST equal parameter_domain_core_digest
  class                               # DERIVED

parameter_domain_digest = H(parameter_domain_core_digest, dd_digest)
```

**I-DD-01:** class derived; FIXED only via registered FIXED derivation with no dataset/calibration/adaptive refs.  
**I-DD-02:** bound_core_digest equality required; no circular hash of full domain into DD.  
**I-DD-03:** promotion floors recompute class from dd_digest.

### 4.5 Dependencies

Kinds `LOGICAL | DEFINITIONAL | BRIDGE | UTILITY_CONSTRAINT` — all essential.  
`UTILITY_CONSTRAINT` additionally obeys ART-07c **I-UTIL-02**.

---

## 5. Mechanism instance

```text
MechanismInstance
  mechanism_digest
  joint_law_family
  parameter_domain                    # typed as Claim domains
  selection_operator_digest
  definition_pins[]
  known_failure_cx_classes[]
```

**I-MECH-01:** typed domain (I-SCOPE-02).

---

## 6. Counterexample

```text
Counterexample
  cx_digest
  construct_fingerprint               # H(construct_schema_id, construct_payload)
  refutation_type                     # FULL | PARTIAL | SCOPE_LIMIT
  target_claim_digests[]
  parameter_region                    # typed
  construct_schema_id
  construct_payload
  refutation_witness_digest?          # required for FULL
  archived
  created_event_id
```

**I-CX-01:** Closure hits Claim C if:
1. digest ∈ targets or reachable via RENAMES/EQUIVALENT_TO edges only (I-REL-01/02), **or**
2. `claim_math_fingerprint(C) ∈ {claim_math_fingerprint(t) | t ∈ target_claim_digests}`.  
REVISION_OF/SUPERSEDES do not expand CX closure.

**I-CX-02:** Archive ≠ ignore.  
**I-CX-03:** region typed.  
**I-CX-04:** FULL requires nonempty construct; witness Claim in `refutation_schemas[]`; witness binds construct + targets; `DerivedProofFloor(witness)=CERTIFIED_INFORMAL`. Else draft only.  
**I-CX-05:** FULL type accepted only when I-CX-04 holds.

---

## 7. Status axes

```text
ResearchMaturityRecord                # mutate via ART-13b APPLY_PROMOTION; ART-16b ADVANCE_DEMOTION_WAVE; or ART-16b I-DW-30/33 seed SUPERSEDE on RECORD_COUNTEREXAMPLE(FULL)/START/I-DW-33
  claim_digest
  research_maturity                   # OPEN | CONJECTURE | PARTIAL_RESULT | RESULT | SUPERSEDED

DemotionWave                          # ART-16b; authoritative fields in ART-16b §1
  wave_digest                         # identity; cursor NOT hashed into digest
  trigger_kind                        # FULL_CX | PIN_SUPERSESSION | LEAN_GAP
  trigger_digest
  seeds[]
  work_items[]
  cursor                              # live progress; outside wave_digest

DemotionFloorBreak                    # ART-16b I-DW-25; keyed by claim_digest
  claim_digest
  wave_digest
  intro_event_seq

LeanToolchainHead                     # ART-10b
  toolchain_digest
  mathlib_pin_digest
  set_at_event_id

LeanManifest                          # ART-10b; fields in ART-10b §1
  manifest_digest
  claim_digest


CheckpointRecord                      # ART-17b; authoritative fields in ART-17b §1
  checkpoint_id
  event_seq_max
  merkle_root
  irreversible_head_seq_at_create
  irreversible_head_digest_at_create

IrreversibleReceipt                   # ART-17b
  event_seq
  event_digest
  kind

CycleRecord                           # ART-08d; identity = cycle_digest only (cards/logs outside identity)
  cycle_digest
  target_claim_digest
  phase

QuarantineLock                        # ART-08d
  quarantine_digest

ExampleCard                           # ART-08d
  example_card_digest
  quarantine_digest

FalsifierCard                         # ART-08d
  falsifier_card_digest
  quarantine_digest

AttackLog                             # ART-08d
  attack_log_digest
  cycle_digest
```

```text
EioVetoRecord                         # side table; Commit-derived; ART-13b
  claim_digest
  active                              # true while veto live

EioAssessmentRecord                   # ART-13b RECORD_EIO_ASSESSMENT
  intent_digest
  outcome                             # ALLOW | BLOCK

DisconfirmLog                         # ART-11b RECORD_DISCONFIRM
  disconfirm_digest
  claim_digest
  attempts[]

AuditRecord                           # ART-11b RECORD_AUDIT
  audit_digest
  intent_digest
  answers[]
  verdict
```

Other axis names remain vocabulary for later FSMs but are **derived/display** in Iter1:

| Axis | Iter1 authority |
|------|-----------------|
| proof_status | = DerivedProofFloor |
| counterexample_status | derived from CX closure |
| integration / inference | deferred (Iter9+) |
| lean | ART-10b DerivedLeanStatus / LeanManifest |

**I-PF-04 (DerivedProofFloor):** At most one ProofAttachment per claim_digest (extras invalid).

```text
DerivedProofFloor(C) at state S =
  if ResearchMaturityRecord[C]=SUPERSEDED → UNPROVED   # ART-16b I-DW-23
  else if live DemotionFloorBreak for C and ART-16b I-DW-25 not yet discharged → UNPROVED  # wave-listed or no post-clear ATTACH
  else if ProofAttachment kind=LEAN_REF:               # before CERTIFY — Lean never launders via I-CERTIFY-01
      if live LeanManifest for C and ART-10b DerivedLeanStatus(C) ∈ {LEAN_FULL, LEAN_CORE} → INFORMAL
      else → UNPROVED
  else if ART-04c I-CERTIFY-01 holds for C at S → CERTIFIED_INFORMAL
   else if no valid ProofAttachment → UNPROVED
   else if kind=INFORMAL_STRUCTURED or kind=CERTIFIED_STRUCTURED → INFORMAL
      # CERTIFIED_STRUCTURED without CertificationRecord is still only INFORMAL floor
      # INFORMAL never authorizes discharge, EQUIVALENT_TO, or FULL CX
   else → UNPROVED
```

**I-AX-01:** If FULL CX closure hits C ⇒ ResearchMaturityRecord.research_maturity ∈ {SUPERSEDED, OPEN} and floor ≠ CERTIFIED_INFORMAL.

**I-STATUS-COUPLE (ART-07c / ART-13b):** `research_maturity = RESULT` requires `DerivedProofFloor = CERTIFIED_INFORMAL`. Enforced at APPLY_PROMOTION Commit time (ART-13b I-AP-04).

---

## 8. HumanDecision

**Authoritative schema:** ART-04c §6 only (`HumanDecisionUnsigned` + detached signature; `decision_digest = decision_payload_digest`).  
This artifact does not redefine fields. Claims/commands store `decision_digest` references only.

**I-HD-AUTH / I-CERTIFY:** ART-04c. Former I-HD-01 revoked when ART-04c ACTIVE.

---

## 9. ProofEvidence

```text
ProofEvidence
  proof_evidence_digest               # = H(claim_digest, kind, body_schema_id, body_payload,
                                      #    lemma_claim_digests, proposer_principal_digest?)
                                      # NEVER includes certification_dec_digest (would cycle with ART-04c)
  claim_digest
  kind                                # INFORMAL_STRUCTURED | CERTIFIED_STRUCTURED | LEAN_REF
  body_schema_id
  body_payload
  lemma_claim_digests[]
  proposer_principal_digest?          # required when used as certify input
```

**I-PF-01..03:** lemmas=LOGICAL premises; proofs outside claim_digest; kinds closed enum.  
**I-PF-04:** `DerivedProofFloor` CERTIFIED_INFORMAL only via ART-04c I-CERTIFY-01 (CertificationRecord).  
`certification_dec_digest` is **not** a ProofEvidence field — it lives only on the ATTACH_CERTIFICATION command / event alongside the CertificationRecord.

---

## 10. SchemaRegistry

```text
SchemaRegistryEntry
  schema_id
  schema_digest                       # = H(schema_id, schema_role, schema_body_digest, …)
  schema_body_digest                  # content-addressed typed schema body
  schema_role                         # ASSERTION | DEFINITION_BODY | SYMBOL_TABLE | PROPOSITION
                                      # | SUBJECT | OPERATOR | COMPOSITION_RULE | INFERENCE_TARGET
                                      # | DATA_DEPENDENCE | PROOF_BODY | REGION | CX_CONSTRUCT | …
  applies_to_chain_segments[]
  certificate_segments[]              # which segments may be cited as certificates
  required_assumption_slots[]
  opaque_string_check_result          # DERIVED structural walk (I-DEF-03); must be PASS
  evidence_segment_pairs[]
  accepted_evidence_schema_ids[]
  requires_conclusion_field
  conclusion_proposition_schema_id
  refutation_schemas[]
  equivalence_schemas[]
  # Certificate / inference coherence (ART-07c):
  accepted_notion_kinds[]?            # required on certificate assertion schemas
  accepted_relation_kinds[]?
  allowed_triples[]?                  # (notion_kind, relation_kind, budget_kind)
  allowed_inference_tuples[]?         # (guarantee_kind, conclusion_schema_id, budget_kind,
                                      #  quantifier_schema_id, target_schema_id)
  # ART-11c DATA_DEPENDENCE schemas:
  dd_class_fixed?                     # true ⇒ FIXED; requires allowed_read_kinds=[]
  allowed_read_kinds[]?               # DATASET|CALIBRATION|ADAPTIVE|EXTERNAL_FETCH|OTHER
```

Unknown schema or `opaque_string_check_result≠PASS` ⇒ invalid.

**I-SCH-01 SchemaValid(schema_id, payload):** live SchemaRegistryEntry for `schema_id` with `opaque_string_check_result=PASS`; `payload` nonempty; payload structurally conforms to the typed body identified by `schema_body_digest`; else invalid.

---

## 10A. CandidateResearchPackage & IntakeReceipt (DUAL.2)

Normative registration of ART-CRP intake objects. Sole external mathematical intake into System B. Schema authority remains ART-CRP; this section binds digests into the ART-07b object registry.

```text
CandidateResearchPackage              # immutable once sealed; live row after successful Commit intake
  object_class                        # = CANDIDATE_RESEARCH_PACKAGE
  schema_version                      # "ARTCRP.v1"
  crp_digest                          # = H("ARTCRP.v1", author_kind, author_principal_digest,
                                      #     author_binding_digest_or_⊥, profile, math_scope_pin_digest,
                                      #     payload_canonical, prior_crp_digest_or_⊥)
  author_kind                         # HUMAN | RESEARCH_DISCOVERY_ASSISTANT
  author_principal_digest
  author_binding_digest?              # required if ASSISTANT
  package_phase                       # = profile: PHASE_A_CHARACTERIZATION | PHASE_B_STABILIZATION
                                      #            | MIXED | OBLIGATION_ONLY | BRIDGE_ONLY
  admissibility_state                 # ADMISSIBLE | INADMISSIBLE  # Commit-derived from admissible_package
  source_provenance                   # H(author_kind, author_principal_digest, sealed_at)
  contained_object_refs[]             # draft digests for defs/claims/assumptions/mechs in payload
  intake_status                       # PENDING | ACCEPTED_DRAFT | REJECTED
  commit_event_seq?                   # set on ACCEPTED_DRAFT
  intake_receipt_digest?
  emitted_obligation_digests[]        # ProofObligation digests minted at intake (I-PO-01)
  math_scope_pin_digest
  prior_crp_digest?
  sealed_at
```

```text
IntakeReceipt                         # immutable; EventLog-adjacent
  object_class                        # = INTAKE_RECEIPT
  receipt_digest                      # = H("ARTCRP.IN.v1", crp_digest, event_seq, draft_claim_digests_sorted)
  crp_digest
  event_seq
  draft_claim_digests[]
  status                              # ACCEPTED_DRAFT | REJECTED
  reason_codes[]?
  obligation_digests[]                # copy of emitted_obligation_digests at accept
```

**I-CRP-OBJ-01:** Live `CandidateResearchPackage` rows exist only after successful `SUBMIT_CANDIDATE_PACKAGE` DeriveEffects (or REJECTED receipt with no Research object upserts beyond EventLog receipt).  
**I-CRP-OBJ-02:** `author_kind ∈ {HUMAN, RESEARCH_DISCOVERY_ASSISTANT}` else `CRP_AUTHOR`.  
**I-CRP-OBJ-03:** ART-CRP normative text + this registration are joint authority; conflict ⇒ fail-closed reject intake.

---

## 10B. ProofObligation (DUAL.2)

First-class obligation tracking for CRP-originated (and legacy) claims.

```text
ProofObligation                       # mutable status via Commit only
  obligation_digest                   # = H("ART07b.PO.v1", obligation_id, crp_digest_or_⊥, claim_digest,
                                      #     obligation_type, statement_digest, deps_canonical,
                                      #     assumptions_canonical)
  obligation_id                       # stable id within claim scope
  originating_crp_digest?             # set when minted from CRP intake
  originating_claim_digest
  obligation_type                     # PROOF | DISCHARGE | CX_RELEVANT | BRIDGE_APPLICABILITY
                                      # | CERT_ATTACH | ASSUMPTION_SLOT | OTHER_TYPED
  statement_digest                    # H(statement schema + payload)
  statement_payload                   # typed; SchemaValid
  dependency_digests[]                # claim/def/assumption digests
  assumption_digests[]
  status                              # OPEN | DISCHARGED | WAIVED_HUMAN | FAILED | SUPERSEDED
  discharge_evidence_digests[]        # empty unless DISCHARGED|WAIVED_HUMAN
  cx_relevance                        # NONE | MUST_ATTACK | WITNESS_BOUND
  bridge_relevance                    # NONE | MUST_EVALUATE | BOUND
  blocks_promotion                    # bool — if true, OPEN|FAILED blocks APPLY / certification
  audit_bind_required                 # bool — major_milestone path may require audit covering this
```

**I-PO-01 Intake mint:** On `SUBMIT_CANDIDATE_PACKAGE` ACCEPTED_DRAFT, Commit DeriveEffects MUST mint ≥1 `ProofObligation` per draft claim (at minimum `obligation_type=PROOF` with `blocks_promotion=true` for promotion targets above OPEN), append digests to CRP `emitted_obligation_digests[]` and IntakeReceipt.  
**I-PO-02 Discharge:** `status=DISCHARGED` only with nonempty `discharge_evidence_digests[]` bound under Commit (proof/cert/CX-skip HD as typed).  
**I-PO-03 Promotion gate:** `APPLY_PROMOTION` and `ATTACH_CERTIFICATION` REJECT with `OBLIGATION_UNRESOLVED` if any live obligation with `originating_claim_digest=target` and `blocks_promotion=true` has `status ∈ {OPEN, FAILED}`.  
**I-PO-04 Pipeline (normative):**  
`CandidateResearchPackage → canonical Claims → minted ProofObligations → status tracking → DISCHARGED|WAIVED → promotion eligibility`.  
**I-PO-05 Bindings:** Obligations are ResearchState objects upserted only via ART-06b; CX may reference via `cx_relevance`; bridges via `bridge_relevance`; ART-11b audit may cite obligation digests as evidence; ART-16b demotion may set linked obligations to `FAILED`/`SUPERSEDED`.

---

## 11. Invariants (summary)

| ID | Topic |
|----|-------|
| I-REL-01/02 | Equivalence proved; renames fingerprint-bound |
| I-DEF-01..03 | Pins, historical side-bind, structural opacity check |
| I-ASM-01..03 | NetRequired / CERTIFIED discharge |
| I-FP-01 | Fingerprint includes NetRequiredDigest |
| I-CHAIN-01 | Full chain segment dependencies |
| I-CERT-01/02* | Certificate + EvidenceUse |
| I-COMP-01/02 | Composition rule ≠ selection operator |
| I-OBJ-SEL-01 | Selected object bound to generator |
| I-BRIDGE-01 / I-XFORM-01 | Bridge typing + weakening transforms |
| I-DD-01..03 | Derived data-dependence class |
| I-CX-01..05 | Closure digest+relation+fingerprint; FULL needs CERTIFIED witness |
| I-PF-00..04 | Proof binding; INFORMAL non-authoritative for invalidation |
| I-HD-AUTH / I-CERTIFY | ART-04c — authentic HD; CERTIFIED reachable |
| I-SUB/OP/MECH/SCOPE | Subject/operator/domain typing |
| I-SCH-01 | SchemaValid(schema_id, payload) |
| I-CRP-OBJ-01..03 | CRP + IntakeReceipt registry |
| I-PO-01..05 | ProofObligation mint / discharge / promotion gate |

---

## 12. Ownership (provisional)

All normative objects created only via authoritative mutation boundary (**ART-06b** `I.Commit`). No direct registry poke.

---

## 13. Supersession

| Prior | Status |
|-------|--------|
| ART-07 Bridge sketch | Non-normative |
| ART-09 unary/dual labels | Non-normative until Iter5 |
| ART-06 `from_status/to_status` | Non-normative for promotion |
| Self-attested FIXED / INFORMAL authority / unsigned HD | Revoked by I-DD / I-PF-04 / I-HD-01 |

---

## 14. Deferred (explicit)

| Topic | Iteration |
|-------|-----------|
| Mutation boundary, side-table roots, authenticated transitions | 3 |
| Actor identity, role, independence, HD authenticity, expiry enforcement | 4 |
| Promotion intents, axis transition tables | 5 |
| Audit policy registry | 6 |
| Demotion waves; semantic-equivalence beyond fingerprint | 7 |
| Lean binding for LEAN_REF floor | **CLOSED** Iter8 ART-10b |
| Factual data-provenance completeness | 11 |
| Hash/canonicalization + conformance executable | **CLOSED** Iter12 ART-21b |

## 15. Non-goals

Production implementation; particular DB/language/crypto; expanding math scope beyond the locked chain.
