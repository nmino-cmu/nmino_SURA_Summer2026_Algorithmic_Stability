## Ten-scenario tabletop

| # | Scenario | Verdict | Evidence and adversarial result |
|---|---|---|---|
| 1 | Successful theorem discovery | **PARTIAL** | The research FSM, promotion predicates, independent certifier, integration audit, and Lean manifest are specified in [ART-08](/Users/nicholasmino/Desktop/Research/Work/architecture/08-research-cycle/RESEARCH_CYCLE_FSM.md:25), [ART-09](/Users/nicholasmino/Desktop/Research/Work/architecture/09-theorem-status/THEOREM_STATUS_FSM.md:41), and [ART-13](/Users/nicholasmino/Desktop/Research/Work/architecture/13-proof-review/PROOF_REVIEW.md:34). But the only E2E trace stops at CONJECTURE/PARTIAL_RESULT and explicitly is not a theorem or ResearchState execution: [ART-22](/Users/nicholasmino/Desktop/Research/Work/architecture/22-example-trace/E2E_TRACE.md:25). No positive promotion, crash, replay, or restart trace exists. |
| 2 | Counterexample destroys promoted theorem | **PARTIAL** | `FULL_REFUTE` requires synchronous target demotion and dependent `NEEDS_REVIEW`; incomplete waves block S14: [ART-12](/Users/nicholasmino/Desktop/Research/Work/architecture/12-counterexample/COUNTEREXAMPLE_PROTOCOL.md:82). The wave itself lacks durable phase, cursor, affected-set, commit marker, and idempotency semantics: [ART-16](/Users/nicholasmino/Desktop/Research/Work/architecture/16-failure-recovery/FAILURE_RECOVERY.md:59). A crash mid-wave is not safely resumable. |
| 3 | Definition change after multiple proofs | **PARTIAL** | A new pin triggers automatic demotion, invalidates audit PASS, and makes Lean dependents stale: [ART-02](/Users/nicholasmino/Desktop/Research/Work/architecture/02-scope/MATH_SCOPE.md:75), [ART-10](/Users/nicholasmino/Desktop/Research/Work/architecture/10-lean/LEAN_FSM.md:50), [ART-11](/Users/nicholasmino/Desktop/Research/Work/architecture/11-integration-audit/INTEGRATION_AUDIT.md:100). There is no state/schema migration protocol or resumable bulk revalidation procedure. |
| 4 | Lean rejects previously accepted theorem | **PASS** | Lean status is derived from a manifest, toolchain/pin changes cause `LEAN_STALE`, and gaps trigger demotion and triage without silent axioms: [ART-10](/Users/nicholasmino/Desktop/Research/Work/architecture/10-lean/LEAN_FSM.md:28), [ART-16 P4](/Users/nicholasmino/Desktop/Research/Work/architecture/16-failure-recovery/FAILURE_RECOVERY.md:42), [ART-09](/Users/nicholasmino/Desktop/Research/Work/architecture/09-theorem-status/THEOREM_STATUS_FSM.md:61). |
| 5 | Inference bridge failure | **PASS** | `CX.bridge_fail` is mandatory when applicable; OPEN/ASSUMED bridges fail inference milestones; a full refutation demotes dependents: [ART-12](/Users/nicholasmino/Desktop/Research/Work/architecture/12-counterexample/COUNTEREXAMPLE_PROTOCOL.md:41), [ART-11 Q11](/Users/nicholasmino/Desktop/Research/Work/architecture/11-integration-audit/INTEGRATION_AUDIT.md:71). Runtime atomicity remains untested. |
| 6 | Corrupted checkpoint recovery | **FAIL** | The Merkle root covers event payloads, not the checkpoint metadata. Validation checks only the root and refutation watermark; it does not authenticate gate state, pin-table reference, manifest list, audit tail, checkpoint lineage, or an external monotonic high-water mark: [ART-17](/Users/nicholasmino/Desktop/Research/Work/architecture/17-indefinite-ops/INDEFINITE_OPS.md:22), [ART-24](/Users/nicholasmino/Desktop/Research/Work/architecture/24-interfaces/INTERFACE_CONTRACTS.md:41). There is also no replica/backup selection procedure, so “validation fails → S15” is detection, not recovery. |
| 7 | Human interrupt during promotion | **FAIL** | `I.HardStop` is declared immediate and promotion rollback is required: [ART-24](/Users/nicholasmino/Desktop/Research/Work/architecture/24-interfaces/INTERFACE_CONTRACTS.md:36). No linearization point, fencing epoch, isolation level, or compare-and-commit rule prevents a promotion that checked `hard_stop=false` from committing after the interrupt. |
| 8 | Model replacement | **FAIL** | ART-18 defines only report and reconciliation shapes; neither records model/version/prompt/tool policy nor defines admission, shadow evaluation, handoff, revalidation, or rollback: [ART-18](/Users/nicholasmino/Desktop/Research/Work/architecture/18-model-protocols/MODEL_PROTOCOLS.md:24). ART-04 hard-codes Grok/Composer families: [ART-04](/Users/nicholasmino/Desktop/Research/Work/architecture/04-agents/AGENT_ROLES.md:24). |
| 9 | Scope drift attempt | **PASS** | Positive quarantine is required before S02, Orchestrator cannot self-classify `IN_CHAIN`, fields freeze, and Q16 rechecks chain placement: [ART-01](/Users/nicholasmino/Desktop/Research/Work/architecture/01-charter/CHARTER.md:67), [ART-08b](/Users/nicholasmino/Desktop/Research/Work/architecture/08-research-cycle/QUESTION_SELECTION.md:85), [ART-11](/Users/nicholasmino/Desktop/Research/Work/architecture/11-integration-audit/INTEGRATION_AUDIT.md:77). This is the strongest governance path in the package, though semantic classification remains model-dependent. |
| 10 | Accidental data-dependent perturbation | **FAIL** | The architecture requires a `psi_data_dependence` declaration, human gate, audit question, and CX class: [ART-07](/Users/nicholasmino/Desktop/Research/Work/architecture/07-schemas/SCHEMAS.md:24), [ART-15](/Users/nicholasmino/Desktop/Research/Work/architecture/15-human-gates/HUMAN_GATES.md:31), [ART-12](/Users/nicholasmino/Desktop/Research/Work/architecture/12-counterexample/COUNTEREXAMPLE_PROTOCOL.md:48). These controls detect declared or mathematically exposed dependence, not accidental hidden dataflow. A mechanism incorrectly marked `independent` has no provenance/taint control to expose it. |

## Targeted artifact verdicts

| Artifact | Verdict | Core weakness |
|---|---|---|
| ART-16 Failure recovery | **PARTIAL** | Sensible fail-closed playbooks, but no resumable recovery FSM or idempotent transaction schema. |
| ART-17 Indefinite operations | **FAIL** | Checkpoint integrity is incomplete; no migration, durability, checkpoint cadence, RPO/RTO, redundancy, or restore drills. |
| ART-18 Model protocols | **FAIL** | No model provenance, replacement, admission, capability, or recalibration protocol. |
| ART-18b Bullshit linter | **FAIL** | Internally incomplete inputs, ambiguous action mapping, and trivially gameable evidence-ratio rule. |
| ART-19 Memory | **FAIL** | Retrieval hygiene exists; long-term storage growth and bounded operational cost do not. |

## Findings

Schema used for every finding: **ID, severity, status, affected components/scenarios, attack, evidence, impact, required correction, closure test.**

### F-01 — Checkpoint validation cannot establish a safe restore point

- **Severity / status:** CRITICAL / OPEN
- **Affected:** ART-17, ART-24; scenarios 2, 6
- **Attack:** Restore a valid older prefix after later events or alter restore-critical checkpoint metadata independently of the event Merkle root.
- **Evidence:** Checkpoint metadata is listed separately, while the root covers only event payloads; validator output is only `merkle_ok + watermark_ok`: [ART-17](/Users/nicholasmino/Desktop/Research/Work/architecture/17-indefinite-ops/INDEFINITE_OPS.md:22), [ART-24](/Users/nicholasmino/Desktop/Research/Work/architecture/24-interfaces/INTERFACE_CONTRACTS.md:41).
- **Impact:** Refuted claims, released hard stops, stale pins, or invalid manifests can be resurrected.
- **Required correction:** Authenticate the complete checkpoint envelope; specify hash/canonicalization suite; add chained monotonic checkpoint IDs, externally durable refutation/high-water anchors, replica policy, and verified fallback selection.
- **Closure test:** Corrupt or truncate every checkpoint field and event prefix; no stale checkpoint may validate, including when the primary event store loses its newest suffix.

### F-02 — No state, event, or checkpoint migration contract

- **Severity / status:** CRITICAL / OPEN
- **Affected:** ART-06, ART-17, architecture versioning; scenarios 3, 6
- **Attack:** Restart a multi-year deployment using newer code against older events/checkpoints.
- **Evidence:** The checkpoint has no architecture version, event-schema version, canonicalization version, migration ID, or runtime build. The bootstrap contract hash exists only for initial DesignState import: [ART-03](/Users/nicholasmino/Desktop/Research/Work/architecture/03-context/SYSTEM_CONTEXT.md:86).
- **Impact:** Replay semantics can change silently or old state can become unreadable.
- **Required correction:** Version all event/checkpoint schemas; define forward migrations, compatibility windows, migrator hashes, pre/post-invariant checks, rollback policy, and mixed-version deployment rules.
- **Closure test:** Restore fixtures from every supported historical version and prove identical authoritative registries and invariant outcomes after migration.

### F-03 — Model replacement is architecturally undefined

- **Severity / status:** CRITICAL / OPEN
- **Affected:** ART-04, ART-18, ART-18b; scenario 8
- **Attack:** Replace Grok or Composer with a model having different tool behavior, calibration, context limits, or safety characteristics.
- **Evidence:** Reports contain no model provenance fields, while role tables name specific model families: [ART-18](/Users/nicholasmino/Desktop/Research/Work/architecture/18-model-protocols/MODEL_PROTOCOLS.md:24), [ART-04](/Users/nicholasmino/Desktop/Research/Work/architecture/04-agents/AGENT_ROLES.md:26).
- **Impact:** Role separation and prior audit confidence do not survive model substitution.
- **Required correction:** Record provider/model/version, prompt hash, tool-policy hash and capability profile; define admission evaluations, shadow/canary operation, handoff state, independence tests, revalidation scope, rollback, and emergency withdrawal.
- **Closure test:** Replace each role with a deliberately weaker model and demonstrate that admission fails or the rollout safely rolls back without canonical-state corruption.

### F-04 — Human interrupt has no concurrency or fencing semantics

- **Severity / status:** HIGH / OPEN
- **Affected:** ART-06, ART-15, ART-24; scenario 7
- **Attack:** Race `I.HardStop` against a promotion or S13/S14 commit.
- **Impact:** A mutation can commit after the human believes the system is frozen.
- **Required correction:** Define a serializable commit boundary using a monotonically increasing stop epoch/fencing token; every mutation must compare the epoch at final commit.
- **Closure test:** Exhaustively race and crash-inject interrupt versus every mutating transition; zero post-freeze commits are allowed.

### F-05 — Recovery and demotion waves are not crash-resumable

- **Severity / status:** HIGH / OPEN
- **Affected:** ART-16, ART-12, ART-24; scenarios 2, 3
- **Evidence:** The demotion-wave schema contains an order but no durable phase, cursor, effect set, or completion proof: [ART-16](/Users/nicholasmino/Desktop/Research/Work/architecture/16-failure-recovery/FAILURE_RECOVERY.md:59).
- **Impact:** Replay can double-apply, omit, or indefinitely strand dependent demotions.
- **Required correction:** Introduce recovery operation IDs, durable intent/effect sets, idempotency keys, phase transitions, commit markers, and restart rules.
- **Closure test:** Crash after every write in every recovery playbook and prove convergence to the same final state.

### F-06 — Memory growth is explicitly unbounded but operationally unmanaged

- **Severity / status:** HIGH / OPEN
- **Affected:** ART-17, ART-19
- **Attack:** Years of append-only events, counterexamples, failed proofs, checkpoints, manifests, and summaries exhaust storage or make replay/index rebuild infeasible.
- **Evidence:** History is append-only and pruning never deletes, while ART-19 only says to “prefer” primary objects within working context: [ART-17](/Users/nicholasmino/Desktop/Research/Work/architecture/17-indefinite-ops/INDEFINITE_OPS.md:55), [ART-19](/Users/nicholasmino/Desktop/Research/Work/architecture/19-memory/MEMORY.md:27). Retention conflict is acknowledged but unresolved: [LIMITATIONS](/Users/nicholasmino/Desktop/Research/Work/architecture/23-limitations/LIMITATIONS.md:11).
- **Impact:** “Indefinite” operation eventually degrades or stops.
- **Required correction:** Add capacity models, hard context/query budgets, hot/warm/cold tiers, bounded pagination, index lifecycle, safe compaction proofs, checkpoint retention, backpressure, and legal-hold/deletion governance.
- **Closure test:** Multi-year synthetic load must remain within declared storage, retrieval-latency, and restart-time limits.

### F-07 — Data independence is self-attested, not enforced

- **Severity / status:** HIGH / OPEN
- **Affected:** ART-07, ART-11, ART-12; scenario 10
- **Attack:** Calibration code reads dataset-derived state while its mechanism row declares `independent`.
- **Impact:** Stability and inference claims may be invalid while all schema checks pass.
- **Required correction:** Require a typed parameter-derivation graph, dataset provenance/taint tracking, audited sub-mechanism certificate, and executable negative tests.
- **Closure test:** Hidden direct and transitive dataset dependencies must be detected before promotion.

### F-08 — ART-18b is ambiguous and gameable

- **Severity / status:** HIGH / OPEN
- **Affected:** ART-18b, synthesis governance
- **Attack:** Pad prose with unrelated IDs to reduce B4; use stale IDs; exploit unspecified predicate-to-action mapping.
- **Evidence:** Inputs omit `cx_ids` even though B4 requires them, and “any predicate true → action” does not map predicates to QUARANTINE/BLOCK/ESCALATE: [ART-18b](/Users/nicholasmino/Desktop/Research/Work/architecture/18-model-protocols/BULLSHIT_LINTER.md:11).
- **Impact:** Different implementations can emit different verdicts, and contribution theater can pass syntactic checks.
- **Required correction:** Version a deterministic decision table; validate ID existence, relevance, status, and pins; prohibit denominator padding; make QUARANTINE/ESCALATE commit semantics explicit.
- **Closure test:** Adversarial corpora covering stale IDs, irrelevant-ID padding, paraphrased theorem claims, and unresolved citations must produce fixed expected verdicts.

### F-09 — Governance decisions lack the lifecycle claimed by the authority lattice

- **Severity / status:** HIGH / OPEN
- **Affected:** ART-05, ART-15, checkpoint gate state
- **Attack:** Reuse an old or revoked approval indefinitely, or restore it from a checkpoint.
- **Evidence:** The authority lattice says human decisions are typed and expire, but the canonical `human_decisions` schema has no actor, issuance time, expiry, revocation, version, or authentication fields: [ART-05](/Users/nicholasmino/Desktop/Research/Work/architecture/05-authority/AUTHORITY_MATRIX.md:24), [ART-15](/Users/nicholasmino/Desktop/Research/Work/architecture/15-human-gates/HUMAN_GATES.md:9).
- **Impact:** Stale gates can authorize future behavior with no auditable decision lifecycle.
- **Required correction:** Add authenticated decision identity, issued/expiry/revoked timestamps, scope predicate, supersession chain, quorum rules, and non-overridable epistemic constraints.
- **Closure test:** Expired/revoked decisions must fail both live promotion and checkpoint restore.

## Blockers

Before `DESIGN_FINAL` approval for this operational scope:

1. Close F-01 and F-02 with an authenticated, monotonic, migration-aware checkpoint format.
2. Close F-03 with a real model replacement/admission protocol.
3. Close F-04 and F-05 with transactional, fenced, crash-resumable semantics.
4. Close F-06 with measurable storage, retrieval, and restart bounds.
5. Close F-07 for accidental data dependence.
6. Resolve ART-18b and governance lifecycle defects.
7. Add executable acceptance tests, crash injection, migration fixtures, concurrency races, and restore drills. The existing document-presence suite is insufficient.

## Maturity and readiness

- **Epistemic architecture maturity:** 3/5 — coherent theorem, counterexample, scope, audit, and Lean controls.
- **Long-term operations maturity:** 1/5 — core durability and lifecycle contracts are missing.
- **Implementation/validation maturity:** 0/5 — intentionally unimplemented and untested.
- **`DESIGN_FINAL` readiness for the audited focus:** **FAIL / HOLD**
- **Implementation start:** **BLOCKED**
- **Research execution:** **BLOCKED**
- **Years-long autonomous operation:** **NOT READY**

The active implementation block is correct and should remain in force.
