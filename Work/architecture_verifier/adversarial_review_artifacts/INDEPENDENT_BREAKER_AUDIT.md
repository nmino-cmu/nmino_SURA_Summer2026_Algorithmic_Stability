## 1. Executive summary

**NOT READY. This package does not deserve to become an implementation blueprint.**

It contains a thoughtful epistemic-control concept, but its decisive controls remain prose assertions rather than implementable, testable semantics. The architecture has no authoritative commit protocol, no canonical Claim schema, no trustworthy audit-to-promotion binding, no safe restore trust anchor, no enforceable role identity, and no reproducible release/audit identity.

`AUDIT-0.3-R20 PASS` and `C12 = 2` are false-convergence claims. R20 was prompted as a regression review of a hard-stop patch, not a credible full-system examination; it was not bound to the live package bytes; the archived transcripts contain 57 redactions, 175 tool calls, and zero tool results; and the first claimed post-PASS round has the same minute timestamp as R20 while R20 describes it as “in flight.” The package cannot prove audit completeness, ordering, independence, or reproducibility.

The active implementation block is correct and must remain in force.

## 2. Architecture strengths

The package has real conceptual strengths:

- The charter establishes a narrow mathematical scope and explicitly rejects certificate-type laundering.
- Stability, utility, inference, theorem, and Lean status are treated as distinct concerns.
- Counterexamples and failed proofs are intended to be durable research outputs.
- Human gates default toward hold or denial rather than silent approval.
- The system recognizes definition pins, dependency closure, demotion, quarantine, integration review, and independent proof certification as necessary controls.
- Design-time simulation is separated from ResearchState authority.
- The package openly acknowledges correlated-model failure, citation uncertainty, and deferred Lean coverage.

These strengths make the package a useful requirements and threat-model source. They do not make it an implementation blueprint.

## 3. Top ten architectural risks

**R1 — Authoritative state mutation is undefined**

- **Title:** No authoritative committer or atomic event reducer
- **Severity:** Critical
- **Confidence:** 0.99
- **Affected subsystem:** Entire state plane, promotion, demotion, gates, frontier, recovery
- **Failure scenario:** A caller submits a promotion with `dep_closure_ok=true`, `eio_pass=true`, and `contradiction_clear=true`. Nothing identifies the component that must authenticate the caller, recompute those predicates, compare the expected state head, serialize the write, or update projections atomically. A permissive implementation accepts fabricated predicates; a literal implementation deadlocks because no principal has commit authority.
- **Root cause:** The design says committed events are authoritative while separately calling registries authoritative. `I.ProposeWrite` ends at a pending transaction, but there is no `I.Commit`, event envelope, compare-and-swap rule, or authorized reducer.
- **Evidence:** [ART-06 declares event authority and caller-supplied promotion booleans](/Users/nicholasmino/Desktop/Research/Work/architecture/06-state/STATE_MODEL.md:12), [ART-05 grants proposal and veto rights but no commit right](/Users/nicholasmino/Desktop/Research/Work/architecture/05-authority/AUTHORITY_MATRIX.md:38), and [ART-24 provides no commit interface](/Users/nicholasmino/Desktop/Research/Work/architecture/24-interfaces/INTERFACE_CONTRACTS.md:24).
- **Suggested architectural repair:** Define one logical `I.Commit` boundary with an authenticated principal, typed command/event schema, expected log head, stop epoch, idempotency key, deterministic reducer, operation-specific authorization, and atomic projection updates. Ban direct registry mutation and remove authoritative caller-supplied booleans.
- **Expected impact:** Establishes a single enforceable source of authority and prevents fabricated promotions, split-brain writes, and implementation-specific semantics.

**R2 — Integration audits are replayable and self-attested**

- **Title:** Audit-to-promotion TOCTOU and answer-policy bypass
- **Severity:** Critical
- **Confidence:** 0.99
- **Affected subsystem:** Integration audit, theorem promotion, applicability policy
- **Failure scenario:** Audit claim snapshot A before the promotion target is selected, then alter the statement, dependencies, certificate, or target axes and reuse the `audit_id`. Applicable questions can also be answered `NA`, or their record-local `blocker_if_no` can be set false.
- **Root cause:** Audits lack immutable statement and dependency hashes, intended promotion axes, evidence closure, and policy version. Applicability and blocker status are instance data rather than derived rules.
- **Evidence:** S10 precedes target classification at S12 in [ART-08](/Users/nicholasmino/Desktop/Research/Work/architecture/08-research-cycle/RESEARCH_CYCLE_FSM.md:62). The audit schema lacks an audited claim digest and intended target, permits record-local `blocker_if_no`, and declares 16 answers despite defining 18 question rows in [ART-11](/Users/nicholasmino/Desktop/Research/Work/architecture/11-integration-audit/INTEGRATION_AUDIT.md:25). `audit_id` remains optional in [the promotion transaction](/Users/nicholasmino/Desktop/Research/Work/architecture/06-state/STATE_MODEL.md:69).
- **Suggested architectural repair:** Lock promotion intent before audit. Bind the audit to exact Claim, dependency, certificate, utility, bridge, pin, quarantine, policy, and intended-axis hashes. Derive applicability and blocker semantics from a versioned question registry: applicable requires `YES`; inapplicable requires policy-derived `NA`; `NO` or `UNKNOWN` blocks.
- **Expected impact:** Makes PASS a deterministic, non-replayable authorization over one exact promotion.

**R3 — Claims and bridges are not formally typed enough to support promotion**

- **Title:** Canonical Claim schema and typed bridge theorem are absent
- **Severity:** Critical
- **Confidence:** 0.99
- **Affected subsystem:** Theorem DAG, certificate compatibility, inference, status axes
- **Failure scenario:** A generic `PROVED` bridge from `DP/INDEX` to `INFERENCE_COVERAGE/INDEX` is reused across different neighbor relations, selection operators, parameter regimes, assumptions, failure budgets, and definition pins. Alternatively, card metadata says “stability” while the actual conclusion asserts coverage or policy validity.
- **Root cause:** ART-07 defines mechanisms, certificates, utilities, bridges, and experiments, but not Claims. Bridges contain enum names and objects rather than exact theorem endpoints and transforms. ART-09 is multi-axis while ART-06 promotes a unary status.
- **Evidence:** [ART-07 has no Claim schema and its Bridge schema is enum-to-enum](/Users/nicholasmino/Desktop/Research/Work/architecture/07-schemas/SCHEMAS.md:96); [ART-09 introduces multiple axes](/Users/nicholasmino/Desktop/Research/Work/architecture/09-theorem-status/THEOREM_STATUS_FSM.md:28); [ART-06 still uses `from_status`/`to_status`](/Users/nicholasmino/Desktop/Research/Work/architecture/06-state/STATE_MODEL.md:69).
- **Suggested architectural repair:** Introduce an immutable, content-addressed Claim record containing exact statement AST/hash, dependency edges, assumptions, chain segment, object, certificate, operator, parameter domain, pins, and independent status axes. Make each bridge a promoted theorem edge between exact source and target schema hashes with explicit assumption and parameter/failure-budget transforms.
- **Expected impact:** Prevents certificate mixing, summary-label laundering, and generic bridge reuse.

**R4 — Refuted or stale mathematics can be resurrected**

- **Title:** No counterexample closure, active-definition-head, or durable demotion-wave predicate
- **Severity:** Critical
- **Confidence:** 0.99
- **Affected subsystem:** Counterexamples, definitions, theorem DAG, promotion, demotion
- **Failure scenario:** Archive a FULL_REFUTE record, clone the theorem under a new `claim_id`, or promote against a superseded definition pin. A crash during a demotion wave leaves some dependents PROVED, yet no durable open-wave state blocks future promotion.
- **Root cause:** Promotion does not re-establish counterexample closure; archived counterexamples disappear from default retrieval; definitions have supersession links but no authoritative live heads; demotion waves lack state, target closure, cursor, and completion proof.
- **Evidence:** Promotion lacks counterexample and wave-closure fields in [ART-06](/Users/nicholasmino/Desktop/Research/Work/architecture/06-state/STATE_MODEL.md:69). Archived counterexamples are excluded by default in [ART-12](/Users/nicholasmino/Desktop/Research/Work/architecture/12-counterexample/COUNTEREXAMPLE_PROTOCOL.md:99). The demotion-wave “schema” is only an ID, trigger, order, and assertion in [ART-16](/Users/nicholasmino/Desktop/Research/Work/architecture/16-failure-recovery/FAILURE_RECOVERY.md:59).
- **Suggested architectural repair:** Add authoritative active definition heads; a `cx_closure_ok` calculation covering archived records, equivalent fingerprints, superseded claims, ancestors, and dependencies; and a crash-resumable demotion-wave registry with closure hash, targets, cursor, effects, status, and completion event.
- **Expected impact:** Prevents resurrection of refuted theorems and promotion while invalidation is incomplete.

**R5 — Recovery can silently roll the system backward**

- **Title:** Checkpoint validation cannot detect prefix rollback or semantic-version drift
- **Severity:** Critical
- **Confidence:** 0.99
- **Affected subsystem:** Checkpointing, restore, gates, demotion, long-term operation
- **Failure scenario:** Restore a valid prefix immediately before a refutation, denial, hard stop, or demotion, and present only that prefix to validation. Its Merkle root and locally computed refutation watermark both pass. New software may then replay the same old events under changed semantics.
- **Root cause:** The candidate checkpoint and available log are their own trust anchor. The complete checkpoint envelope is not authenticated, irreversible events are not externally anchored, and event/checkpoint/migration versions are absent.
- **Evidence:** ART-17 recomputes the root from the presented prefix and compares its sequence only with FULL_REFUTEs visible in that same log in [the checkpoint algorithm](/Users/nicholasmino/Desktop/Research/Work/architecture/17-indefinite-ops/INDEFINITE_OPS.md:38). The checkpoint schema contains no architecture, event-schema, reducer, canonicalization, or migration version in [ART-17](/Users/nicholasmino/Desktop/Research/Work/architecture/17-indefinite-ops/INDEFINITE_OPS.md:22).
- **Suggested architectural repair:** Authenticate the entire checkpoint envelope; externally anchor signed monotonic log-head receipts; cover every irreversible safety event; version events, reducers, canonicalization, checkpoints, and migrations; and require replay-equivalence fixtures.
- **Expected impact:** Makes rollback and multi-version restart detectable rather than self-validating.

**R6 — Human control and hard stop are not linearizable**

- **Title:** Gate bootstrap is circular and `hard_stop` lacks fencing semantics
- **Severity:** Critical
- **Confidence:** 0.99
- **Affected subsystem:** Human gates, startup, interruptibility, commit concurrency
- **Failure scenario:** A promotion validates before a hard stop, the stop commits, and the promotion commits afterward. During release, the system must append a `human_decisions` row even though active hard stop nominally forbids ResearchState mutation. At bootstrap, `DESIGN_FINAL` cannot be durably recorded without using ResearchState before research authority exists.
- **Root cause:** Gates, phase, and stop state have no independent control plane. There is no stop epoch or serialization point shared by every mutation.
- **Evidence:** `human_decisions` and `hard_stop` live in ResearchState in [ART-06](/Users/nicholasmino/Desktop/Research/Work/architecture/06-state/STATE_MODEL.md:51), while ResearchState writes are forbidden before execution approval in [ART-03](/Users/nicholasmino/Desktop/Research/Work/architecture/03-context/SYSTEM_CONTEXT.md:95). Release requires a decision append in [ART-15](/Users/nicholasmino/Desktop/Research/Work/architecture/15-human-gates/HUMAN_GATES.md:72), but `I.HardStop` defines “immediate” without a fence in [ART-24](/Users/nicholasmino/Desktop/Research/Work/architecture/24-interfaces/INTERFACE_CONTRACTS.md:36).
- **Suggested architectural repair:** Create an append-only ControlState active from bootstrap for phase, gate, role-binding, and stop events. Every state commit must compare a monotonic `stop_epoch`; stop increments and fences the epoch; release is one narrow atomic signed control event.
- **Expected impact:** Eliminates bootstrap deadlock and prevents post-freeze commits.

**R7 — Lean status is not actually a function of the proof closure**

- **Title:** Lean manifests are content-incomplete and status predicates overlap
- **Severity:** Critical
- **Confidence:** 0.99
- **Affected subsystem:** Lean verification, formal status, stale detection
- **Failure scenario:** Change a proof body or imported theorem without changing the statement, entry-module name, pins, or toolchain and reuse the previous manifest. A `LEAN_CORE` record may also satisfy the written row despite `build_ok=false`.
- **Root cause:** The manifest lacks source-tree hashes, proof/declaration hashes, imported-declaration hashes, dependency manifests, build recipe, and active theorem-status snapshot. Status precedence is not total.
- **Evidence:** The manifest fields and incomplete predicates are in [ART-10](/Users/nicholasmino/Desktop/Research/Work/architecture/10-lean/LEAN_FSM.md:28). `LEAN_STALE` only mentions pin and toolchain changes, while `LEAN_CORE` does not explicitly require `build_ok` in [the status table](/Users/nicholasmino/Desktop/Research/Work/architecture/10-lean/LEAN_FSM.md:48).
- **Suggested architectural repair:** Content-address the full Lean build closure, including source, elaborated declarations, imports, axioms, dependency manifests, build recipe, environment, and active claim/pin heads. Define a total status precedence and require reproducible independent rebuilds.
- **Expected impact:** Prevents stale or failed builds from retaining machine-verified status.

**R8 — The normative workflow contradicts itself**

- **Title:** Required review path is unreachable and the sole exemplar demonstrates a forbidden PASS
- **Severity:** Critical
- **Confidence:** 0.99
- **Affected subsystem:** Research-cycle FSM, integration audit, example trace
- **Failure scenario:** A cycle completes its first attack/audit pass. `math_stable` requires two passes, but S10 has no route back through the complete attack/audit sequence. Implementers then follow ART-22, which records `BRIDGE_OPEN` and PASS even though the charter classifies any live open inference-hop bridge as inference-facing and ART-11 requires FAIL.
- **Root cause:** Prose predicates were patched independently without checking reachability or executing the trace.
- **Evidence:** The two-pass requirement and missing loop are visible in [ART-08](/Users/nicholasmino/Desktop/Research/Work/architecture/08-research-cycle/RESEARCH_CYCLE_FSM.md:47). The charter’s facing predicate is in [ART-01](/Users/nicholasmino/Desktop/Research/Work/architecture/01-charter/CHARTER.md:90), the mandatory FAIL rule is in [ART-11](/Users/nicholasmino/Desktop/Research/Work/architecture/11-integration-audit/INTEGRATION_AUDIT.md:80), and the contradictory PASS is in [ART-22](/Users/nicholasmino/Desktop/Research/Work/architecture/22-example-trace/E2E_TRACE.md:25).
- **Suggested architectural repair:** Replace the prose FSM with a machine-readable transition relation, explicit review-loop counters, and executable positive and negative fixtures. Fix the trace before treating it as conformance evidence.
- **Expected impact:** Restores reachability and prevents implementations from copying an invalid canonical path.

**R9 — R20/C12 are false convergence**

- **Title:** The audit and convergence ledger are not bound to a reproducible package
- **Severity:** Critical
- **Confidence:** 0.99
- **Affected subsystem:** Release governance, independent audit, acceptance, package integrity
- **Failure scenario:** A team accepts ART-25 and the T-suite as proof that all Critical/High defects are closed, then implements a package the auditor never examined as a frozen whole.
- **Root cause:** No immutable release manifest or digest exists; the evidence archive omits tool results; R20’s prompt was scoped to one patch regression; audit and first post-audit review ordering is ambiguous; agent UUIDs are treated as proof of independence.
- **Evidence:** The banner claims `ARCH-0.3-ITER5` while ART-25 records only `ARCH-0.3` in [README](/Users/nicholasmino/Desktop/Research/Work/architecture/00-README.md:3) and [ART-25](/Users/nicholasmino/Desktop/Research/Work/architecture/25-audit-reports/FINAL_AUDIT.md:32). The R20 transcript is explicitly a hard-stop regression request and says ADV-ITER9-3 was “in flight” in [the archived audit](/Users/nicholasmino/Desktop/Research/Work/architecture/adversarial_review_artifacts/862084d7-07ee-4cd1-b29d-b89a6f4955c9.jsonl:1); ADV-ITER9-3 itself is timestamped in the same minute in [its transcript](/Users/nicholasmino/Desktop/Research/Work/architecture/adversarial_review_artifacts/a11ce32d-1b69-4601-9752-cc69d9beb601.jsonl:1). The acceptance table still says it is “under R17” while declaring R20 PASS in [ART-21](/Users/nicholasmino/Desktop/Research/Work/architecture/21-acceptance-tests/ACCEPTANCE_TESTS.md:35).
- **Suggested architectural repair:** Revoke current readiness credit. Freeze a release with file hashes and provenance, execute a genuinely complete audit against that digest, archive sufficient evidence, and then run two strictly subsequent independent adversarial rounds against the same digest.
- **Expected impact:** Converts convergence from agent testimony into reproducible release evidence.

**R10 — Role separation and model independence are fictitious**

- **Title:** Role labels, human decisions, and model instances lack authenticated identity
- **Severity:** Critical
- **Confidence:** 0.98
- **Affected subsystem:** EIO, auditing, certification, gates, model replacement
- **Failure scenario:** One orchestrator runs the same underlying model with different arbitrary IDs as proposer, certifier, auditor, scheduler, and EIO. A forged `human_decisions` row or unreviewed model upgrade then satisfies all string-based separation tests.
- **Root cause:** There is no principal registry, credential model, signed decision format, appointment authority, independence domain, model/prompt/tool-policy provenance, or replacement protocol.
- **Evidence:** ART-04 relies on model-family labels and the rule that one agent ID cannot be the sole proposer, prover, and auditor in [its role and anti-collusion rules](/Users/nicholasmino/Desktop/Research/Work/architecture/04-agents/AGENT_ROLES.md:24). Human decisions contain no actor authentication, issuance, expiry, or revocation fields in [ART-15](/Users/nicholasmino/Desktop/Research/Work/architecture/15-human-gates/HUMAN_GATES.md:9).
- **Suggested architectural repair:** Define signed principal and role bindings with issuer, credential, model/provider/version, prompt and tool-policy hashes, validity interval, independence domain, appointment constraints, and revocation. Add model admission, shadow, canary, rollback, and revalidation protocols.
- **Expected impact:** Makes independent review, human authority, and model replacement enforceable rather than nominal.

## 4. Critical blockers

These are the minimum stop-work blockers, consolidated from the ten risks.

**B1 — No executable state-authority kernel**

- **Title:** Commit, authorization, and transaction semantics must exist before domain workflow
- **Severity:** Critical
- **Confidence:** 0.99
- **Affected subsystem:** All mutable state and interfaces
- **Failure scenario:** Incompatible teams implement different writers, predicate evaluation orders, retry behavior, and rollback semantics while each claims conformance.
- **Root cause:** No canonical event envelope, reducer, authorization model, CAS boundary, idempotency rule, or failure taxonomy.
- **Evidence:** [ART-06 promotion fields](/Users/nicholasmino/Desktop/Research/Work/architecture/06-state/STATE_MODEL.md:69) and [ART-24 interfaces](/Users/nicholasmino/Desktop/Research/Work/architecture/24-interfaces/INTERFACE_CONTRACTS.md:24) leave these decisions open.
- **Suggested architectural repair:** Produce a machine-readable state model and reference reducer with formal preconditions, postconditions, errors, and concurrency semantics.
- **Expected impact:** Creates an interoperable substrate on which other safeguards can actually bind.

**B2 — Theorem promotion is not proof-carrying**

- **Title:** Claim, bridge, audit, promotion, and counterexample closure must be redesigned together
- **Severity:** Critical
- **Confidence:** 0.99
- **Affected subsystem:** Theorem DAG, integration, promotion, inference
- **Failure scenario:** A stale audit, generic bridge, caller-supplied boolean, or forgotten counterexample authorizes an unsupported theorem.
- **Root cause:** Evidence objects are not content-addressed or transitively bound to one exact promotion.
- **Evidence:** [Claim schema is absent and Bridge is underspecified](/Users/nicholasmino/Desktop/Research/Work/architecture/07-schemas/SCHEMAS.md:96); [audits lack a target digest](/Users/nicholasmino/Desktop/Research/Work/architecture/11-integration-audit/INTEGRATION_AUDIT.md:25); [promotion is an assertion bag](/Users/nicholasmino/Desktop/Research/Work/architecture/06-state/STATE_MODEL.md:69).
- **Suggested architectural repair:** Introduce a canonical Claim/evidence graph and an axis-specific proof-carrying promotion transaction whose predicates are recomputed from authoritative pre-state.
- **Expected impact:** Eliminates the primary unsupported-promotion paths.

**B3 — Safety invalidation and recovery are non-durable**

- **Title:** Refutations, pin supersession, demotion, stop, restore, and migration lack monotonic closure
- **Severity:** Critical
- **Confidence:** 0.99
- **Affected subsystem:** Definitions, counterexamples, demotion, checkpoints, restart
- **Failure scenario:** A crash or rollback resurrects an invalid claim or loses a human denial or stop.
- **Root cause:** No active-head map, open-wave workflow, external log anchor, or schema migration contract.
- **Evidence:** [Demotion waves are not stateful](/Users/nicholasmino/Desktop/Research/Work/architecture/16-failure-recovery/FAILURE_RECOVERY.md:59) and [checkpoint freshness is established only from the candidate log](/Users/nicholasmino/Desktop/Research/Work/architecture/17-indefinite-ops/INDEFINITE_OPS.md:38).
- **Suggested architectural repair:** Add monotonic control and log heads, crash-resumable invalidation workflows, authenticated checkpoints, and versioned migrations.
- **Expected impact:** Prevents unsafe recovery and multi-year semantic corruption.

**B4 — The control plane is unauthenticated and unfenced**

- **Title:** Human gates, role bindings, and hard stop require an independent ControlState
- **Severity:** Critical
- **Confidence:** 0.99
- **Affected subsystem:** Governance, identity, bootstrap, interruptibility
- **Failure scenario:** A forged or stale gate authorizes a transition, or a promotion commits after a human stop.
- **Root cause:** Control facts share ResearchState lifecycle and lack signatures, expiry, revocation, and stop-epoch fencing.
- **Evidence:** [ResearchState owns human decisions and hard stop](/Users/nicholasmino/Desktop/Research/Work/architecture/06-state/STATE_MODEL.md:51), while [research writes are gated from startup](/Users/nicholasmino/Desktop/Research/Work/architecture/03-context/SYSTEM_CONTEXT.md:95).
- **Suggested architectural repair:** Establish signed, append-only ControlState plus principal registry and epoch-fenced commits.
- **Expected impact:** Makes human authority and emergency control durable and race-safe.

**B5 — The specification has no executable conformance source**

- **Title:** Contradictory prose cannot serve as a normative blueprint
- **Severity:** Critical
- **Confidence:** 0.99
- **Affected subsystem:** FSM, integration questions, trace, acceptance
- **Failure scenario:** Implementers select whichever interpretation permits progress: 16 versus 18 audit questions, one versus two review passes, or PASS versus FAIL for an open inference bridge.
- **Root cause:** There is no schema compiler, transition interpreter, policy engine, or executable fixture set.
- **Evidence:** [ART-11’s impossible audit cardinality](/Users/nicholasmino/Desktop/Research/Work/architecture/11-integration-audit/INTEGRATION_AUDIT.md:41), [ART-08’s unreachable two-pass condition](/Users/nicholasmino/Desktop/Research/Work/architecture/08-research-cycle/RESEARCH_CYCLE_FSM.md:80), and [ART-22’s invalid PASS](/Users/nicholasmino/Desktop/Research/Work/architecture/22-example-trace/E2E_TRACE.md:25).
- **Suggested architectural repair:** Create a non-autonomous reference interpreter and conformance harness before `DESIGN_FINAL`.
- **Expected impact:** Converts normative ambiguity into testable behavior.

**B6 — Current readiness evidence is invalid**

- **Title:** The package must be re-released and independently re-audited
- **Severity:** Critical
- **Confidence:** 0.99
- **Affected subsystem:** Release, acceptance, C11/C12, audit governance
- **Failure scenario:** The implementation plan is authorized from a PASS that cannot be tied to the live package or independently reproduced.
- **Root cause:** No release digest, incomplete evidence archive, ambiguous ordering, and presence-based acceptance tests.
- **Evidence:** [ART-25’s unbound ledger](/Users/nicholasmino/Desktop/Research/Work/architecture/25-audit-reports/FINAL_AUDIT.md:9), [R20’s narrow scope](/Users/nicholasmino/Desktop/Research/Work/architecture/adversarial_review_artifacts/862084d7-07ee-4cd1-b29d-b89a6f4955c9.jsonl:1), and [ART-21’s documentary PASS table](/Users/nicholasmino/Desktop/Research/Work/architecture/21-acceptance-tests/ACCEPTANCE_TESTS.md:35).
- **Suggested architectural repair:** Mark R20/C12 superseded, publish a hash manifest, run executable acceptance, then perform a fresh full audit and two subsequent adversarial rounds.
- **Expected impact:** Provides defensible evidence that the corrected package—not an earlier or partial view—was reviewed.

## 5. High-priority improvements

**H1 — Assign enforceable ownership and complete interface contracts**

- **Title:** Normative components lack accountable owners and operational contracts
- **Severity:** High
- **Confidence:** 0.98
- **Affected subsystem:** State, schemas, audit, release, operations
- **Failure scenario:** A defect spans audit policy, state reducer, and release metadata, but every team treats another team as responsible.
- **Root cause:** Many normative artifacts omit an Owner; ART-24 omits owning component, authentication, atomicity, retry, timeout, and error behavior.
- **Evidence:** [ART-24’s interface table](/Users/nicholasmino/Desktop/Research/Work/architecture/24-interfaces/INTERFACE_CONTRACTS.md:24) contains only abbreviated input/output/invariant columns.
- **Suggested architectural repair:** Add a RACI matrix and complete interface contracts with owner, principal, preconditions, postconditions, atomicity, errors, retries, timeouts, idempotency, observability, and versioning.
- **Expected impact:** Prevents incompatible implementations and unowned integrity failures.

**H2 — Enforce data independence through provenance rather than declarations**

- **Title:** `psi_data_dependence=independent` is self-attested
- **Severity:** High
- **Confidence:** 0.97
- **Affected subsystem:** Mechanisms, experiments, integration audit
- **Failure scenario:** Calibration code reads dataset-derived state transitively while the mechanism record says `independent`; Q4 is answered YES and the theorem promotes.
- **Root cause:** No typed derivation graph, dataset taint, execution boundary, or negative dependency test exists.
- **Evidence:** ART-07 records only a declaration and optional submechanism IDs in [the mechanism schema](/Users/nicholasmino/Desktop/Research/Work/architecture/07-schemas/SCHEMAS.md:24); ART-11 reduces enforcement to a checklist response in [Q4](/Users/nicholasmino/Desktop/Research/Work/architecture/11-integration-audit/INTEGRATION_AUDIT.md:64).
- **Suggested architectural repair:** Add data-provenance and taint graphs, hermetic parameter derivation, signed execution manifests, and tests for hidden direct and transitive dependencies.
- **Expected impact:** Prevents mathematically invalid independence claims from passing on metadata alone.

**H3 — Define bounded long-term operation**

- **Title:** Append-only memory has no capacity, retention, or restart envelope
- **Severity:** High
- **Confidence:** 0.97
- **Affected subsystem:** Storage, retrieval, checkpoints, operations
- **Failure scenario:** Years of events, counterexamples, manifests, and checkpoints exhaust storage or make replay and index rebuilding operationally impossible.
- **Root cause:** “Never delete” is specified without capacity models, tiers, compaction proofs, retention schedules, backpressure, or restart-time objectives.
- **Evidence:** [ART-17 requires append-only/archive-only history and budgets only cycles](/Users/nicholasmino/Desktop/Research/Work/architecture/17-indefinite-ops/INDEFINITE_OPS.md:55); legal retention conflict is merely acknowledged in [ART-23](/Users/nicholasmino/Desktop/Research/Work/architecture/23-limitations/LIMITATIONS.md:11).
- **Suggested architectural repair:** Specify volume assumptions, hot/warm/cold tiers, bounded queries, index lifecycle, safe compaction, checkpoint retention, legal holds, deletion governance, RPO/RTO, and backpressure.
- **Expected impact:** Makes “indefinite operation” measurable instead of aspirational.

**H4 — Make policy engines deterministic**

- **Title:** Linter, scheduler, and applicability rules are gameable
- **Severity:** High
- **Confidence:** 0.96
- **Affected subsystem:** Synthesis, question selection, audit policy
- **Failure scenario:** Prose is padded with irrelevant IDs to defeat B4; two schedulers choose different equal-scoring questions; auditors disagree on applicable counterexample or audit classes.
- **Root cause:** Predicate-to-action mappings, tie-breaks, relevance validation, and policy versions are unspecified.
- **Evidence:** ART-18b says any predicate triggers “action” without mapping predicates to outputs and uses `cx_ids` in B4 despite omitting them from inputs in [the linter contract](/Users/nicholasmino/Desktop/Research/Work/architecture/18-model-protocols/BULLSHIT_LINTER.md:11). ART-08b defines `argmax` without a tie-break in [the scheduler](/Users/nicholasmino/Desktop/Research/Work/architecture/08-research-cycle/QUESTION_SELECTION.md:47).
- **Suggested architectural repair:** Version deterministic decision tables, validate evidence relevance and currentness, define stable tie-breaks, and publish adversarial fixtures.
- **Expected impact:** Eliminates policy divergence and denominator-padding attacks.

**H5 — Replace the “minimal profile” overlay with one runtime contract**

- **Title:** OPERABLE_MINIMAL does not actually reduce the runtime architecture
- **Severity:** High
- **Confidence:** 0.95
- **Affected subsystem:** Roles, registries, operational complexity
- **Failure scenario:** Day-one operation immediately requires Literature Analyst, Mechanism Designer, Utility Analyst, and Lean Verifier even though the advertised roster omits some of them; registry mappings differ between ART-04b and ART-06.
- **Root cause:** The profile is an overlay on a mandatory 25-artifact structure and forbids deletion rather than selecting one authoritative runtime model.
- **Evidence:** [ART-04b’s roster and conditional roles](/Users/nicholasmino/Desktop/Research/Work/architecture/04-agents/OPERABLE_MINIMAL_PROFILE.md:29) omit roles assigned mandatory S06/S08 duties in [ART-04](/Users/nicholasmino/Desktop/Research/Work/architecture/04-agents/AGENT_ROLES.md:42). Its registry list also conflicts with [ART-06’s authoritative registries](/Users/nicholasmino/Desktop/Research/Work/architecture/06-state/STATE_MODEL.md:31).
- **Suggested architectural repair:** Make one reduced runtime contract authoritative; move critic catalogs and historical governance into non-normative appendices.
- **Expected impact:** Reduces implementation surface and removes profile-versus-core ambiguity.

## 6. Potential overengineering

- Seventeen research-cycle states coexist with separate theorem and Lean state machines, yet basic transitions remain unreachable.
- Twenty-one pseudo-registries are declared before one event/transaction protocol is defined.
- The architecture maintains an extensive role catalog while lacking principal identity.
- Fixed question-scoring weights and a speculative-prose linter are premature relative to missing commit, recovery, and security fundamentals.
- The 25-artifact package requirement turns document presence into a design goal.
- C11/C12 make audit reports part of the architecture’s own acceptance evidence, creating a self-referential governance loop.
- OPERABLE_MINIMAL adds another normative layer instead of materially deleting runtime surface.

## 7. Potential underengineering

The package is simultaneously over-documented and under-specified. Major omissions include:

- Canonical machine-readable schemas and reducer
- Event ordering, concurrency, idempotency, and commit atomicity
- Principal authentication and capability authorization
- Claim and exact dependency typing
- Migration and mixed-version behavior
- Durable recovery and external rollback anchors
- Executable conformance and negative testing
- Model replacement and admission controls
- Data-provenance enforcement
- Capacity, reliability, security, and incident-response requirements

## 8. Missing architectural components

- Independent bootstrap `ControlState`
- Authenticated principal and role-binding registry
- Canonical command/event envelope
- Deterministic state reducer and projection builder
- Immutable Claim repository
- Typed bridge-theorem registry
- Active-definition-head registry
- Audit-policy/question registry
- Promotion-intent registry
- Counterexample-closure engine
- Durable demotion-wave workflow
- Lean build-closure and attestation service
- External transparency/log-head witness
- Checkpoint migration framework
- Release manifest and package verifier
- Data-provenance/taint subsystem
- Model admission and replacement controller
- Operational observability, capacity, and incident-management plane

## 9. Missing invariants

At minimum, the design lacks enforceable invariants that:

- Every mutation is authorized by exactly one committer and deterministic reducer.
- Every mutation compares both expected log head and expected stop epoch.
- Committed state equals deterministic replay of the authenticated event log.
- Audit PASS authorizes exactly one immutable claim snapshot and target-axis transition.
- Applicable audit questions pass only on `YES`; `NA` is permitted only when policy derives inapplicability.
- Promotion uses active definition heads.
- Promotion is blocked by every applicable historical counterexample, including archived and equivalent fingerprints.
- Promotion is blocked while any relevant demotion wave is non-complete.
- A bridge applies only to its exact source/target objects, operators, pins, assumptions, and parameter transforms.
- Lean status derives from the full proof and import closure.
- Human decisions are authenticated, scoped, current, unrevoked, and non-replayable.
- Restore never selects a head older than an independently witnessed irreversible event.
- Acceptance and audit results apply only to one release digest.

## 10. Missing ownership

Explicit accountable ownership is missing for:

- Event log and commit reducer
- ControlState and gate lifecycle
- Principal/credential registry
- Definition-head policy
- Claim and bridge schemas
- Audit question/applicability policy
- Counterexample equivalence and demotion completion
- Checkpoint trust anchor and disaster recovery
- Schema migration and compatibility
- Release manifest and package signing
- Model admission and replacement
- Data provenance
- Capacity and retention
- Acceptance-test execution

The current practice of naming an orchestrator or auditor in prose does not establish operational ownership.

## 11. Missing interfaces

Required interfaces include:

- `I.Commit(command, expected_head, stop_epoch)`
- `I.ControlEvent(signed_gate_or_stop)`
- `I.RoleBind` and `I.RoleRevoke`
- `I.ClaimRegister`
- `I.PromotionIntent`
- `I.Promote`
- `I.AuditOpen` and `I.AuditFinalize`
- `I.BridgeRegister`
- `I.DefinitionHeadAdvance`
- `I.CounterexampleClosure`
- `I.DemotionWaveApply`
- `I.LeanBuildAttest`
- `I.CheckpointCreate` and strengthened `I.CheckpointValidate`
- `I.Migrate`
- `I.ReleaseManifestVerify`
- `I.ModelAdmit`, `I.ModelReplace`, and `I.ModelRollback`
- `I.DataProvenanceCheck`

Each needs versioning, authentication, preconditions, postconditions, atomicity, errors, retries, timeouts, idempotency, and audit events.

## 12. Missing audits

The package lacks defined audits for:

- Reducer determinism and authorization
- Promotion dependency closure
- Typed bridge compatibility
- Active-definition-head use
- Counterexample and demotion-wave closure
- Principal independence and role appointment
- Human decision authenticity and expiry
- Lean full-closure reproducibility
- Data-independence and taint
- Checkpoint rollback resistance
- Migration equivalence
- Model replacement/admission
- Storage and restart capacity
- Package-manifest integrity
- Acceptance-evidence reproducibility

## 13. Missing validation

Required validation is absent:

- Property-based tests for every reducer invariant
- State-machine reachability and model checking
- Invalid audit-question-set fixtures
- Promotion TOCTOU tests
- Bridge parameter/domain mismatch tests
- Archived-counterexample resurrection tests
- Crash injection after every demotion/recovery write
- Hard-stop races against every mutating command
- Checkpoint truncation and metadata corruption tests
- Historical-version migration fixtures
- Lean proof/import mutation tests
- Model-replacement canaries
- Multi-year load and replay tests
- Executable positive and negative E2E traces

## 14. Missing theorem safeguards

Before theorem promotion can be trusted, the architecture needs:

- Content-addressed mathematical statements
- Typed essential and nonessential dependency edges
- Explicit assumption discharge
- Exact certificate/operator/object/pin bindings
- Axis-specific promotion with compare-and-swap
- Promotion intent fixed before audit
- Exact audit digest and freshness window
- Historical counterexample closure
- Active-definition-head validation
- Open-demotion-wave exclusion
- Explicit inference-bridge theorem transforms
- Non-resurrection across renamed or superseding claims
- Deterministic contradiction and equivalence handling

## 15. Missing Lean safeguards

The Lean subsystem needs:

- Source-tree and build-recipe hashes
- Elaborated declaration and proof-body hashes
- Imported declaration and dependency-manifest hashes
- Exact theorem-to-Claim binding
- Toolchain, mathlib, environment, and option closure
- Total status precedence
- `build_ok` required for every proof-bearing status
- Axiom provenance and dependency blast radius
- Staleness on upstream refutation, demotion, bridge change, or claim change
- Reproducible independent build attestations
- Negative tests proving status demotion on every relevant mutation

## 16. Missing research safeguards

The research loop lacks:

- Enforced data lineage and taint isolation
- Policy-derived attack-class applicability
- Strong independence domains for disconfirmation and certification
- Prompt-injection isolation for literature and tool outputs
- Model capability admission and calibration
- Token, money, wall-time, storage, and human-review budgets
- Escalation for reviewer fatigue and gate backlog
- Explicit privacy, licensing, and sensitive-data boundaries
- Research reproducibility bundles
- Long-run drift monitoring for scope, model behavior, and audit quality

## 17. Package integrity issues

- The live package contains 52 files but has no source-control root, release manifest, or file hashes.
- The banner is not an immutable snapshot identifier.
- Audit evidence is redacted and omits all tool results.
- Critique summaries openly state that full transcripts live behind agent IDs rather than in the package.
- Historical and current artifacts are mixed without machine-readable supersession metadata.
- Acceptance results are not signed, timestamped, or digest-bound.
- No artifact inventory proves that no ResearchState or execution evidence exists.
- The package is therefore neither self-contained nor independently reproducible.

## 18. Cross-document inconsistencies

- ART-22 PASS with `BRIDGE_OPEN` contradicts ART-01 and ART-11.
- ART-11 declares 16 answers but defines 18 questions.
- ART-15 says humans alone decide gates but defines `N/A_UTILITY_ACK` as an Integration Auditor acknowledgment; ART-07 also permits auditor acknowledgment.
- ART-05 does not grant the Frontier Scheduler commit authority, while ART-08b says the scheduler alone commits selection.
- ART-06 says committed events are authoritative; ART-19 says only promotions and cycle-ledger commits persist authority.
- ART-09 uses multi-axis status while ART-06 uses unary `from_status`/`to_status`.
- ART-08 requires two attack/audit passes but provides no complete second-pass route.
- ART-04b’s roster and registries do not match mandatory duties and authoritative registries elsewhere.
- Human gate bootstrap depends on ResearchState before ResearchState authority exists.
- ART-20b C4 still references hard rules 1–20, while ART-20 contains rules through 23 plus 3b/3c.

## 19. Broken references

A live scan found **62 broken Markdown link instances across 36 unique targets**:

- `critiques/INDEX.md`: 22
- `critiques/SUMMARIES.md`: 25
- Iteration records: 15

The links are bare agent UUID-like paths with no local target or durable resolver. Examples begin in [critiques/INDEX.md](/Users/nicholasmino/Desktop/Research/Work/architecture/critiques/INDEX.md:5), while [SUMMARIES explicitly says the full transcripts live behind those IDs](/Users/nicholasmino/Desktop/Research/Work/architecture/critiques/SUMMARIES.md:3).

ART-04b also cites nonexistent “charter §IX” in [its non-deletion rationale](/Users/nicholasmino/Desktop/Research/Work/architecture/04-agents/OPERABLE_MINIMAL_PROFILE.md:25).

Closure requires zero unresolved normative/evidence links.

## 20. Version inconsistencies

- README declares authoritative `ARCH-0.3-ITER5`.
- ART-25 audits only `ARCH-0.3`.
- Iteration 9 records material changes after the Iteration 5 banner.
- ART-01, ART-20b, ART-23, and IMPLEMENTATION_BLOCK remain stamped `ARCH-0.2`.
- ART-21 still labels current status as R17 while declaring R20 in rows.
- No event, schema, checkpoint, reducer, canonicalization, or migration versions exist.
- No digest ties any audit to exact bytes.

The banner’s claim that old headers are merely historical does not solve version identity; it replaces explicit version discipline with an unverified prose override.

## 21. Acceptance-test weaknesses

The T01–T24 suite is predominantly document-presence testing:

- T01 checks files, not semantics.
- T04 asserts a total authority lattice that lacks a committer and conflict tie-breaks.
- T08 misses the impossible 16-versus-18 cardinality.
- T10 repeats the unsupported claim that Lean status is a function of the manifest.
- T15 relies on a contradictory narrative trace.
- T16 is false because no audit is bound to the live version.
- T17 is unverifiable because ordering, independence, evidence, and package identity are not proven.
- T18/T19 depend on broken critique links.
- T20 infers no execution from gate prose rather than a state/log inventory.
- T21–T23 pass on interface-name presence.
- No test has a run ID, runner, timestamp, package digest, expected/actual result, or immutable evidence set.

Consequently, the PASS table is verification theater, not conformance evidence.

## 22. Traceability weaknesses

- Promotion booleans are not linked to the evidence used to derive them.
- Audits are not linked to exact statements or intended target axes.
- Claims lack immutable statement hashes.
- Bridges do not reference exact source/target certificates.
- Counterexamples are not transitively linked into promotion closure.
- Human decisions lack authenticated actors and lifecycle.
- Lean manifests do not cover full source/import closure.
- Acceptance tests do not map assertions to immutable evidence.
- Audit and adversarial reviews do not map to a release digest.
- Ownership is often inferred rather than normative.
- Historical evidence links do not resolve.

The package has many IDs but lacks an end-to-end evidence chain.

## 23. Long-term operation weaknesses

- No safe state/event migration contract
- No replicated or external monotonic log witness
- No RPO, RTO, durability, or availability targets
- No checkpoint replica selection or disaster-restore drill
- No crash-resumable demotion or recovery operations
- No capacity model or bounded replay/index-rebuild time
- No storage tiers, compaction proof, or retention schedule
- No key rotation, credential revocation, or secret-management plan
- No model replacement or emergency withdrawal protocol
- No gate expiry/revocation lifecycle
- No operational telemetry, alerting, or incident command
- No audit succession or reviewer-fatigue control
- No legal-hold/deletion reconciliation
- Budgets count cycles but omit money, tokens, wall time, storage, and human workload

The “indefinite” operating claim is unsupported.

## 24. Overall architecture maturity (0–10) with justification

**2.5/10**

- Scope and epistemic intent: **6/10**
- Mathematical workflow concepts: **5/10**
- Normative state and interface model: **2/10**
- Security and authority enforcement: **1/10**
- Recovery and long-term operations: **1/10**
- Executable validation: **0.5/10**
- Package/release integrity: **2/10**

The package is more mature as a research-governance requirements catalogue than as an architecture. Blueprint maturity is low because the controls that matter most are neither machine-defined nor validated.

## 25. Readiness for implementation planning (YES/NO + conditions)

**NO.**

Implementation planning may begin only after:

- The six Critical blockers are closed.
- R20/C12 and the current T-suite PASS are withdrawn or marked superseded.
- A canonical machine-readable state, claim, audit, and promotion model exists.
- Control, identity, stop, recovery, migration, and release semantics are defined.
- A non-autonomous reference interpreter and adversarial conformance suite execute successfully.
- A frozen release digest passes a new full independent audit and two strictly subsequent clean adversarial rounds.
- A human then evaluates `DESIGN_FINAL`; prior human approval would not cure the technical defects.

## 26. Exactly what must change before implementation planning (ordered checklist)

1. Keep `IMPLEMENTATION_BLOCK` active and mark `AUDIT-0.3-R20`, C11, C12, and T16–T17 as superseded or unverified.
2. Freeze a new release identity with a complete path/artifact/version/SHA-256 manifest.
3. Define canonical serialization, hash suite, command/event envelope, event ordering, and reducer version.
4. Implement the normative specification as a non-autonomous reference reducer and schema validator.
5. Create authenticated ControlState for gates, phase, role bindings, stop epochs, revocation, and bootstrap.
6. Define principals, credentials, capability authorization, signed human decisions, independence domains, and appointment authority.
7. Add `I.Commit` with expected-head CAS, stop-epoch fencing, idempotency, deterministic predicate computation, and atomic projections.
8. Add an immutable content-addressed Claim schema with exact statement, assumptions, dependencies, axes, chain segment, certificates, operators, and pins.
9. Replace the Bridge schema with exact typed theorem edges and explicit parameter/failure-budget transforms.
10. Replace promotion booleans with immutable evidence references and reducer-computed, axis-specific predicates.
11. Lock promotion intent before S10 and bind every audit to the exact target snapshot and policy version.
12. Replace the audit answer schema with a versioned question registry; resolve 16 versus 18; derive applicability and blocker semantics.
13. Add active definition heads and atomically check them at audit and promotion.
14. Add historical counterexample closure across archived/equivalent/superseded claims and dependency ancestors.
15. Implement durable crash-resumable demotion waves and block promotion/frontier changes while relevant waves remain open.
16. Redesign the Lean manifest around the complete source, declaration, proof, import, axiom, build, and dependency closure.
17. Rewrite the FSM as a machine-readable transition relation with a reachable two-pass review loop.
18. Correct ART-22 and convert it into executable positive and negative fixtures.
19. Authenticate checkpoint envelopes, externally anchor monotonic log heads, and cover every irreversible safety event.
20. Version state, events, reducers, checkpoints, canonicalization, and migrations; add replay-equivalence fixtures.
21. Add data-provenance and taint enforcement for parameter independence.
22. Define model admission, provenance, shadow/canary replacement, rollback, and revalidation.
23. Specify storage, retention, compaction, replication, RPO/RTO, capacity, backpressure, and operational budgets.
24. Assign accountable owners and complete every interface’s preconditions, postconditions, errors, retries, timeouts, atomicity, and observability.
25. Consolidate OPERABLE_MINIMAL into the sole runtime contract and move non-runtime critic/governance catalogs to appendices.
26. Repair all 62 broken links and materialize every relied-upon audit or critique report locally.
27. Create digest-bound executable acceptance results covering concurrency, crash, restore, migration, theorem, bridge, Lean, and identity attacks.
28. Run a full independent audit against the frozen digest with sufficient unredacted or independently reproducible evidence.
29. Run two strictly subsequent independent adversarial rounds against that unchanged digest.
30. Only after all preceding items pass should the human consider `DESIGN_FINAL` and authorize implementation planning.
