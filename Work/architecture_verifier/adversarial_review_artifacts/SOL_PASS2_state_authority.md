## Scope examined

ART-03, ART-04, ART-04b, ART-05, ART-06, ART-15, ART-16, ART-17, ART-19, ART-20, ART-20b, ART-24, `IMPLEMENTATION_BLOCK`, and `FINAL_AUDIT`; cross-checked against ART-01, ART-07–13, ART-18, ART-21, and the R20 evidence transcript.

## Assumptions

- An interface name is not enforcement unless its principal, atomicity boundary, state precondition, and failure behavior are defined.
- Actor IDs, role names, and predicate booleans are attacker-controlled unless bound to authenticated provenance.
- Restore safety must survive loss or corruption of the local state being restored.
- Human authority must pass through a defined, durable control path rather than undocumented out-of-band edits.

## `identified_flaws[]`

### ASA-01 — No authoritative committer or atomic event reducer

- **Severity:** CRITICAL
- **Description:** Committed events are declared authoritative, while registries are also called authoritative; ART-19 then says only promotions and cycle-ledger commits persist authority. The authority matrix grants proposal rights but never grants commit rights. `I.ProposeWrite` explicitly stops at a pending transaction, while `I.Frontier` independently “commits.” See [ART-06:L12](/Users/nicholasmino/Desktop/Research/Work/architecture/06-state/STATE_MODEL.md:12), [ART-06:L31](/Users/nicholasmino/Desktop/Research/Work/architecture/06-state/STATE_MODEL.md:31), [ART-19:L37](/Users/nicholasmino/Desktop/Research/Work/architecture/19-memory/MEMORY.md:37), [ART-05:L38](/Users/nicholasmino/Desktop/Research/Work/architecture/05-authority/AUTHORITY_MATRIX.md:38), and [ART-24:L29](/Users/nicholasmino/Desktop/Research/Work/architecture/24-interfaces/INTERFACE_CONTRACTS.md:29).
- **Concrete failure scenario:** An undocumented “system” component appends a promotion containing `eio_pass=true`; no specified committer exists to recompute the predicate or reject the actor. Alternatively, literal implementation deadlocks because nobody may commit.
- **Affected components:** All registries, ownership, authority lattice, promotion, hard stop, recovery.
- **Proposed correction:** Define one typed `I.Commit` capability: authenticated principal, event schema, expected-head/CAS, idempotency key, deterministic reducer, operation-specific authorization, global hard-stop check, and atomic projection updates. Ban direct registry mutation.
- **Tradeoffs:** A centralized logical write path adds latency but can still be replicated underneath.
- **Unresolved question:** Who currently owns event-log append authority?
- **Confidence:** 0.99

### ASA-02 — Gate bootstrap creates dual-loop deadlock or bleed

- **Severity:** CRITICAL
- **Description:** `human_decisions` exists only as a ResearchState registry, but ResearchState ownership begins after `RESEARCH_EXECUTION_START`; the startup gates must be recorded before that point. `IMPLEMENTATION_BLOCK` references an undefined “gate log.” See [ART-03:L95](/Users/nicholasmino/Desktop/Research/Work/architecture/03-context/SYSTEM_CONTEXT.md:95), [ART-03:L98](/Users/nicholasmino/Desktop/Research/Work/architecture/03-context/SYSTEM_CONTEXT.md:98), [ART-06:L51](/Users/nicholasmino/Desktop/Research/Work/architecture/06-state/STATE_MODEL.md:51), [ART-15:L10](/Users/nicholasmino/Desktop/Research/Work/architecture/15-human-gates/HUMAN_GATES.md:10), and [IMPLEMENTATION_BLOCK:L15](/Users/nicholasmino/Desktop/Research/Work/architecture/IMPLEMENTATION_BLOCK.md:15).
- **Concrete failure scenario:** `DESIGN_FINAL` cannot be durably recorded without writing ResearchState before research authority exists. Allowing an out-of-band Markdown edit solves the deadlock by creating a second authority and bypass channel.
- **Affected components:** DesignState/ResearchState separation, human gates, bootstrap import, implementation block.
- **Proposed correction:** Create an independent append-only `ControlState`, live from system bootstrap, for gates, phase, role bindings, and stop epochs. Research commits must carry a ControlState phase receipt. Make DesignState import one-way, schema-allowlisted, hashed, and bound to exact approval IDs.
- **Tradeoffs:** Adds a third store, but removes the circular dependency.
- **Unresolved question:** Is the intended gate log DesignState, ResearchState, or an external system?
- **Confidence:** 0.99

### ASA-03 — `hard_stop` is neither linearizable nor safely releasable

- **Severity:** CRITICAL
- **Description:** `I.HardStop` says “immediate” but defines no write fence, cancellation epoch, or serialization with in-flight commits. During a stop, ResearchState mutations are forbidden except hard-stop set/clear, yet release requires first appending a `human_decisions` row—another ResearchState mutation. See [ART-24:L36](/Users/nicholasmino/Desktop/Research/Work/architecture/24-interfaces/INTERFACE_CONTRACTS.md:36), [ART-06:L55](/Users/nicholasmino/Desktop/Research/Work/architecture/06-state/STATE_MODEL.md:55), and [ART-15:L74](/Users/nicholasmino/Desktop/Research/Work/architecture/15-human-gates/HUMAN_GATES.md:74).
- **Concrete failure scenario:** A promotion validates while `active=false`; a stop then commits; the promotion commits afterward. On release, literal enforcement blocks the required decision append. An ad hoc “gate write” exception instead becomes an undocumented mutation bypass.
- **Affected components:** Interruptibility, promotion, frontier, recovery, human authority.
- **Proposed correction:** Use a monotonic `stop_epoch`. Every commit must atomically compare the expected epoch. Stop increments the epoch and fences in-flight writes. Release must be one narrowly typed atomic event containing the signed human decision and state transition.
- **Tradeoffs:** Requires coordination at the commit boundary.
- **Unresolved question:** What is the linearization point between a stop signal and every other mutation?
- **Confidence:** 0.99

### ASA-04 — Checkpoint freshness test cannot detect prefix rollback

- **Severity:** CRITICAL
- **Description:** The checkpoint stores its own Merkle root, and validation compares `event_seq_max` with the maximum FULL_REFUTE visible in the available event log. No independent monotonic head or external trust anchor exists. See [ART-17:L24](/Users/nicholasmino/Desktop/Research/Work/architecture/17-indefinite-ops/INDEFINITE_OPS.md:24), [ART-17:L40](/Users/nicholasmino/Desktop/Research/Work/architecture/17-indefinite-ops/INDEFINITE_OPS.md:40), and [ART-17:L47](/Users/nicholasmino/Desktop/Research/Work/architecture/17-indefinite-ops/INDEFINITE_OPS.md:47).
- **Concrete failure scenario:** Restore a checkpoint immediately before a FULL_REFUTE and present only that valid prefix. The omitted refutation is not visible to `max_seq(FULL_REFUTE events)`, so both Merkle and watermark checks pass. The same path can roll back later human denials, hard stops, contradictions, vetoes, and demotions even when it does not cross a refutation.
- **Affected components:** Recovery, checkpointing, human gates, hard stop, demotion.
- **Proposed correction:** Anchor signed log-head receipts outside the restorable store. The restore floor must cover every irreversible safety event, not only FULL_REFUTE. Prefer replay from the anchored head; never authorize truncation using evidence contained solely in the candidate checkpoint.
- **Tradeoffs:** Requires an independent durable witness or replicated transparency log.
- **Unresolved question:** Where does the validator obtain the latest trustworthy head after corruption?
- **Confidence:** 0.99

### ASA-05 — Promotion transaction is an assertion bag, not a proof-carrying transaction

- **Severity:** CRITICAL
- **Description:** The promotion schema accepts caller-supplied booleans such as `dep_closure_ok`, `contradiction_clear`, `eio_pass`, `lit_closure_ok`, and `hop_chain_ok`. It omits EIO decision ID, certifier/proposer provenance, gate decisions, cycle and quarantine snapshot, stop epoch, expected log head, demotion-wave state, attack records, and status-specific evidence. It also uses unary `from_status`/`to_status` despite the theorem FSM being multi-axis. See [ART-06:L69](/Users/nicholasmino/Desktop/Research/Work/architecture/06-state/STATE_MODEL.md:69) and [ART-09:L27](/Users/nicholasmino/Desktop/Research/Work/architecture/09-theorem-status/THEOREM_STATUS_FSM.md:27).
- **Concrete failure scenario:** Submit `CONJECTURE → PROVED_ON_PAPER` with all booleans true, an optional/missing audit ID, and invented role labels. No interface is responsible for deriving the predicates from authoritative state.
- **Affected components:** Promotion, EIO, proof certification, literature, gates, quarantine, role ceiling.
- **Proposed correction:** Remove authoritative boolean inputs. Require immutable evidence references and compute every predicate inside `I.Commit` from pre-state. Define exact per-target-status predicate matrices and multi-axis compare-and-swap.
- **Tradeoffs:** Larger transactions and more reducer logic.
- **Unresolved question:** Which component currently computes and attests each boolean?
- **Confidence:** 0.99

### ASA-06 — Demotion-wave completeness is unrepresentable

- **Severity:** CRITICAL
- **Description:** The demotion wave contains only an ID, trigger, prose order, and an `incomplete_wave` assertion. It has no registry, status, closure snapshot, cursor, target set, completion proof, or idempotency semantics. ART-06 does not list demotion waves as state. See [ART-16:L59](/Users/nicholasmino/Desktop/Research/Work/architecture/16-failure-recovery/FAILURE_RECOVERY.md:59), [ART-06:L31](/Users/nicholasmino/Desktop/Research/Work/architecture/06-state/STATE_MODEL.md:31), and [ART-24:L47](/Users/nicholasmino/Desktop/Research/Work/architecture/24-interfaces/INTERFACE_CONTRACTS.md:47).
- **Concrete failure scenario:** A FULL_REFUTE demotes one direct claim, leaves several DAG dependents PROVED, and records a nonempty `demotion_triggered[]`. There is no authoritative predicate proving the closure complete, so S14 can proceed.
- **Affected components:** Counterexamples, theorem DAG, Lean labels, recovery precedence, frontier.
- **Proposed correction:** Add a demotion-wave registry with trigger-head, closure hash, expected targets, per-target effects, `OPEN/APPLYING/COMPLETE/FAILED`, cursor, completion event, and an unconditional promotion/frontier blocker while any relevant wave is open.
- **Tradeoffs:** Demotions become durable workflows rather than a simple transaction.
- **Unresolved question:** How is an incomplete wave discovered after restart?
- **Confidence:** 0.99

### ASA-07 — EIO and independence controls are capturable role labels

- **Severity:** CRITICAL
- **Description:** Grok assigns role instances; role separation is mostly string inequality. The only broad anti-collusion rule prevents the same agent ID from being the sole proposer, prover, and auditor. There is no principal registry, model attestation, appointment authority, or independence domain. “Grok (newest)” is also a moving model target. See [ART-04:L12](/Users/nicholasmino/Desktop/Research/Work/architecture/04-agents/AGENT_ROLES.md:12), [ART-04:L28](/Users/nicholasmino/Desktop/Research/Work/architecture/04-agents/AGENT_ROLES.md:28), [ART-04:L42](/Users/nicholasmino/Desktop/Research/Work/architecture/04-agents/AGENT_ROLES.md:42), and [ART-04:L71](/Users/nicholasmino/Desktop/Research/Work/architecture/04-agents/AGENT_ROLES.md:71).
- **Concrete failure scenario:** One orchestrator starts the same underlying model under new IDs as scheduler, certifier, auditor, and EIO. All ID inequalities and `roles_invoked[]` checks pass. Replacing “newest” changes behavior without a required C12 reset because the reset list excludes ART-04 and most trust-boundary artifacts.
- **Affected components:** EIO veto, proof separation, quarantine ownership, Full-System Audit, model replacement.
- **Proposed correction:** Introduce immutable role bindings containing principal/service identity, model/provider/version hash, prompt and tool-policy hash, issuer, validity interval, and independence domain. The orchestrator must not appoint its own EIO, certifier, or auditor. Any model or authority binding change must invalidate active audit credit.
- **Tradeoffs:** Less flexible model swapping and more operational identity management.
- **Unresolved question:** What constitutes a distinct agent instance beyond an arbitrary ID?
- **Confidence:** 0.98

### ASA-08 — Quarantine freeze does not preserve historical evidence

- **Severity:** HIGH
- **Description:** Quarantine is keyed only by `q_id`, has no cycle, version, event sequence, or content hash, and is frozen only until cycle end. Promotions retain merely `hop_chain_ok=true`, not the tuple used to calculate it. See [ART-06:L54](/Users/nicholasmino/Desktop/Research/Work/architecture/06-state/STATE_MODEL.md:54) and [ART-06:L71](/Users/nicholasmino/Desktop/Research/Work/architecture/06-state/STATE_MODEL.md:71).
- **Concrete failure scenario:** A captured scheduler supplies a new ID and classifies an orchestrator question as `IN_CHAIN`; after S16 the same quarantine row is changed. The promoted claim has no immutable snapshot proving the original chain link or classifier.
- **Affected components:** S02 lock, admissibility, hop checks, promotion evidence, retrieval.
- **Proposed correction:** Make each lock immutable and keyed by `{cycle_id,q_id,lock_seq}`. Bind its content hash and authenticated role binding into cards, audits, and promotion records. Reclassification creates a new object, never an update.
- **Tradeoffs:** More versions and storage.
- **Unresolved question:** Why does the freeze expire if historical promotions continue depending on it?
- **Confidence:** 0.97

### ASA-09 — Authority “lattice” is not total and ranks evidence incorrectly

- **Severity:** HIGH
- **Description:** The document claims total ordering but defines no tie-break for conflicting human decisions, pin versions, audits, or counterexamples; EIO veto is absent from the lattice itself. Human decisions require expiry here, while the human-decision schema has no expiry. The resolution record has no registry or enforcement interface. See [ART-05:L12](/Users/nicholasmino/Desktop/Research/Work/architecture/05-authority/AUTHORITY_MATRIX.md:12), [ART-05:L24](/Users/nicholasmino/Desktop/Research/Work/architecture/05-authority/AUTHORITY_MATRIX.md:24), [ART-05:L36](/Users/nicholasmino/Desktop/Research/Work/architecture/05-authority/AUTHORITY_MATRIX.md:36), and [ART-15:L10](/Users/nicholasmino/Desktop/Research/Work/architecture/15-human-gates/HUMAN_GATES.md:10).
- **Concrete failure scenario:** Two human decisions for the same target conflict; or a valid counterexample conflicts with a Lean manifest. Both implementations can claim compliance while choosing opposite winners.
- **Affected components:** Conflict resolution, EIO, human override, theorem status.
- **Proposed correction:** Replace the global ranking with operation-specific authorization rules: deny/veto precedence, exact version binding, expiry/revocation, and contradiction opening when epistemic evidence conflicts. Persist resolution events through the sole committer.
- **Tradeoffs:** More policy rules, fewer misleadingly simple rankings.
- **Unresolved question:** Should a conflict between machine proof and counterexample ever be “resolved” by rank rather than quarantined?
- **Confidence:** 0.97

### ASA-10 — Human-gate theater remains despite correct token wording

- **Severity:** HIGH
- **Description:** ART-15 correctly states `ESCALATE_HUMAN ≠ gate`, but the actual check mentions only matching `gate_id + target_ref`; it does not explicitly require `decision=approve`, non-expiry, target version, predicate hash, or unused override. `N/A_UTILITY_ACK` is in the mandatory human-gate table but is described as an Integration Auditor acknowledgment. ART-08b calls for anti-easy and weight-revision human gates that have no ART-15 IDs. See [ART-15:L18](/Users/nicholasmino/Desktop/Research/Work/architecture/15-human-gates/HUMAN_GATES.md:18), [ART-15:L24](/Users/nicholasmino/Desktop/Research/Work/architecture/15-human-gates/HUMAN_GATES.md:24), [ART-15:L44](/Users/nicholasmino/Desktop/Research/Work/architecture/15-human-gates/HUMAN_GATES.md:44), and [ART-08b:L21](/Users/nicholasmino/Desktop/Research/Work/architecture/08-research-cycle/QUESTION_SELECTION.md:21).
- **Concrete failure scenario:** A deny/hold row satisfies a literal matcher; an old `OVERRIDE_EIO` is replayed against a revised claim; or a prose “weight revision approved” is accepted because no gate ID exists.
- **Affected components:** Human gates, EIO override, utility waiver, scheduler policy.
- **Proposed correction:** Require signed decisions with subject, `decision=approve`, target version/hash, requested operation, applicable predicate version, expiry, revocation state, and optional one-use nonce. Register missing gates or remove them from normative language.
- **Tradeoffs:** More precise packets and less informal human intervention.
- **Unresolved question:** Is `N/A_UTILITY_ACK` human authority or auditor authority?
- **Confidence:** 0.99

### ASA-11 — Audit convergence is self-referential and stale by construction

- **Severity:** HIGH
- **Description:** C4 permits interface declarations to count as enforcement, while acceptance tests largely check that documents and interface names exist. The C12 reset list excludes ART-03–06, ART-15, ART-20, ART-24, and most role/model changes. R20 was prompted principally as a hard-stop patch regression but is recorded as a full-system PASS. See [ART-20b:L18](/Users/nicholasmino/Desktop/Research/Work/architecture/20-invariants/DESIGN_CONVERGENCE.md:18), [ART-20b:L48](/Users/nicholasmino/Desktop/Research/Work/architecture/20-invariants/DESIGN_CONVERGENCE.md:48), [ART-21:L10](/Users/nicholasmino/Desktop/Research/Work/architecture/21-acceptance-tests/ACCEPTANCE_TESTS.md:10), [R20 transcript:L1](/Users/nicholasmino/Desktop/Research/Work/architecture/adversarial_review_artifacts/862084d7-07ee-4cd1-b29d-b89a6f4955c9.jsonl:1), and [FINAL_AUDIT:L34](/Users/nicholasmino/Desktop/Research/Work/architecture/25-audit-reports/FINAL_AUDIT.md:34).
- **Concrete failure scenario:** Change the authority matrix, gate semantics, committer, or model bindings without triggering C12 reset; retain `AUDIT-0.3-R20` and two clean rounds.
- **Affected components:** C3, C4, C11, C12, FINAL_AUDIT, acceptance tests.
- **Proposed correction:** Supersede R20 and reset C12. Bind audits to a manifest hash of every normative artifact and role/model provenance. Any normative hash change resets credit. Replace presence tests with executable state-machine/model tests and adversarial traces.
- **Tradeoffs:** More frequent audits, but audit credit becomes meaningful.
- **Unresolved question:** What makes the archived auditor independent from the same identity/model-control failure described above?
- **Confidence:** 0.99

## Overengineering attack: delete or merge

- Merge ART-03, ART-04, ART-04b, ART-05, ART-15, and `IMPLEMENTATION_BLOCK` into one normative control-plane and trust-boundary specification.
- Merge ART-06, ART-16, ART-17, ART-19, and ART-24 into one event, commit, recovery, and storage protocol.
- Merge ART-20, ART-20b, and ART-21 into one assurance matrix. Keep audits as dated evidence, not a normative artifact named `FINAL_AUDIT`.
- Merge ART-08/08b/08c and ART-09 into one generated runtime transition specification.
- Delete repeated gate-status blocks from README, ART-15, ART-21, ART-25, and `IMPLEMENTATION_BLOCK`; render them from one signed ControlState.
- Delete the weighted scheduler constants and twelve critic personas from the security architecture. Treat them as policy/configuration. Retain trust domains and separation constraints.
- Delete the home-grown unanchored Merkle recipe; replace it with a standard externally anchored transparency-log construction.
- Delete caller-supplied `*_ok` and `eio_pass` fields as authoritative inputs; derive them.
- Delete the ART-04b “non-deletion rule.” Artifact count is not an invariant, and it actively protects duplication.

## Blockers

1. Define the sole authenticated commit/reducer authority.
2. Introduce bootstrap-safe ControlState for human gates, phase, role bindings, and stop epochs.
3. Make hard stop and release linearizable.
4. Replace promotion booleans with derived, evidence-bound predicates.
5. Anchor checkpoint freshness outside the restored state.
6. Make demotion waves authoritative, complete, and restartable.
7. Add principal/model/role provenance and independent appointment.
8. Make quarantine decisions immutable and promotion-bound.
9. Repair human decision semantics and missing gate IDs.
10. Supersede R20, reset C12 to zero, and perform a manifest-bound full audit.

## Maturity

**3/10.** The package has unusually broad conceptual coverage and good fail-closed intent, but its safety kernel is still prose and self-reported predicates.

## Readiness

- **`DESIGN_FINAL` approval readiness:** **FAIL**
- **`IMPLEMENTATION_START`:** **BLOCKED / NOT READY**
- **`RESEARCH_EXECUTION_START`:** **BLOCKED / NOT READY**
- **Current audit posture:** `AUDIT-0.3-R20` should be **superseded**
- **C12:** reset to **0**
- **Overall readiness:** architecture revision only; not implementation-ready.
