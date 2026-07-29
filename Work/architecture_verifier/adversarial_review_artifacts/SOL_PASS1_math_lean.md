## Findings

### 1. Audit-before-promotion creates a theorem-promotion TOCTOU

- **Title:** Integration audit is not bound to the eventual promotion target or claim snapshot
- **Severity:** Critical
- **Confidence:** High
- **Affected subsystem:** Theorem workflow, promotion, integration audit
- **Failure scenario:** At S10, audit claim statement A as a CONJECTURE/non-major result, with relaxed applicability. At S12, select `PARTIAL_RESULT` or another major target, alter the claim/certificate/bridge payload to B, and reuse the earlier `audit_id`. The promotion transaction contains neither the audited claim hash nor the intended target captured at audit time.
- **Root cause:** `major_milestone` depends on `promotion_tx`, but the promotion target is chosen after S10; audit records have no target-status or immutable input digest.
- **Evidence:** `major_milestone(claim_id, promotion_tx)` depends on target status in [CHARTER.md:95](/Users/nicholasmino/Desktop/Research/Work/architecture/01-charter/CHARTER.md:95); S10 precedes S12 in [RESEARCH_CYCLE_FSM.md:63](/Users/nicholasmino/Desktop/Research/Work/architecture/08-research-cycle/RESEARCH_CYCLE_FSM.md:63); the audit schema lacks claim hash and intended target in [INTEGRATION_AUDIT.md:25](/Users/nicholasmino/Desktop/Research/Work/architecture/11-integration-audit/INTEGRATION_AUDIT.md:25); `audit_id` is optional in the promotion transaction at [STATE_MODEL.md:69](/Users/nicholasmino/Desktop/Research/Work/architecture/06-state/STATE_MODEL.md:69).
- **Suggested smallest architectural repair:** Lock an axis-specific promotion intent before S10. Bind every audit to `{claim_statement_hash, dependency snapshot, cert/utility/bridge versions, def-pin heads, intended target axes}`. Require an exact fresh PASS digest in the promotion transaction.
- **Expected impact:** Prevents unsupported promotion and reuse of an audit against a stronger or changed theorem.

### 2. `NA` and caller-supplied blocker flags bypass almost every audit question

- **Title:** ART-11 permits applicable blocking questions to be answered `NA`
- **Severity:** Critical
- **Confidence:** High
- **Affected subsystem:** Integration audit, certificate checking, scope checking
- **Failure scenario:** Mark Q11 applicable, answer `NA`, and keep `hop_chain_ok=true`. The FAIL rule catches blocking `NO` or `UNKNOWN`, not `NA`. Alternatively, submit `blocker_if_no=false` in the answer object. This can bypass bridge, data-dependence, operator, policy, and utility checks.
- **Root cause:** Applicability and blocker status are mutable fields supplied in the audit record rather than derived policy; the response-state truth table is incomplete.
- **Evidence:** `response_enum` includes `NA` and the answer carries its own `blocker_if_no` in [INTEGRATION_AUDIT.md:48](/Users/nicholasmino/Desktop/Research/Work/architecture/11-integration-audit/INTEGRATION_AUDIT.md:48); verdict FAIL names only blocker `NO/UNKNOWN` in [INTEGRATION_AUDIT.md:80](/Users/nicholasmino/Desktop/Research/Work/architecture/11-integration-audit/INTEGRATION_AUDIT.md:80); the applicability-bitmap rule only rejects N/A lacking a bitmap entry in [INTEGRATION_AUDIT.md:108](/Users/nicholasmino/Desktop/Research/Work/architecture/11-integration-audit/INTEGRATION_AUDIT.md:108).
- **Suggested smallest architectural repair:** Derive applicability and blocker status from the typed claim snapshot. Enforce: applicable ⇒ only `YES` passes; inapplicable ⇒ only `NA` with a derived reason; `NO` and `UNKNOWN` always block required paths. Remove `blocker_if_no` from instance data.
- **Expected impact:** Converts the checklist from self-attestation into a deterministic gate.

### 3. A bridge proves only an enum-to-enum slogan, not a typed implication

- **Title:** Bridge schema cannot establish certificate compatibility
- **Severity:** Critical
- **Confidence:** High
- **Affected subsystem:** Certificate typing, inference bridge, promotion
- **Failure scenario:** Register one `PROVED` bridge from `DP`/INDEX to `INFERENCE_COVERAGE`/INDEX. Reuse it for a different neighbor relation, selection operator, domain, parameter regime, failure probability, or definition pin. Q11 sees a `PROVED` kind conversion and passes.
- **Root cause:** Bridges lack source/target certificate IDs, domains, operators, assumptions, parameter transforms, failure-budget transforms, definition pins, and dependency closure.
- **Evidence:** Certificates carry these distinctions in [SCHEMAS.md:47](/Users/nicholasmino/Desktop/Research/Work/architecture/07-schemas/SCHEMAS.md:47), but bridges contain only kinds, objects, status, and optional claim ID in [SCHEMAS.md:96](/Users/nicholasmino/Desktop/Research/Work/architecture/07-schemas/SCHEMAS.md:96); Q11 checks only acceptance of `cert_kind` via a proved bridge in [INTEGRATION_AUDIT.md:71](/Users/nicholasmino/Desktop/Research/Work/architecture/11-integration-audit/INTEGRATION_AUDIT.md:71).
- **Suggested smallest architectural repair:** Make a bridge a typed theorem edge referencing exact source and target certificate schema hashes, operators, pins, assumptions, parameter transform, and a promoted proof claim. Remove certificate-local `bridge_availability`; derive it from the authoritative bridge registry.
- **Expected impact:** Prevents certificate-kind mixing and generic bridge reuse.

### 4. The canonical trace explicitly contradicts the OPEN-bridge rule

- **Title:** ART-22 blesses an audit PASS that ART-01 and ART-11 require to FAIL
- **Severity:** Critical
- **Confidence:** High
- **Affected subsystem:** Bridge handling, inference promotion, example validation
- **Failure scenario:** Follow ART-22: record `BRIDGE_OPEN`, call the claim “local stability only,” and issue S10 PASS. ART-01 says any live OPEN inference-hop bridge makes the claim inference-facing; ART-11 then mandates FAIL.
- **Root cause:** “Inference-facing” is defined registry-wide, while the trace treats an OPEN bridge as harmless when inference is narratively disclaimed.
- **Evidence:** OPEN/ASSUMED inference-hop bridges trigger `inference_facing` in [CHARTER.md:90](/Users/nicholasmino/Desktop/Research/Work/architecture/01-charter/CHARTER.md:90); ART-11 requires FAIL for such inference milestones in [INTEGRATION_AUDIT.md:80](/Users/nicholasmino/Desktop/Research/Work/architecture/11-integration-audit/INTEGRATION_AUDIT.md:80); ART-22 nevertheless records PASS with `BRIDGE_OPEN` in [E2E_TRACE.md:25](/Users/nicholasmino/Desktop/Research/Work/architecture/22-example-trace/E2E_TRACE.md:25).
- **Suggested smallest architectural repair:** Define facing from exact dependency edges, not all live registry bridges. An unused OPEN bridge must not appear in the audited dependency set; if the promoted claim consumes it, promotion fails.
- **Expected impact:** Removes a direct OPEN-to-inference laundering precedent and makes the reference trace unambiguous.

### 5. Forgotten or archived counterexamples do not block promotion

- **Title:** Promotion has no active-counterexample closure predicate
- **Severity:** Critical
- **Confidence:** High
- **Affected subsystem:** Counterexample invalidation, theorem DAG, promotion
- **Failure scenario:** A FULL_REFUTE demotes claim C. Archive that CX or introduce C′ with a new ID and substantially the same goal. Default retrieval omits archived records; the promotion transaction for C′ checks `contradiction_clear` but has no `cx_closure_ok`, fingerprint-equivalence, or refutation-watermark field.
- **Root cause:** Demotion is event-driven, while promotion does not re-prove absence of applicable historical counterexamples.
- **Evidence:** The promotion fields omit counterexample closure in [STATE_MODEL.md:69](/Users/nicholasmino/Desktop/Research/Work/architecture/06-state/STATE_MODEL.md:69); CX status includes `ARCHIVED` in [COUNTEREXAMPLE_PROTOCOL.md:58](/Users/nicholasmino/Desktop/Research/Work/architecture/12-counterexample/COUNTEREXAMPLE_PROTOCOL.md:58); default retrieval excludes archived records in [COUNTEREXAMPLE_PROTOCOL.md:99](/Users/nicholasmino/Desktop/Research/Work/architecture/12-counterexample/COUNTEREXAMPLE_PROTOCOL.md:99).
- **Suggested smallest architectural repair:** Require `cx_closure_ok` over the claim, dependency closure, equivalent fingerprints, superseded claims, and ancestor pins, including archived records. Archive may affect presentation, never blocking semantics.
- **Expected impact:** Prevents resurrection of refuted mathematics under a new claim ID or retrieval mode.

### 6. Superseded definition pins remain promotable

- **Title:** Pins are versioned but no authoritative active-head predicate exists
- **Severity:** High
- **Confidence:** High
- **Affected subsystem:** Definition pins, audit invalidation, promotion, Lean staleness
- **Failure scenario:** After `def.v2` supersedes `def.v1`, start a new cycle pinned to `def.v1`; all fields are internally frozen and consistent, so audit and promotion can succeed. Alternatively, supersede a pin after S10 but before promotion and reuse the PASS before the demotion wave finishes.
- **Root cause:** The state records supersession links but no active head/currentness rule; “frozen” is confused with “current.”
- **Evidence:** Definitions are keyed by `def_id@pin` with supersession links in [STATE_MODEL.md:31](/Users/nicholasmino/Desktop/Research/Work/architecture/06-state/STATE_MODEL.md:31); promotion carries only `def_pins[]` in [STATE_MODEL.md:69](/Users/nicholasmino/Desktop/Research/Work/architecture/06-state/STATE_MODEL.md:69); `math_stable` checks frozen pins, not active pins, in [RESEARCH_CYCLE_FSM.md:80](/Users/nicholasmino/Desktop/Research/Work/architecture/08-research-cycle/RESEARCH_CYCLE_FSM.md:80); audit invalidation is merely declared in [INTEGRATION_AUDIT.md:100](/Users/nicholasmino/Desktop/Research/Work/architecture/11-integration-audit/INTEGRATION_AUDIT.md:100).
- **Suggested smallest architectural repair:** Add an authoritative `active_definition_heads` map. Promotion must atomically verify that every pin is current and that no supersession/demotion event occurred after its audit snapshot. Historical-pin claims may remain stored but cannot advance the live chain.
- **Expected impact:** Closes pin-fork and audit-staleness attacks.

### 7. There is no canonical claim schema capable of evaluating the advertised predicates

- **Title:** Claim typing and multi-axis status are structurally absent
- **Severity:** Critical
- **Confidence:** High
- **Affected subsystem:** Theorem DAG, promotion, inference-facing classification, hop checking
- **Failure scenario:** Keep card fields tagged `stability` while the actual conclusion asserts coverage; or update a unary summary label without coherently updating `formal_status` and `paper_status`. There is no authoritative claim record containing the statement hash, chain segment, certificate, stabilized object, dependencies, pins, and axes together.
- **Root cause:** ART-07 defines mechanisms, certificates, utilities, bridges, and experiments—but not claims. ART-09 introduces multiple axes while ART-06 promotes with unary `from_status/to_status`.
- **Evidence:** The theorem registry is only described as a `claim_id` DAG in [STATE_MODEL.md:31](/Users/nicholasmino/Desktop/Research/Work/architecture/06-state/STATE_MODEL.md:31); the multi-axis record is underspecified in [THEOREM_STATUS_FSM.md:28](/Users/nicholasmino/Desktop/Research/Work/architecture/09-theorem-status/THEOREM_STATUS_FSM.md:28); promotion remains unary in [STATE_MODEL.md:69](/Users/nicholasmino/Desktop/Research/Work/architecture/06-state/STATE_MODEL.md:69); ART-07 has no Claim section between [SCHEMAS.md:24](/Users/nicholasmino/Desktop/Research/Work/architecture/07-schemas/SCHEMAS.md:24) and its experiment schema.
- **Suggested smallest architectural repair:** Add one immutable, content-addressed Claim schema and make promotion axis-specific. Derive summary labels, `inference_facing`, `policy_facing`, chain placement, and audit applicability from that record.
- **Expected impact:** Makes promotion and scope predicates evaluable instead of narrative.

### 8. Lean status is not actually a function of the manifest

- **Title:** The Lean manifest is neither content-complete nor associated with a total status function
- **Severity:** Critical
- **Confidence:** High
- **Affected subsystem:** Lean workflow, stale verification, formal-status promotion
- **Failure scenario:** Change a proof body or imported theorem without changing the statement, entry-module name, definition pins, or toolchain. Reuse the old manifest. `LEAN_STALE` does not trigger for an upstream claim refutation without a pin/toolchain change. Separately, a manifest with `build_ok=false` can satisfy the written `LEAN_CORE` row because that row does not require `build_ok`.
- **Root cause:** The manifest lacks source-tree/proof hashes, imported declaration hashes, dependency-manifest hashes, build recipe, and active claim-status snapshot. Status predicates overlap and have no precedence.
- **Evidence:** Manifest fields are listed in [LEAN_FSM.md:28](/Users/nicholasmino/Desktop/Research/Work/architecture/10-lean/LEAN_FSM.md:28); the unsupported “function” assertion is at [LEAN_FSM.md:46](/Users/nicholasmino/Desktop/Research/Work/architecture/10-lean/LEAN_FSM.md:46); status rows are incomplete at [LEAN_FSM.md:48](/Users/nicholasmino/Desktop/Research/Work/architecture/10-lean/LEAN_FSM.md:48); `LEAN_STALE` only mentions pin/toolchain changes in [LEAN_FSM.md:56](/Users/nicholasmino/Desktop/Research/Work/architecture/10-lean/LEAN_FSM.md:56); promotion’s `lean_manifest_ok` is optional in [STATE_MODEL.md:71](/Users/nicholasmino/Desktop/Research/Work/architecture/06-state/STATE_MODEL.md:71).
- **Suggested smallest architectural repair:** Content-address the complete Lean closure and bind it to exact theorem declarations, active definition heads, imported theorem versions, axiom provenance, and dependency manifests. Define one deterministic precedence table. Never store a writable Lean status.
- **Expected impact:** Prevents stale Lean and manifest theater.

### 9. `math_stable` has no valid two-pass path and simultaneously admits non-PASS audits

- **Title:** The math-stability gate is both unreachable and semantically permissive
- **Severity:** High
- **Confidence:** High
- **Affected subsystem:** Research-cycle FSM, Lean readiness
- **Failure scenario:** A cycle needs two full attack+audit passes, but after S10 the FSM has no transition back to S09/S10. Implementers must either require a human waiver for every Lean attempt or incorrectly count the pre-proof S09 as a full audit pass. In addition, `verdict ≠ FAIL` admits `IRRELEVANT` and `ESCALATE_HUMAN` into the predicate.
- **Root cause:** The predicate was specified independently of the reachable FSM and uses a negative verdict condition instead of `PASS`.
- **Evidence:** Two passes are required in [RESEARCH_CYCLE_FSM.md:84](/Users/nicholasmino/Desktop/Research/Work/architecture/08-research-cycle/RESEARCH_CYCLE_FSM.md:84); the latest verdict need only be non-FAIL at [RESEARCH_CYCLE_FSM.md:89](/Users/nicholasmino/Desktop/Research/Work/architecture/08-research-cycle/RESEARCH_CYCLE_FSM.md:89); S10 has no return edge in [RESEARCH_CYCLE_FSM.md:63](/Users/nicholasmino/Desktop/Research/Work/architecture/08-research-cycle/RESEARCH_CYCLE_FSM.md:63).
- **Suggested smallest architectural repair:** Add a versioned `S10 PASS → S09` re-attack loop, count distinct audit IDs over the identical claim snapshot, and require latest verdict exactly PASS.
- **Expected impact:** Makes the gate reachable and prevents Lean entry on irrelevant or unresolved work.

### 10. UtilityCompat is an asserted tag, and the N/A branch launders HEURISTIC utility

- **Title:** `PROVED_INEQUALITY` has no proof, while N/A is label-driven
- **Severity:** High
- **Confidence:** High
- **Affected subsystem:** Utility certificates, promotion, `math_stable`
- **Failure scenario:** Mint a UtilityCompat row with `link_kind=PROVED_INEQUALITY` but no theorem or proof reference. Alternatively, retain only HEURISTIC support for a utility-bearing stability claim and set `utility_analysis_ref=N/A` plus acknowledgment; the rules do not prove the promoted conclusion contains no utility assertion.
- **Root cause:** UtilityCompat is a relationship enum rather than a theorem edge. N/A depends on `chain_segment=stability`, not semantic absence of a utility proposition.
- **Evidence:** UtilityCompat has no `claim_id`, proof reference, assumptions, or parameter mapping in [SCHEMAS.md:82](/Users/nicholasmino/Desktop/Research/Work/architecture/07-schemas/SCHEMAS.md:82); the N/A disjunction appears in [SCHEMAS.md:93](/Users/nicholasmino/Desktop/Research/Work/architecture/07-schemas/SCHEMAS.md:93); the close card allows explicit N/A in [EXPERIMENT_PROTOCOL.md:55](/Users/nicholasmino/Desktop/Research/Work/architecture/08-research-cycle/EXPERIMENT_PROTOCOL.md:55).
- **Suggested smallest architectural repair:** Make `PROVED_INEQUALITY` reference a promoted theorem over exact cert/utility snapshots. Permit N/A only when the canonical claim has `utility_id=NONE` and no utility conclusion. Reject simultaneous HEURISTIC/N/A treatment for the same claim.
- **Expected impact:** Stops both assertion-only compatibility and HEURISTIC bypass.

### 11. Data-dependent ψ enters without the mandatory human gate

- **Title:** `explicit_submechanism` bypasses `DATA_DEP_PSI`
- **Severity:** High
- **Confidence:** High
- **Affected subsystem:** Scope lock, mechanism typing, human gates
- **Failure scenario:** Set `psi_data_dependence=explicit_submechanism`, provide any submechanism ID, answer Q4 YES, and continue. No admissibility or promotion field requires a matching `DATA_DEP_PSI` decision, and the schema does not require a certificate proving the calibration submechanism.
- **Root cause:** The gate is enumerated but not wired into a derived scope predicate.
- **Evidence:** The default and human-gated change are stated in [MATH_SCOPE.md:67](/Users/nicholasmino/Desktop/Research/Work/architecture/02-scope/MATH_SCOPE.md:67); the schema freely permits `explicit_submechanism` in [SCHEMAS.md:31](/Users/nicholasmino/Desktop/Research/Work/architecture/07-schemas/SCHEMAS.md:31); Q4 only asks whether it is certified in [INTEGRATION_AUDIT.md:64](/Users/nicholasmino/Desktop/Research/Work/architecture/11-integration-audit/INTEGRATION_AUDIT.md:64); the gate exists in [HUMAN_GATES.md:31](/Users/nicholasmino/Desktop/Research/Work/architecture/15-human-gates/HUMAN_GATES.md:31) but is absent from the promotion transaction.
- **Suggested smallest architectural repair:** Derive `requires_DATA_DEP_PSI` from the mechanism snapshot and require a matching approved decision plus a typed calibration certificate before S06 exit and promotion.
- **Expected impact:** Restores the declared data-dependence scope lock.

### 12. Finite, fixed Λ is a prose assertion rather than an enforceable type

- **Title:** Continuous or data-dependent candidate sets can be tagged `IN_CHAIN`
- **Severity:** High
- **Confidence:** High
- **Affected subsystem:** Mathematical scope, question selection, experiment readiness
- **Failure scenario:** Put \(\Lambda=[0,1]\), a data-derived shortlist, or a data-dependent feasible set in the free-text `optimization_problem`, cite `DEF.candidates@def.v1`, and have the scheduler classify the question `IN_CHAIN`. No structured field exposes cardinality or generation dependence, and ART-11 has no finite/fixed-Λ question.
- **Root cause:** Scope classification is self-reported through quarantine labels; the mathematical object is not represented in a machine-checkable candidate-set record.
- **Evidence:** Finite and data-independent Λ is pinned in [MATH_SCOPE.md:28](/Users/nicholasmino/Desktop/Research/Work/architecture/02-scope/MATH_SCOPE.md:28); admissibility requires finite Λ in [CHARTER.md:67](/Users/nicholasmino/Desktop/Research/Work/architecture/01-charter/CHARTER.md:67); ExampleCard stores an `optimization_problem` description in [EXPERIMENT_PROTOCOL.md:28](/Users/nicholasmino/Desktop/Research/Work/architecture/08-research-cycle/EXPERIMENT_PROTOCOL.md:28); OOS handling depends on scheduler classification in [QUESTION_SELECTION.md:85](/Users/nicholasmino/Desktop/Research/Work/architecture/08-research-cycle/QUESTION_SELECTION.md:85).
- **Suggested smallest architectural repair:** Add a canonical candidate-set object with `finite`, cardinality/witness, generation dependence, feasibility dependence, and definition pin. Derive required gates from it; reject disagreement with the mathematical statement.
- **Expected impact:** Blocks continuous-Λ and data-dependent-candidate drift.

### 13. The mandatory counterexample applicability function is incomplete

- **Title:** Most listed attack classes are never made applicable
- **Severity:** High
- **Confidence:** High
- **Affected subsystem:** Counterexample workflow, composition, constrained selection
- **Failure scenario:** For repeated composition, attack only a vanishing gap and omit `CX.noncompose`; for constrained selection omit `CX.active_set`; for selection-probability certificates omit `CX.zero_prob` and `CX.support_change`; for sensitivity claims omit `CX.unbounded_sens`. All can satisfy the published minimum applicability table.
- **Root cause:** The architecture lists twelve classes but defines applicability for only heterogeneity, data-dependent ψ, inference bridges, policy claims, and one baseline choice.
- **Evidence:** The full attack-class list is in [COUNTEREXAMPLE_PROTOCOL.md:25](/Users/nicholasmino/Desktop/Research/Work/architecture/12-counterexample/COUNTEREXAMPLE_PROTOCOL.md:25); the applicability mapping is only the small table at [COUNTEREXAMPLE_PROTOCOL.md:44](/Users/nicholasmino/Desktop/Research/Work/architecture/12-counterexample/COUNTEREXAMPLE_PROTOCOL.md:44); ART-20 nevertheless claims enforcement for support and composition in [INVARIANTS.md:33](/Users/nicholasmino/Desktop/Research/Work/architecture/20-invariants/INVARIANTS.md:33).
- **Suggested smallest architectural repair:** Define a total applicability function over typed features: probabilistic-support claim, adaptive repetition, constrained feasibility, sensitivity bound, policy object, bridge use, and mechanism family.
- **Expected impact:** Prevents selectively omitting the attack class most likely to refute the claim.

### 14. Proposer/certifier separation cannot be verified by promotion

- **Title:** Proof certification has no authoritative transaction binding
- **Severity:** High
- **Confidence:** High
- **Affected subsystem:** Proof review, theorem promotion, role separation
- **Failure scenario:** Put both role names in `roles_invoked[]` while the same principal performs both, or omit an ACCEPT record entirely. The promotion transaction has no proof-review ID, proposer ID, certifier ID, reviewed statement hash, or review outcome.
- **Root cause:** ART-13 describes a review record but ResearchState has no proof-review registry and promotion cannot reference it.
- **Evidence:** ART-13 requires a certifier outcome record in [PROOF_REVIEW.md:18](/Users/nicholasmino/Desktop/Research/Work/architecture/13-proof-review/PROOF_REVIEW.md:18); review packet fields are only prose in [PROOF_REVIEW.md:38](/Users/nicholasmino/Desktop/Research/Work/architecture/13-proof-review/PROOF_REVIEW.md:38); promotion contains only `roles_invoked[]` in [STATE_MODEL.md:69](/Users/nicholasmino/Desktop/Research/Work/architecture/06-state/STATE_MODEL.md:69).
- **Suggested smallest architectural repair:** Add an authoritative `proof_reviews` registry and require a review ID bound to the exact claim hash/pins, with distinct principal IDs and an ACCEPT outcome.
- **Expected impact:** Makes unsupported `PROVED_ON_PAPER` promotion rejectable.

### 15. Imported-result reframing is not detectable

- **Title:** `IMPORTED_RESULT_REGISTER` cannot enforce first-use or reframe rules
- **Severity:** High
- **Confidence:** High
- **Affected subsystem:** External theorem use, dependency DAG, promotion
- **Failure scenario:** Import a theorem once, then change its assumption map, formalization mapping, or chain role and continue using the original registration. The literature row has no versioned assumption map or chain role, so the reframe cannot be detected.
- **Root cause:** The boundary predicate is stronger than the imported-result data model.
- **Evidence:** Registration is required on every material reframe in [CHARTER.md:56](/Users/nicholasmino/Desktop/Research/Work/architecture/01-charter/CHARTER.md:56) and [THEOREM_STATUS_FSM.md:48](/Users/nicholasmino/Desktop/Research/Work/architecture/09-theorem-status/THEOREM_STATUS_FSM.md:48); the literature schema lacks assumption map, chain role, version, and registration receipt in [LITERATURE_BOUNDARY.md:38](/Users/nicholasmino/Desktop/Research/Work/architecture/14-literature/LITERATURE_BOUNDARY.md:38).
- **Suggested smallest architectural repair:** Create a versioned ImportedResult record containing exact statement/source span, assumptions, formalization mapping, chain role, pins, and gate receipt. Any field change creates a new version and registration obligation.
- **Expected impact:** Prevents imported-theorem laundering and unsupported chain advancement.

### 16. The current PASS/C12 posture is false convergence

- **Title:** ART-25 promotes a narrow patch audit as a full-system PASS
- **Severity:** High
- **Confidence:** High
- **Affected subsystem:** Design convergence, audit governance, implementation readiness
- **Failure scenario:** A human sees `AUDIT-0.3-R20`, C12=2, and no Critical/High issues, then approves DESIGN_FINAL. Yet R20’s own scope was a hard-stop patch and regression check, not an adversarial audit of theorem, Lean, certificate, CX, and scope guarantees. Acceptance tests T05/T10/T15 pass largely because corresponding text exists—even though ART-22 is contradictory.
- **Root cause:** Audit completeness and semantic test coverage are not prerequisites for assigning `audit_pass_id`; C12 counts clean rounds relative to a narrow baseline.
- **Evidence:** C11 requires an independent full-package PASS in [DESIGN_CONVERGENCE.md:25](/Users/nicholasmino/Desktop/Research/Work/architecture/20-invariants/DESIGN_CONVERGENCE.md:25); ART-25 claims PASS/C12=2 in [FINAL_AUDIT.md:5](/Users/nicholasmino/Desktop/Research/Work/architecture/25-audit-reports/FINAL_AUDIT.md:5); the R20 transcript explicitly scopes itself to the hard-stop patch at [862084d7…jsonl:1](/Users/nicholasmino/Desktop/Research/Work/architecture/adversarial_review_artifacts/862084d7-07ee-4cd1-b29d-b89a6f4955c9.jsonl:1); presence-oriented T05/T10/T15 are declared PASS in [ACCEPTANCE_TESTS.md:42](/Users/nicholasmino/Desktop/Research/Work/architecture/21-acceptance-tests/ACCEPTANCE_TESTS.md:42).
- **Suggested smallest architectural repair:** Withdraw R20 as a full-system baseline, reset C12 to zero, and require semantic adversarial traces covering the failures above before a new audit PASS.
- **Expected impact:** Prevents a governance PASS from masking unimplemented mathematical guarantees.

## Subsystems that can be removed or reduced

| Subsystem | Recommendation | Why |
|---|---|---|
| `Certificate.bridge_availability` | Remove | It duplicates authoritative bridge state and permits disagreement. Derive availability from exact bridge edges. |
| Experiment-card `lean_status` | Remove | Lean status must be derived solely from the current manifest; a copied card field is a stale-label vector. |
| Unary summary status and unary `from_status/to_status` | Remove | They conflict with the multi-axis model. Use axis-specific transitions and derive display labels. |
| ART-11 instance-level `blocker_if_no` and manual applicability bitmap | Remove | These are policy, not evidence. Deterministically derive them from the typed claim. |
| ART-08b scoring weights, anti-easy rule, and stagnation heuristics | Remove from the correctness control plane | They affect research prioritization, not theorem validity. Retain only the atomic question/scope lock. |
| OPERABLE_MINIMAL role ceiling | Remove as a correctness gate | Roster size does not establish independence or correctness. Retain exact principal-separation constraints for proposer/certifier/auditor/verifier. |
| Mechanism-family literature checklist inside `math_stable` | Remove from mathematical stability | Prior art is necessary for novelty/import provenance, not for whether a theorem statement is stable. Keep it as a separate publication/novelty gate. |
| Current rigid S00–S16 FSM | Replace with a smaller transactional lifecycle | The ordering creates TOCTOU and an unreachable two-pass condition. The necessary core is lock → evidence snapshot → audit → atomic promotion. |
| Current `math_stable` predicate | Demote to workflow policy or replace | It is not needed for formal soundness if manifests bind exact claim hashes. A snapshot-based “ready to formalize” receipt is sufficient. |
| ART-22 | Keep only as a test fixture, never authority | It currently contradicts binding bridge rules. |
| ART-20b/ART-25 | Keep only as design-governance artifacts | They must not participate in theorem, certificate, Lean, or promotion truth. |
| Derived `frontier` registry | Remove as stored subsystem | ART-06 already says it is a view. Compute it from `open_questions`. |

## Subsystems whose necessity is established

- A canonical, immutable Claim record and dependency DAG are necessary because every promotion, bridge, counterexample, and Lean result must bind to the same proposition.
- An atomic promotion transaction is necessary, but only if it re-evaluates current pins, CX closure, proof review, audit snapshot, gates, and Lean manifest.
- The counterexample registry is necessary because invalidation must survive new cycles, new claim IDs, archival, and pin revisions.
- Typed bridge objects are necessary only when crossing certificate kinds; without them, no inference-facing claim may promote.
- Independent proof certification and Lean verification are necessary, with principal identity and immutable artifact binding.
- A scope-lock object is necessary, but quarantine labels alone are insufficient; it must derive finite/fixed Λ and ψ dependence from typed mathematical objects.
- UtilityCompat is necessary only for claims that actually assert utility; it must be a theorem edge, not an enum or waiver-shaped substitute.

## Blockers for an implementation blueprint

1. Define the canonical Claim schema and axis-specific status product.
2. Replace audit/promotion TOCTOU with immutable promotion intent and snapshot hashes.
3. Make audit applicability total and eliminate `NA`/blocker self-selection.
4. Redesign bridge and UtilityCompat objects as typed theorem edges.
5. Add current-pin and all-history counterexample-closure predicates.
6. Make Lean manifests content-address the full dependency and axiom closure.
7. Wire `DATA_DEP_PSI`, `CONTINUOUS_LAMBDA`, and feasible-set gates into derived scope predicates.
8. Add an authoritative proof-review registry with principal separation.
9. Repair or replace the two-pass `math_stable` workflow.
10. Reset the claimed full-system audit PASS and C12 ledger.

**Maturity for this slice:** 3/10. The package has a useful vocabulary and identifies many correct hazards, but its decisive guarantees are presently non-total, self-attested, contradictory, or unbound to authoritative snapshots.

**Implementation-blueprint readiness:** **No.**

**Research-execution readiness:** **No.**
