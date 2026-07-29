# Repair Iteration 1 — Canonical Mathematical Objects

**Normative artifact:** [`../07-schemas/CANONICAL_OBJECTS.md`](../07-schemas/CANONICAL_OBJECTS.md) (`ART-07b`)  
**Frozen version:** `ARCH-0.3-REPAIR-ITER1.26`  
**Gate:** Iteration-1 ready for Iter2? **YES**  
**Independent critiques (Sol `gpt-5.6-sol`):** gate26 / adv26 / math26 / min26 — all PASS (no CRITICAL/HIGH)

**Provenance:** Codex CLI ephemeral, read-only sandbox; critiques archived under `adversarial_review_artifacts/REPAIR_ITER1_CRITIQUE_{gate,adv,math,min}26.txt`.

---

## A. Defects being repaired

From independent breaker audit and Iter1 critique loop:

- Free-text Claims as authority
- Missing content-addressed Claim identity
- Vacuous / untyped definition pins and bodies
- Self-attested dependency “essential” flags; digest cycles via proofs
- Missing ClaimRelation / equivalence rules
- Optional inference bridges; certificate-type laundering
- No assumption closure; unary theorem status
- Forgeable operators, subjects, transforms, data-dependence class
- Self-attested INFORMAL / FULL CX / HumanDecision authority
- Incomplete mathematical chain (missing front segments)
- Composition without certificate inputs; bridge unbound from covering cert
- R20/C12 treated as blueprint clearance

---

## B. Design decisions

1. Claim is immutable and content-addressed; proofs/discharges/historical bindings are side tables.
2. Relatedness is external `ClaimRelation` (RENAMES fingerprint-bound; EQUIVALENT_TO CERTIFIED-only).
3. Dependencies embed premise digests only (DAG-safe); kinds LOGICAL|DEFINITIONAL|BRIDGE.
4. Certificates/utilities/bridges that authorize are Claims (segment-tagged).
5. Full chain segments from `data_regime` through `inference` with digest projections.
6. `DerivedProofFloor` from ProofEvidence; INFORMAL never authorizes discharge/CX/equivalence.
7. `I-HD-01`: HumanDecision non-authoritative until Iter4 (unsigned actor cannot mint gates).
8. Bridge: protected fields equal; only assumption/domain/budget transform; source_cert = selected_object.covering_cert.
9. Data dependence: acyclic via `parameter_domain_core_digest`; class derived, not attested.
10. CX closure: digests + math fingerprint + RENAMES/EQUIVALENT_TO only (not REVISION/SUPERSEDES).

---

## C. Normative definitions

See ART-07b §§1–15: DefinitionVersion, ActiveDefinitionHead, DefPin, Assumption, DischargeRecord, Claim, SubjectRef, SelectionOperator, MechanismInstance, TransformRule/TransformRecord, CertificateCompositionRule, DataDependenceRecord, Counterexample, ResearchMaturityRecord, ProofEvidence, HumanDecision (stub), SchemaRegistry, ClaimRelation, EvidenceUse.

---

## D. Schemas / formal object structures

Encoded as structured field blocks in ART-07b (implementation-neutral). SchemaRegistry roles: ASSERTION, DEFINITION_BODY, SYMBOL_TABLE, PROPOSITION, SUBJECT, OPERATOR, COMPOSITION_RULE, INFERENCE_TARGET, DATA_DEPENDENCE, PROOF_BODY, REGION, TRANSFORM_RULE, ….

---

## E. Invariants

Primary IDs: I-REL-01/02, I-DEF-01..03, I-ASM-01..03, I-FP-01/02, I-CHAIN-01, I-CERT-01/02*, I-COMP-01/02, I-OBJ-SEL-01, I-BRIDGE-01, I-INF-01, I-XFORM-01, I-DD-01..03, I-CX-01..05, I-PF-00..04, I-HD-01, I-SUB/OP/MECH/SCOPE, I-AX-01.

---

## F. Authority and ownership

| Concern | Owner |
|---------|--------|
| Object create/mutate | Authoritative mutation boundary (**Iter3**) |
| Human gate authenticity | **Iter4** (I-HD-01 blocks until then) |
| Axis transitions / promotion | **Iter5** |
| SchemaRegistry design-time entries | Design / gated research |

---

## G. Interfaces

Iteration 1 defines object identity and well-formedness predicates only. Command/event APIs deferred to Iter3.

---

## H. State transitions

Not in scope for Iter1 (FSM = Iter9). ResearchMaturityRecord is a side-table stub; legal transitions Iter5.

---

## I. Failure behavior

Invalid Claims/relations/CX/bridges are rejected by well-formedness predicates (no authoritative write until Iter3). Non-finite Λ and historical/certified gates fail closed under I-HD-01.

---

## J. Validation fixtures

Deferred to Iter12 conformance model. Iter1 acceptance = independent critique PASS on frozen ART-07b text.

---

## K. Cross-document changes

| Doc | Change |
|-----|--------|
| ART-25 / IMPLEMENTATION_BLOCK / 00-README | Blueprint readiness revoked; repair banner; ART-07b normative |
| ART-07 | Subordinate to ART-07b |
| ART-09 | Non-normative until Iter5 |
| Package map | ART-07b added |
| This file | Iteration-1 record |

---

## L. Removed or simplified

- Author `essential` boolean; EMPIRICAL_SUPPORT Claim deps
- Free Bridge sketch as promotion authority
- Unary from/to theorem status as promotion key
- Author-writable `equivalent_fingerprints` on CX
- Ambient subject maps; separate TransformObject lifecycle
- INFORMAL as invalidation/discharge authority
- REVISION_OF/SUPERSEDES as CX closure edges
- Duplicate payload predecessor digests (derived from deps)

---

## M. Open questions (deferred, not blocking)

1. Initial concrete SchemaRegistry entries for baseline noisy-argmin (Iter2 populates certificate/bridge field catalogs).
2. OPERABLE_MINIMAL must list ART-07b (Iter13).
3. ActiveDefinitionHead mutation protocol (Iter3).
4. MEDIUM minimality cleanups (derive more fields; collapse inert stubs) — Iter13.

---

## N. Independent critique findings

| Round | Artifact | Result |
|-------|----------|--------|
| Rechecks 1–25 | iterative CRITICAL closure | archived RECHECK*/gate* |
| gate26 | ITER1.26 | **YES** / No CRITICAL or HIGH |
| adv26 | ITER1.26 | **PASS** |
| math26 | ITER1.26 | **PASS** |
| min26 | ITER1.26 | **PASS** (MEDIUM → Iter13) |

---

## O. Resolution log (accepted)

| Finding | Resolution |
|---------|------------|
| Free-text Claim | assertion_schema + I-DEF-03 structural opacity |
| Def body / symbols | typed DefinitionVersion + symbol_table schema |
| Equivalence / renames | ClaimRelation + I-REL-01/02 |
| Proof in claim digest | side ProofAttachment; I-PF-* |
| INFORMAL authority | I-PF-04; CERTIFIED-only for discharge/CX/equiv |
| Forgeable HD | I-HD-01 non-authoritative until Iter4 |
| Historical cycle | HistoricalScopeBinding side table |
| Operator forgeability | SelectionOperator content-addressed |
| DD self-attest / circular | derived class + domain core digest |
| Missing chain front | data_regime…selection_application segments |
| Score laundering | score_family_digest projections |
| Composition empty/assumptions | ≥1 LOGICAL cert inputs; InheritedRequired |
| Bridge laundering | protected equality + covering_cert anchor |
| CX reissue / poisoning | fingerprint + no author equivalent_fingerprints |
| Revision CX hit | REVISION/SUPERSEDES not CX edges |

**Rejected:** Expanding Iter1 into full identity/auth (Iter4) or Lean rebuild (Iter8).  
**Deferred:** MEDIUM minimality field collapses → Iter13; factual DD completeness → Iter11.

---

## P. Readiness decision for Iteration 2

**YES.**

Iteration 2 may begin: **Typed certificates and bridges** (populate exact certificate/bridge schemas and anti-laundering field catalogs on top of ART-07b ITER1.26).

Do **not** lift IMPLEMENTATION_BLOCK. Do **not** claim DESIGN_FINAL.
