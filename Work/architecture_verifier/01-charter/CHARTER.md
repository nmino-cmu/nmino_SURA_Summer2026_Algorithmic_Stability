# 01 — Shared Area-1 Constitution

**Artifact ID:** `ART-01`  
**Owner:** Human (charter) · maintained for consistency by design orchestrator  
**Version:** `ARCH-0.3-REPAIR-DUAL.1`  
**Normative status:** `ACTIVE_PARTIAL`  
**Authority:** Immutable except by human gate `SCOPE_CHANGE` or `DESIGN_FINAL` amendment

> **DUAL-SYSTEM (DUAL.1):** This file is the **shared Area-1 constitution** (scope + boundary predicates).  
> System B mission charter = [ART-01V](CHARTER_VERIFICATION.md).  
> System A mission charter = [ART-01D](CHARTER_DISCOVERY.md).  
> External math intake = [ART-CRP](../24-interfaces/CANDIDATE_RESEARCH_PACKAGE.md).

> **INCOMPATIBILITY WARNING:** Legacy `cert_kind` / bridge status labels **non-authoritative** (ART-07c). Caller `*_ok` **non-authoritative** (ART-06b). Discovery engines are **not** on the Verification Architecture normative path.

## Purpose

Bind **both** System A (Discovery Assistant) and System B (Verification Architecture) to one mathematical research program and shared boundary predicates.

## Scope (immutable)

**STRUCTURED PERTURBATION DESIGN FOR FINITE-CANDIDATE OPTIMIZATION-BASED SELECTION**, with formal stability and utility certificates and a verified extension path to post-hoc inference and constrained-optimization-selected policies — **including Phase A characterization / instability work that does not yet introduce a perturbation mechanism** (ART-CRP).

## Goals (shared program)

1. Preserve fixed mathematical scope.  
2. Maintain versioned formal definitions.  
3. Allow discovery (A) to propose conjectures / mechanisms / characterization results via CRP.  
4. Require verification (B) to attack, audit, certify, and promote — never invent the next question.  
5. Construct minimal symbolic/analytic test problems (via CRP).  
6. Search aggressively for counterexamples (B).  
7. Separate proved / partial / conjectural / false claims.  
8. Audit end-to-end chain compatibility.  
9. Formalize mature claims in Lean under staged statuses.  
10. Persist institutional memory indefinitely.  
11. Escalate scope, certificate-type, novelty, and inference claims to humans.  
12. Produce documents suitable for human mathematical review.

## Non-goals

Generic scientific discovery outside Area-1; generic autonomous coding; treating B as an autonomous inventor; bypassing CRP intake into ResearchState.

## System split

| System | Charter | May invent? | May Commit ResearchState? |
|--------|---------|-------------|---------------------------|
| A Discovery | ART-01D | Yes | No — only submit CRP |
| B Verification | ART-01V | No | Yes — via I.Commit |

## Boundary predicates (Area-1 authority — hard)

Downstream milestone / experiment / import language **must** resolve to these predicates (or ART-CRP `admissible_package` for new intake).

### `external_theorem(t)`

True iff **all** hold:

1. Statement originates outside this program’s `theorem_dag` authorship (literature / textbook / prior paper)  
2. Entered only as `IMPORTED_RESULT` with `IMPORTED_RESULT_REGISTER` on **first** use **and** on any re-frame that changes assumption map, formalization mapping, or chain role  
3. May appear in dependency closure / Lean imports  
4. **Must not** alone satisfy Q15 chain-advancement or count as a research contribution — contribution requires an in-program claim on the charter chain  

False → treat as in-program conjecture/claim subject to full cycle obligations.

### `admissible_package(crp)` (primary for new work)

Defined in ART-CRP. Preferred gate for DUAL.1+ intake. Supports Phase A without MechanismInstance.

### `admissible_experiment(cycle_id)` (legacy cycles)

True iff **all** hold before `S02` lock / `S04` entry on a **legacy** ART-08d cycle (ART-CRP I-CRP-20):

1. `quarantine[q_id].chain_link ∈ {characterization, perturbation, stability, composition, object, inference, bridge}` (required; narrative alone fails)  
   - If `chain_link=bridge`: quarantine `class` **must** be `BRIDGE_CANDIDATE` with `SCOPE_CHANGE`/`exc_id` as below — **not** `IN_CHAIN`  
   - Else: targets the named charter chain hop (or `BRIDGE_CANDIDATE` path below)  
2. Finite \(\Lambda\); analytic/symbolic primary (MC `auxiliary_only` if used)  
3. Quarantine status ∈ `{IN_CHAIN, BRIDGE_CANDIDATE}` resolved from registry `quarantine[q_id]` — unset / missing row **fails**  
   - `IN_CHAIN`: requires `classifier_role ∈ {Verification_Orchestrator, EIO, Research_Scope}` (DUAL.1: prefer CRP intake first); **`chain_link ≠ bridge`**  
   - `BRIDGE_CANDIDATE`: requires human `SCOPE_CHANGE` (or `exc_id` sunset exception)  
4. `scope_exceptions` entry, if any, has schema `{exc_id, reason, sunset_cycle, human_gate_id}` and is not expired  
5. `loop_tag ≠ SIMULATION` when writing ResearchState  

False → reject cycle entry / no ResearchState commit.

**S04:** ExampleCard must include `chain_link_intent = quarantine[q_id].chain_link` (hard reject mismatch). After S04 entry, `chain_link_intent` is **frozen**.  
**S03:** FalsifierCard.`chain_segment` must equal `quarantine[q_id].chain_link` **and** ExampleCard.`chain_link_intent` (hard reject mismatch). After S03 entry, `chain_segment` is **frozen**.  
**Re-check:** Card fields vs frozen `quarantine.chain_link` must be **derived inside ART-06b `I.Commit`**.  

**Quarantine immutability:** After `S02` lock, `quarantine[q_id].{chain_link, class, classifier_*, frozen_at_s02}` is **frozen** until cycle terminate/close.

### Facing predicates (for `major_milestone`)

- **`inference_facing(claim)`** iff `chain_segment=inference`  
  **or** ART-07c `InferenceEndpoint.inference_guarantee_kind ∈ {POSTHOC_COVERAGE, POSTHOC_GENERALIZATION, SELECTIVE_LIKELIHOOD}`  
  **or** claim has a BRIDGE dependency for which ART-07c `I.BridgeApplicabilityEvaluate(..., use_class=INFERENCE_FACING)` returns a result other than APPLICABLE  
- **`policy_facing(claim)`** iff `chain_segment=selection_stability` **and** `subject_ref.object_class = POLICY`  
- **`characterization_facing(claim)`** iff `chain_segment=characterization`

### `major_milestone(claim_id, promotion_tx)`

True iff **any** of:

1. Promotion target ∈ `{PARTIAL_RESULT, RESULT}`  
2. `inference_facing(claim)`  
3. `policy_facing(claim)`  
4. Novelty alignment ≥ `PLAUSIBLE_NOVELTY`  
5. `characterization_facing(claim)` ∧ promotion target ∈ `{PARTIAL_RESULT, RESULT}`

When true: ART-15 RequiredGates apply at APPLY (ART-13b). ART-11b I-BIND-01 and ART-08d I-AP-14 are APPLY predicates while ACTIVE.

**Stability milestone** = `major_milestone` ∧ `chain_segment` ∈ `{stability, selection_stability}`.  
**Characterization milestone** = `major_milestone` ∧ `characterization_facing(claim)` — does **not** require MechanismInstance.

### Design convergence

Defined only in `ART-20b` (C1–C14). Material change to these predicates **resets** C12.

## Invariants

- Phase B / MIXED stabilization claims that assert neighbor/oracle guarantees still sit on: perturbation → selection stability → composition → selected object/policy → post-hoc validity  
- Phase A characterization / instability results may complete without that full chain  
- Certificate types are not interchangeable without an explicit bridge object  
- Implementation and research execution blocked until respective human gates  

## Failure modes

- Scope drift via “helpful” adjacent lemmas  
- Treating B as inventor  
- Forcing MechanismInstance on Phase A packages  

## Human gates

`SCOPE_CHANGE`, `DESIGN_FINAL`, `NOVELTY_CLAIM`, `INFERENCE_THEOREM_CLAIM`, plus ART-15 registry

## Unresolved questions

None for constitution text; interpretation disputes escalate to human.
