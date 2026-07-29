# 07c — Typed Stability Certificates and Bridge Theorems (Normative)

**Artifact ID:** `ART-07c`  
**Version:** `ARCH-0.3-REPAIR-ITER2.7`  
**Normative status:** `ACTIVE_NORMATIVE` (Iteration 2 complete; Sol reviews A–D PASS on ITER2.7)  
**Depends on:** `ART-07b` `ARCH-0.3-REPAIR-ITER1.26` (+ narrow SchemaRegistry / FP / I-BRIDGE updates in this package)  
**Supersedes for cert/bridge typing:** ART-07 sketches; ART-06 `cert_id`/`bridge_id` identity; ART-11 untyped bridge status for promotion; ART-07b I-BRIDGE typing beyond covering+subject  
**Authority:** Design material. Changes reset Iteration-2 readiness.

## Purpose

Exact typed, digest-native certificates and Bridge Theorems. No label interchange. No CompatibilityPolicy. Certificate = ART-07b Claim. No parallel cert/bridge lifecycle axes — floors + evaluator results only.

## Scope lock

Fixed research chain only. Neighbor / oracle / DP / robustness / utility / coverage / generalization / policy validity are never interchangeable without an explicit Bridge Theorem.

---

## 1. Theorem certificate

A theorem-level stability certificate **is** an ART-07b `Claim` with `chain_segment ∈ certificate_segments`.

**I-CERT-EMP-01:** Empirical-only evidence or `research_maturity=CONJECTURE` without theorem ProofAttachment MUST NOT occupy theorem certificate endpoints or inference-facing bridge sources.

No `StabilityCertificateInstance`, no author `CertificateEpistemicClass`, no bridge lifecycle enum.

---

## 2. ComparisonRelation

```text
ComparisonRelation
  relation_digest                     # = H(normative fields)
  relation_schema_id                  # schema_role=COMPARISON_RELATION
  relation_kind                       # REPLACE_ONE_NEIGHBOR | ADD_REMOVE_ONE_NEIGHBOR
                                      # | BOUNDED_OBS_PERTURB | ORACLE_COMPARISON
                                      # | SCORE_VECTOR_PERTURB | PARAMETER_PERTURB
                                      # | CANDIDATE_SET_PERTURB | DISTRIBUTIONAL_COMPARISON
                                      # | ALGORITHM_RANDOMNESS_COMPARISON | OTHER_TYPED
  domain_schema_id / domain_payload
  directionality                      # SYMMETRIC | DIRECTED
  adjacency_or_metric
  radius_or_budget?                   # required when kind has radius
  quantified_objects[]
  exclusions[]
  definition_pins[]
```

**I-CERT-RELATION-01:** Each certificate Claim binds exactly one `relation_digest`.

---

## 3. StabilityNotion

```text
StabilityNotion
  notion_digest
  notion_schema_id                    # schema_role=STABILITY_NOTION
  notion_kind                         # DP | APPROX_DP | MAX_INFO_LIKE | UNIFORM_STABILITY
                                      # | LOO_STABILITY | SELECTION_PROB_STABILITY | RANKING_STABILITY
                                      # | ARGMIN_OUTPUT_STABILITY | ORACLE_STABILITY
                                      # | DISTRIBUTIONAL_ROBUSTNESS | EXPECTED_REGRET_ROBUSTNESS
                                      # | HP_DECISION_STABILITY | OTHER_TYPED
  quantifier_structure                # typed AST
  quantifier_digest                   # = H(quantifier_structure)
  guarantee_statement_schema_id
  guarantee_statement_payload
  definition_pins[]
```

**I-NOTION-01:** Distinct notions incompatible unless bridged.  
Legacy ART-07b `guarantee_kind` = coarse projection of `notion_kind` only.

---

## 4. FailureBudget

```text
FailureBudget
  failure_budget_digest
  budget_schema_id                    # schema_role=FAILURE_BUDGET
  budget_kind                         # EPSILON_DELTA | ETA_TAU | PROB_NU | TV
                                      # | COVERAGE_ERROR | GENERALIZATION_GAP | OTHER_TYPED
  budget_payload
  definition_pins[]
```

Same-kind ordering: registered partial order (larger = weaker where applicable).  
Cross-kind: only via `HETEROGENEOUS_BUDGET_MAP`, never via ≤ on incomparable kinds.

---

## 5. CertificateEndpoint (derived)

```text
CertificateEndpoint                   # recomputed; never author-authority
  endpoint_digest                     # = H(all fields below)
  notion_digest
  relation_digest
  quantifier_digest
  selected_object_class
  selection_operator_digest
  score_family_digest?
  mechanism_digest?
  candidate_domain_digest
  data_domain_digest
  parameter_domain_digest
  NetRequiredDigest
  DefPinMultisetDigest
  mathematical_scope_digest
  failure_budget_digest
  exclusions_digest
```

**I-CERT-IDENTITY-01 / I-CERT-ENDPOINT-01 / I-CERT-SCOPE-01:** identity = claim_digest; one endpoint; use only under exact match or Bridge.

**I-CERT-COHERENCE-01:** Certificate assertion schemas MUST declare `allowed_triples[]` of `(notion_kind, relation_kind, budget_kind)` on ART-07b `SchemaRegistryEntry`. Outside list → invalid.

**I-CERT-PROOF-01:** Usable certificate status ≤ `DerivedProofFloor(claim)`.

**I-CERT-SOURCE-FLOOR-01:**  
`use_class=INFERENCE_FACING` ⇒ source floor ≥ `CERTIFIED_INFORMAL` (unreachable until Iter4 ⇒ blocked).  
`use_class=RESEARCH` ⇒ source floor ≥ `INFORMAL`.

**I-CERT-DD-01:** Data-independence / FIXED certificate uses require ART-11c I-DDV-01 VERIFIED **and** I-DDV-11; else `DD_BLOCKED` / `DD_CORE_MISMATCH`.

---

## 6. InferenceEndpoint (target signature)

```text
InferenceEndpoint
  inference_endpoint_digest           # = H(all stored fields below)
  inference_guarantee_kind
  target_schema_id
  target_payload
  # inference_target_digest DERIVED = H(target_schema_id, target_payload)
  conclusion_schema_id
  conclusion_payload
  quantifier_schema_id
  quantifier_payload
  # quantifier_digest DERIVED = H(quantifier_schema_id, quantifier_payload)
  subject_digest
  covering_cert_digest
  data_domain_digest
  parameter_domain_digest
  NetRequiredDigest
  DefPinMultisetDigest
  failure_budget_digest
  mathematical_scope_digest
  exclusions_digest
```

**I-INF-EP-01:** Missing guarantee_kind / conclusion / target or quantifier carriers → invalid.

**I-INF-COHERENCE-01:** `allowed_inference_tuples[]` of  
`(inference_guarantee_kind, conclusion_schema_id, budget_kind, quantifier_schema_id, target_schema_id)`. Outside → invalid.

**I-INF-CLAIM-PROJECTION-01:** For inference Claims, overlapping fields MUST equal ART-07b Claim carriers exactly:  
`subject_digest = subject_ref.subject_digest`,  
`parameter_domain_digest = claim.parameter_domain_digest`,  
`mathematical_scope_digest = H(claim.mathematical_scope)`,  
`NetRequiredDigest` / `DefPinMultisetDigest` / `failure_budget_digest` = Claim-level digests,  
`ConclusionDigest(claim) = H(conclusion_schema_id, conclusion_payload)`,  
derived `inference_target_digest` equals Claim `inference_target` digest projection.

---

## 7. Transforms (on TransformRecord; no separate TransformRule object)

```text
TransformRecord                       # embedded in bridge payload
  transform_kind
  input_digest
  output_digest
  rule_payload                        # typed formula / applicability domain / field map
  # proof authorization: a LOGICAL premise P of the bridge Claim with
  # ConclusionDigest(P) = TransformApplicationDigest (no separate pointer field)
```

```text
transform_kind ∈
  ASSUMPTION_MAP              # out NetRequired ⊇ in (weakening); structural; no proof claim
  PARAMETER_MAP               # out domain ⊆ in; structural
  FAILURE_BUDGET_MAP          # same budget_kind; out ≥ in; structural
  HETEROGENEOUS_BUDGET_MAP    # proof-bound
  QUANTIFIER_MAP              # proof-bound; no silent strengthening
  NOTION_MAP                  # proof-bound; CertificateEndpoint→CertificateEndpoint only
  RELATION_MAP                # proof-bound; CertificateEndpoint→CertificateEndpoint only
  OPERATOR_MAP                # proof-bound; CertificateEndpoint→CertificateEndpoint only
  IDENTITY                    # in_digest = out_digest
  ENDPOINT_CONSTRUCTION       # proof-bound; CertificateEndpoint → InferenceEndpoint ONLY
```

**I-XFORM-STRUCT-01:** Structural kinds: digests + `rule_payload` must satisfy the kind’s order/restriction predicate.

**I-XFORM-STRUCT-02 (closed write set):** For structural kinds, the **only** CertificateEndpoint fields that may differ between input and output are:
- `ASSUMPTION_MAP` → `NetRequiredDigest` (and dependent fingerprint projections of it)
- `PARAMETER_MAP` → `parameter_domain_digest`
- `FAILURE_BUDGET_MAP` → `failure_budget_digest`
All other endpoint fields MUST be byte-identical. Any other change requires a proof-bound map of the appropriate kind.

**I-XFORM-PROOF-01 (proof-bound kinds):** There MUST exist a unique LOGICAL premise P of the bridge Claim with  
`ConclusionDigest(P) = TransformApplicationDigest = H(transform_kind, input_digest, output_digest, rule_payload)`  
and `DerivedProofFloor(P)` meeting use_class floor.

**I-XFORM-PROOF-02 (context closure onto target endpoint):** Let `E_out` be the CertificateEndpoint or InferenceEndpoint after this transform step (final target for last step).  
Let `NetRequiredSet(X)` be the assumption-digest set whose hash is `NetRequiredDigest(X)` (ART-07b).  
Require set inclusion / equality (not digest⊆digest):  
- `NetRequiredSet(P) ⊆ NetRequiredSet(E_out)` (for InferenceEndpoint, NetRequiredSet from its NetRequiredDigest carrier)  
- `DefPinSet(P) ⊆ DefPinSet(E_out)`  
- `P.mathematical_scope_digest = E_out.mathematical_scope_digest`  
- `P.parameter_domain_digest = E_out.parameter_domain_digest`  
(If a `PARAMETER_MAP` precedes this step, equality is to the post-map mid endpoint that is this step’s input.)

**I-BRIDGE-NO-DROP-01:** No silent drop of assumptions, quantifiers, pins, exclusions, or budget contributions not justified by a recorded map.

*(ART-07b may retain a legacy `TransformRule` sketch; ART-07c normative transform carrier is `TransformRecord` only.)*

---

## 8. Bridge Theorem (`chain_segment=bridge`)

### 8.1 Class (derived — no stored `bridge_class`)

```text
BridgeClass(B) =
  INFERENCE_BRIDGE              if target resolves as InferenceEndpoint
  CERTIFICATE_TRANSFER_BRIDGE   if target resolves as CertificateEndpoint
```

Author-supplied class field is forbidden (duplicate discriminator).

### 8.2 Payload (minimal; mirrors forbidden)

```text
BridgeTheoremPayload
  source_cert_claim_digest            # authoritative source
  transforms[]                        # TransformRecord+
  # DERIVED (must recompute; not independently authoritative if stored):
  #   source_endpoint_digest = CertificateEndpoint(source_cert).endpoint_digest
  #   target_endpoint_digest = see §8.3
  #   source_subject_digest / covering_anchor for INFERENCE_BRIDGE
```

Definition pins live on the bridge Claim (`definition_pins[]`), not duplicated in payload.

### 8.3 Recomputation

**CERTIFICATE_TRANSFER_BRIDGE**  
`pre = CertificateEndpoint(source)`  
Apply only CertificateEndpoint→CertificateEndpoint maps in order (no `ENDPOINT_CONSTRUCTION`).  
`target_endpoint_digest` MUST equal final endpoint digest.

**INFERENCE_BRIDGE**  
1. `pre = CertificateEndpoint(source)`  
2. Apply zero or more CertificateEndpoint→CertificateEndpoint maps → `mid`  
3. Exactly one `ENDPOINT_CONSTRUCTION` with `input_digest=mid.endpoint_digest`  
   and `output_digest = InferenceEndpoint.inference_endpoint_digest`  
4. `target_endpoint_digest` MUST equal that output  
5. Carryover equalities forced by construction `rule_payload` MUST include at least:  
   `subject_digest`, `covering_cert_digest (= source_cert_claim_digest)`,  
   and post-map `data_domain`, `parameter_domain`, `NetRequired`, `DefPins`,  
   `failure_budget`, `mathematical_scope`, `exclusions` as declared by the construction schema  
6. Inference-only fields (`inference_guarantee_kind`, `inference_target_digest`, conclusion, inference quantifier)  
   appear only in the construction output / bridge Claim conclusion — never injected outside the proved construction

**I-BRIDGE-IDENTITY-01:** identity = bridge `claim_digest`.  
**I-BRIDGE-MATCH-01:** available cert endpoint **exactly equals** derived `source_endpoint_digest`.  
**I-BRIDGE-TRANSFORM-01:** target equals recomputation above (not “apply every map fieldwise across mismatched shapes”).  
**I-BRIDGE-COVER-01:** INFERENCE_BRIDGE ⇒ `source_cert_claim_digest = selected_object.covering_cert`  
and `InferenceEndpoint.covering_cert_digest = source_cert_claim_digest`.

### 8.4 Use class and floors

```text
use_class ∈ { RESEARCH | INFERENCE_FACING }
```

| use_class | Bridge floor | Source cert floor |
|-----------|--------------|-------------------|
| RESEARCH | ≥ INFORMAL | ≥ INFORMAL |
| INFERENCE_FACING | = CERTIFIED_INFORMAL | = CERTIFIED_INFORMAL |

Until Iter4: CERTIFIED unreachable ⇒ **INFERENCE_FACING always blocked**.  
No `INDEPENDENTLY_CERTIFIED` / `OPEN` / `ASSUMED` lifecycle labels.

### 8.5 Consumer binding

**I-INF-CLAIM-01:** An inference Claim is valid only if all hold:  
1. Unique BRIDGE dep = bridge Claim B; unique LOGICAL dep on `selected_object` S (ART-07b).  
2. ART-07b covering + subject equalities.  
3. Claim’s `InferenceEndpoint.inference_endpoint_digest` = B’s derived `target_endpoint_digest`.  
4. `I.BridgeApplicabilityEvaluate(B, source_cert, target_endpoint, use_class=INFERENCE_FACING, ctx) = APPLICABLE`.  

**I-CERT-TRANSFER-01:** A certificate-segment Claim C that cites evidence via `EvidenceUse.mediation=BRIDGE_TRANSFORM` through bridge B is valid only if:  
1. B is `CERTIFICATE_TRANSFER_BRIDGE` (derived).  
2. C has a `BRIDGE` dependency on B.claim_digest.  
3. `CertificateEndpoint(C).endpoint_digest` = B’s derived `target_endpoint_digest`.  
4. `I.BridgeApplicabilityEvaluate(B, source_cert, CertificateEndpoint(C), use_class, ctx) = APPLICABLE`.  
5. Context inheritance: `NetRequiredSet(B) ⊆ NetRequiredSet(C)`, `DefPinSet(B) ⊆ DefPinSet(C)`,  
   and C equals B’s target endpoint on `mathematical_scope_digest` and `parameter_domain_digest`.

---

## 9. Utility (Claim only)

Utility assertions that constrain validity are **Claims** (assertion schema family `UTILITY_*`).

Payload fields that are **not** duplicated from the Claim carrier (subject_ref, parameter_domain, definition_pins, ConclusionDigest):

```text
UtilityStatement                      # assertion_payload only
  loss_kind                           # SCORE_LOSS | POLICY_LOSS | OTHER_TYPED
  comparator_digest
  threshold_payload
  quantifier_digest
  data_domain_digest?                 # required when loss depends on dataset identity
```

**I-UTIL-01:** Validity ≠ utility.  
**I-UTIL-02:** `CONSTRAINT_INPUT` = Claim dependency `kind=UTILITY_CONSTRAINT` citing utility Claim U.  
Every such consumer’s assertion schema MUST declare required utility-signature slots  
`(loss_kind, comparator_digest, threshold_payload, quantifier_digest)` (and `data_domain_digest` when U carries one).  
Compatibility (computable):  
- `consumer.subject_ref.subject_digest = U.subject_ref.subject_digest`  
- `consumer.parameter_domain_digest = U.parameter_domain_digest`  
- `H(consumer.mathematical_scope) = H(U.mathematical_scope)`  
- `DefPinSet(U) ⊆ DefPinSet(consumer)`  
- consumer’s required utility-signature slots MUST equal U’s `UtilityStatement` fields exactly  
- if U has `data_domain_digest`, consumer’s declared slot equals it  
- `DerivedProofFloor(U)` ≥ floor for evaluator `use_class`  
Omitting signature slots on a `UTILITY_CONSTRAINT` consumer ⇒ invalid Claim.  
**EXCLUDED** = exclusion digest on endpoint.  
**INDEPENDENT_AXIS** = no `UTILITY_CONSTRAINT` dep.

---

## 10. Evaluator outputs (not persisted types)

### I.CertificateRegister
Validate cert Claim: coherence triple, endpoint recompute, EMPIRICAL ban, DD, floor.

### I.BridgeRegister
Validate bridge Claim: match, recomputation §8.3, no-drop, covering, floors, transform proof binding.

### I.EndpointMatchEvaluate
Exact match only → EXACT_MATCH | MISMATCH + field diffs.

### I.BridgeApplicabilityEvaluate
**In:** bridge digest, source cert digest, target requirement digest, **use_class**, context digest.  
**Out:** APPLICABLE | INAPPLICABLE | STALE | INSUFFICIENT_PROOF_FLOOR | BLOCKED  
Result digest binds observed floors, use_class, recomputed endpoints.  
`REFUTED` / `SUPERSEDED` are ClaimRelation / research_maturity states — **not** applicability outputs.

### I.BridgeComposeEvaluate
Ordered bridges + source endpoint + use_class → composed target + cumulative digests + min_floor | INVALID.  
LOSSY/PARTIAL without residual schema → INVALID for INFERENCE_FACING.

---

## 10b. Certificate composition (endpoint-complete)

**I-COMP-ENDPOINT-01:** `CertificateCompositionRule.rule_payload` MUST define a total projection to a full `CertificateEndpoint` (all §5 fields).  
**I-COMP-HOMOGENEITY-01:** All composition inputs MUST share equal `notion_digest`, `relation_digest`, and `quantifier_digest`.  
Otherwise INVALID — obtain homogeneity first via `CERTIFICATE_TRANSFER_BRIDGE` / proof-bound maps; composition itself MUST NOT relabel those fields.  
**I-COMP-ONE-INPUT-01:** One-input composition ⇒ output endpoint digest equals input endpoint digest (IDENTITY only). Any intended change is a Bridge, not composition.

---

## 11. Proof-floor / maturity

**I-STATUS-COUPLE-01:** `research_maturity=RESULT` ⇒ `DerivedProofFloor=CERTIFIED_INFORMAL` (enforced by ART-13b APPLY_PROMOTION).  
Inference-facing use gated by §8.4 floor table + CERTIFIED path (ART-04c) — **not** a separate lifecycle write in Iter5.

---

## 12. Fingerprint projection (ART-07b I-FP-01 / I-FP-03)

```text
endpoint_digest for claim_math_fingerprint =
  certificate_segments → CertificateEndpoint.endpoint_digest
  bridge               → H(source_endpoint_digest, target_endpoint_digest)
  inference            → InferenceEndpoint.inference_endpoint_digest
  other                → ⊥
```

---

## 13. Anti-laundering (summary)

Exact source match; typed transforms + closed structural write sets; ENDPOINT_CONSTRUCTION; proof conclusion + LOGICAL dep + NetRequired/pin/scope closure; inference/transfer consumers bound to target + APPLICABLE; composition endpoint-complete; no CompatibilityPolicy; no empirical→theorem; fingerprint §12; legacy IDs quarantined.

---

## 14. Ownership

Schema steward; mathematical author; proof producer; independent certifier (Iter4); integration auditor (policy); committer (Iter3). Labels ≠ authority until Iter4.

---

## 15. Failure taxonomy

UNKNOWN_SCHEMA | INCOMPLETE_NORMATIVE | DIGEST_MISMATCH | RELATION_MISMATCH | NOTION_MISMATCH | OBJECT_MISMATCH | OPERATOR_MISMATCH | PARAMETER_DOMAIN_MISMATCH | ASSUMPTION_MISMATCH | DEFINITION_PIN_MISMATCH | QUANTIFIER_MISMATCH | FAILURE_BUDGET_MISMATCH | COHERENCE_TRIPLE_INVALID | INFERENCE_TUPLE_INVALID | PROOF_FLOOR_INSUFFICIENT | TRANSFORM_PROOF_MISMATCH | STALE_* | SUPERSEDED_* | REFUTED_CLAIM | INVALID_COMPOSITION | UNTYPED_LEGACY_OBJECT | EMPIRICAL_IN_THEOREM_SLOT | DD_BLOCKED | STATUS_COUPLE_VIOLATION | HETEROGENEOUS_MAP_UNBOUND | UTILITY_CONSTRAINT_INCOMPLETE | ENDPOINT_CONSTRUCTION_MISSING | INFERENCE_TARGET_MISMATCH | APPLICABILITY_NOT_APPLICABLE

---

## 16. Fixtures F2-01…F2-18

Same intents; F2-02 exact mismatch; F2-05 DP→coverage requires proved `ENDPOINT_CONSTRUCTION` (+ optional prior budget/quantifier maps); F2-09 unproved bridge/source → INSUFFICIENT_PROOF_FLOOR / inference Claim invalid under I-INF-CLAIM-01.

---

## 17. ART-07b alignment (narrow)

- I-BRIDGE-01: covering + subject; **I-INF-CLAIM-01** here for inference validity.  
- TransformRecord normative carrier (§7); TransformRule sketch non-authoritative for Iter2.  
- SchemaRegistryEntry: `allowed_triples`, `allowed_inference_tuples`, accepted kind lists.  
- I-FP-01/03: endpoint projection §12.  
- I-STATUS-COUPLE: floors only (no lifecycle dialect).

---

## 18. Non-goals

Iter3 mutation; Iter4 CERTIFY authenticity; Iter5–14 as listed in repair mandate.
