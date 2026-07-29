# Repair Iteration 2 — Typed Certificates and Bridge Theorems

**ART-07c version:** `ARCH-0.3-REPAIR-ITER2.7`  
**Normative draft:** [../07-schemas/TYPED_CERTIFICATES_AND_BRIDGES.md](../07-schemas/TYPED_CERTIFICATES_AND_BRIDGES.md)  
**Depends on:** ART-07b `ARCH-0.3-REPAIR-ITER1.26`  
**Package:** `ARCH-0.3-REPAIR` · **NON-RELEASE**

---

## A. Executive repair summary

Iteration 2 defines digest-native **StabilityCertificate** endpoints and **Bridge Theorems** with explicit relations, notions, failure budgets, transforms, composition, proof-floor coupling, and anti-laundering invariants (ART-07c). Legacy cert/bridge ID dialect is quarantined or pending migration with explicit warnings. RESULT and inference-facing bridge use are **blocked until Iter4** authenticates CERTIFY. Dual-model blocker **B-OBJ-DUAL-01** remains open for non-cert subsystems.

## B. Defects addressed

- Untyped certificate/bridge labels; relation/notion conflation  
- Silent assumption/parameter/budget drop in “bridges”  
- Unproved bridge filling inference slot (rule-level block)  
- RESULT above proof floor (rule-level block pending Iter4)  
- Empirical/conjecture occupying theorem cert slots  
- Silent legacy `cert_id`/`bridge_id` authority (quarantine + warnings)  
- ART-21 false PASS surface; package NON-RELEASE controls  
- Missing comparison/neighbor first-class objects  

## C. Defects explicitly deferred

| Defect | Iteration |
|--------|-----------|
| Mutation kernel / caller booleans | 3, 5 |
| Authenticated CERTIFY / identity | 4 |
| PromotionIntent | 5 |
| Audit intent binding / ART-11 rewrite | 6 |
| Demotion waves / ART-12 align | 7 |
| Lean claim_digest closure | 8 |
| FSM rewrite | 9 |
| Restore trust anchor | 10 |
| Factual DD completeness | 11 |
| Executable fixtures | 12 |
| Minimality consolidation | 13 |
| Release digest / fresh audit | 14 |

## D–K. Models

See ART-07c §§1–10 (certificate, relation, notion, failure budget, bridge, transforms, composition, anti-laundering, status coupling).

## L. Ownership

ART-07c §11 — labels only; Iter4 authenticates.

## M. Interfaces

ART-07c §12: `I.CertificateRegister`, `I.BridgeRegister`, `I.CertificateCompatibilityEvaluate`, `I.BridgeApplicabilityEvaluate`, `I.BridgeComposeEvaluate`.

## N. Failure taxonomy

ART-07c §13.

## O. Validation fixtures

ART-07c §14 (F2-01…F2-18).

## P. Tabletop traces

### TRACE-2A — Valid neighbor cert → proved bridge → inference (research path)
- **Initial:** selection_stability Claim C with REPLACE_ONE_NEIGHBOR + SELECTION_PROB_STABILITY endpoint E; selected_object S; bridge Claim B with transforms; inference Claim I.  
- **Checks:** endpoint recomputes; covering_cert; I-BRIDGE-TRANSFORM-01; floor(B).  
- **Result:** structural OK; if floor(B)<CERTIFIED → inference-valid **blocked** (Iter4); research PROVED bridge visible.  
- **Legacy:** ART-11 must not PASS-authorize via `bridge_id`.  
- **Blockers:** B-BRIDGE-PROOF-01 rule closed for unproved; full close needs Iter4.

### TRACE-2B — Oracle cert offered to neighbor bridge
- **Action:** applicability evaluate.  
- **Result:** RELATION_MISMATCH / INCOMPATIBLE.  
- **Blocked:** inference composition.

### TRACE-2C — Unproved bridge
- **Result:** research-visible PROPOSED/PROVED(INFORMAL); inference-facing → INSUFFICIENT_PROOF_FLOOR / BLOCKED.

### TRACE-2D — Parameter domain change
- **Action:** new cert endpoint; old bridge source_endpoint mismatch.  
- **Result:** STALE / INAPPLICABLE; compositions invalidated.

### TRACE-2E — Bridge superseded by narrower theorem
- **Result:** old bridge SUPERSEDED; dependents STALE; rename cannot bypass (ART-07b).

### TRACE-2F — Legacy ART-11 cert_id/bridge_id
- **Result:** UNTYPED_LEGACY_OBJECT; ART-11 PASS **prohibited** from authorizing promotion; scheduled Iter6; B-AUDIT-BIND-01 open.

## Q. Legacy-artifact migration matrix

| Artifact | Status | Cert/bridge refs | Migration | Prohibited uses | Later iter | Blocker |
|----------|--------|------------------|-----------|-----------------|------------|---------|
| ART-01 | ACTIVE_PARTIAL | inference_facing → ART-07c | redirected | typing authority | 5/9 | — |
| ART-02 | PENDING_MIGRATION | operator transfer / cert_kind | warning banner | typing authority | 5 | — |
| ART-03 | PENDING_MIGRATION | cert-kind vocabulary gate | warning banner | authenticity | 4 | B-IDENTITY |
| ART-04b | PENDING_MIGRATION | day-1 claims/bridges registry | warning: no bridge_id authority | promotion | 3 | B-MUTATION |
| ART-05 / 15 | PENDING_MIGRATION | cert_kind gates | warning | authority authenticity | 3/4 | B-IDENTITY |
| ART-08c | PENDING_MIGRATION | target_cert_kind | warning | blueprint | 9 | — |
| ART-07 | QUARANTINED_LEGACY | all sketches | superseded by 07b/07c | any normative use | — | B-OBJ-DUAL |
| ART-07b | ACTIVE_NORMATIVE | identity; UTILITY_CONSTRAINT; transfer BRIDGE dep; FP-03 | aligned Iter2.6 | — | — | — |
| ART-07c | ACTIVE_NORMATIVE | typing | frozen ITER2.7 | — | — | B-BRIDGE-PROOF partial (Iter4 CERTIFY) |
| ART-08 | PENDING_MIGRATION | hops, psi field | warning | blueprint PASS traces | 9 | B-OBJ-DUAL |
| ART-09 | QUARANTINED_LEGACY | unary status | axes in 07b/07c | promotion tables | 5 | B-STATUS-COUPLE |
| ART-10 | PENDING_MIGRATION | claim_id; cert_kind refusal | warning | Lean clearance | 8 | B-LEAN |
| ART-11 | PENDING_MIGRATION | cert_id, bridge_ids | warning | **promotion authorization** | 6 | B-AUDIT-BIND |
| ART-12 | PENDING_MIGRATION | CX; BRIDGE_OPEN / cert kind | redirected + warning | identity | 7 | B-DEMOTION |
| ART-13 / 18 / 19 / 23 | ACTIVE_PARTIAL | none material | — | — | — | — |
| ART-16/17 | PENDING_MIGRATION | demotion/ckpt | warning | restore clearance | 7/10 | B-DEMOTION, B-RECOVERY |
| ART-20 | PENDING_MIGRATION | rules 2/8 → ART-07c | redirected | full rewrite | 5 | — |
| ART-21 | HISTORICAL_EVIDENCE | T05 etc. | SUPERSEDED_PENDING_REPAIR | readiness | 14 | B-RELEASE-FALSEPASS |
| ART-22 | PENDING_MIGRATION | traces | warning | release evidence | 14 | B-RELEASE |
| ART-24 | PENDING_MIGRATION | interfaces | 07c contracts add | commit boundary | 3 | B-MUTATION |
| ART-25 | ACTIVE_NORMATIVE | pins ART-07c ITER2.7 | posture only | blueprint clearance | 14 | B-RELEASE |
| Info-flow | PENDING_MIGRATION | narrative | warning | authority | 14 | — |
| ART-RBL/RIR/ASI | ACTIVE_NORMATIVE | repair plane | new | — | — | — |

**Temporary compatibility:** Digests authoritative; legacy IDs may appear as explanatory aliases only if bound 1:1 to digests (ART-07b). Unbound IDs → quarantine.  
**Undocumented assumptions:** None intended; missing classification → QUARANTINED_LEGACY (ART-RIR).

## R. Cross-document changes

Package NON-RELEASE banner; ART-21/25 reset; warnings on ART-06–12,16,17,24,info-flow; ART-07b I-STATUS-COUPLE pointer; 00-repair control plane; ART-07c created.

## S. Quarantined artifacts

ART-07 (legacy schemas), ART-09 (unary FSM).

## T. Active incompatibility warnings

Listed on ART-06,07,08,09,10,11,12,16,17,21,24, ARCHITECTURE_INFORMATION_FLOW.

## U. Independent review findings

| Review | Status | Evidence |
|--------|--------|----------|
| A Adversarial | **PASS** | `adversarial_review_artifacts/REPAIR_ITER2.7_REVIEW_adv.txt` (also `REPAIR_ITER2_REVIEW_adv.txt`) |
| B Math | **PASS** | `…/REPAIR_ITER2.7_REVIEW_math.txt` |
| C Minimality | **PASS** | `…/REPAIR_ITER2.7_REVIEW_min.txt` |
| D Integration | **PASS** | `…/REPAIR_ITER2.7_REVIEW_integ.txt` |

Prior waves archived: ITER2.1 (FAIL), 2.2–2.6 (FAIL until closed). No open Critical/High on ITER2.7.

## V. Resolution log

| Item | Resolution |
|------|------------|
| CompatibilityPolicy laundering | Removed; exact endpoint match only |
| Incomplete transforms / quantifier / hetero budgets | TransformRecord kinds + ENDPOINT_CONSTRUCTION |
| Unproved source / unbound applicability | I-INF-CLAIM-01 + floors; transfer I-CERT-TRANSFER-01 |
| Proof-bound unrelated theorems / context laundering | LOGICAL premise + set inclusion onto E_out |
| Structural field smuggling | I-XFORM-STRUCT-02 closed write sets |
| Composition endpoint relabel | I-COMP-HOMOGENEITY-01 / I-COMP-ONE-INPUT-01 |
| Utility under-typed / unbound | Claim-only + mandatory signature I-UTIL-02 |
| SchemaRegistry missing triples | allowed_triples / allowed_inference_tuples on ART-07b |
| Claim↔InferenceEndpoint dual | I-INF-CLAIM-PROJECTION-01 |
| Legacy silent consumers | Warnings ART-01/02/03/04b/10/12/20; matrix scheduled |

## W. Blocker ledger update

See `00-repair/BLOCKER_LEDGER.md`. B-BRIDGE-PROOF-01 / B-STATUS-COUPLE-01 remain **partial** (rules normative; CERTIFY unreachable until Iter4). Dual-model and mutation blockers open for Iter3+.

## X. Iteration 2 completion decision

**YES — COMPLETE.**

ART-07c `ARCH-0.3-REPAIR-ITER2.7` is `ACTIVE_NORMATIVE`. Independent Sol reviews A–D PASS with no remaining Critical/High.

## Y. Authorization to begin Iteration 3

**AUTHORIZED.**

Package remains **NON-RELEASE**; `IMPLEMENTATION_BLOCK` ACTIVE; `DESIGN_FINAL` revoked; blueprint / implementation planning still **no**.
