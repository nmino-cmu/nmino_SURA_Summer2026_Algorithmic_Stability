# Dual-System Architecture Package — Discovery Assistant + Verification Architecture

> ## NON-RELEASE · IMPLEMENTATION_BLOCK ACTIVE
> **ARCHITECTURE_BLUEPRINT_READY = no** · **IMPLEMENTATION_PLANNING_READY = no** · **RESEARCH_EXECUTION_READY = no** · **DESIGN_FINAL = revoked**  
> Do **not** implement, plan implementation, or run research cycles.  
> Repair control: [00-repair/](00-repair/) · Blockers: [BLOCKER_LEDGER.md](00-repair/BLOCKER_LEDGER.md) · Status index: [ARTIFACT_STATUS.md](00-repair/ARTIFACT_STATUS.md)

**Design version:** `ARCH-0.3-REPAIR` · **NON-RELEASE** · **DUAL.1**  
**Mode:** Architecture **repair** + dual-system separation (design plane)  
**Normative objects:** [ART-07b](07-schemas/CANONICAL_OBJECTS.md) · [ART-07c](07-schemas/TYPED_CERTIFICATES_AND_BRIDGES.md) · [ART-06b](06-state/MUTATION_AND_AUTHORITATIVE_STATE.md) · [ART-CRP](24-interfaces/CANDIDATE_RESEARCH_PACKAGE.md)  
**Dual-system:** [DUAL_SYSTEM_SEPARATION_PLAN.md](00-repair/DUAL_SYSTEM_SEPARATION_PLAN.md) · Discovery home: [`../architecture-discovery/`](../architecture-discovery/)  
**A↔B interface (authoritative):** [`../architecture-integration/00-A-B-INTEGRATION.md`](../architecture-integration/00-A-B-INTEGRATION.md) (ART-INT-00)  
**A↔B information flow (narrative):** [`../architecture-visual/DISCOVERY_VERIFIER_INFORMATION_FLOW.md`](../architecture-visual/DISCOVERY_VERIFIER_INFORMATION_FLOW.md)  
**Package Sol gate:** PASS (evidence under adversarial_review_artifacts); `DESIGN_FINAL` still human  

## Package map

| # | Artifact | Path |
|---|----------|------|
| 1 | Shared Area-1 constitution | [01-charter/CHARTER.md](01-charter/CHARTER.md) |
| 1V | Verification charter (B) | [01-charter/CHARTER_VERIFICATION.md](01-charter/CHARTER_VERIFICATION.md) |
| 1D | Discovery charter (A) | [01-charter/CHARTER_DISCOVERY.md](01-charter/CHARTER_DISCOVERY.md) |
| CRP | Candidate Research Package | [24-interfaces/CANDIDATE_RESEARCH_PACKAGE.md](24-interfaces/CANDIDATE_RESEARCH_PACKAGE.md) |
| 2 | Immutable Mathematical Scope | [02-scope/MATH_SCOPE.md](02-scope/MATH_SCOPE.md) |
| 3 | System Context Diagram | [03-context/SYSTEM_CONTEXT.md](03-context/SYSTEM_CONTEXT.md) |
| 4 | Agent Role Specification | [04-agents/AGENT_ROLES.md](04-agents/AGENT_ROLES.md) |
| 4b | Operable Minimal Profile | [04-agents/OPERABLE_MINIMAL_PROFILE.md](04-agents/OPERABLE_MINIMAL_PROFILE.md) |
| 4d | B operable binding | [04-agents/OPERABLE_BINDING.md](04-agents/OPERABLE_BINDING.md) |
| 4e | A discovery operable | [04-agents/OPERABLE_DISCOVERY.md](04-agents/OPERABLE_DISCOVERY.md) |
| 5 | Authority and Escalation Matrix | [05-authority/AUTHORITY_MATRIX.md](05-authority/AUTHORITY_MATRIX.md) |
| 6 | Canonical State Model (legacy) | [06-state/STATE_MODEL.md](06-state/STATE_MODEL.md) (`QUARANTINED_LEGACY`) |
| 6b | Mutation & authoritative state | [06-state/MUTATION_AND_AUTHORITATIVE_STATE.md](06-state/MUTATION_AND_AUTHORITATIVE_STATE.md) |
| 7 | Research Artifact Schemas | [07-schemas/SCHEMAS.md](07-schemas/SCHEMAS.md) |
| 7b | **Canonical Mathematical Objects (Iter1)** | [07-schemas/CANONICAL_OBJECTS.md](07-schemas/CANONICAL_OBJECTS.md) |
| 7c | **Typed Certificates & Bridges (Iter2)** | [07-schemas/TYPED_CERTIFICATES_AND_BRIDGES.md](07-schemas/TYPED_CERTIFICATES_AND_BRIDGES.md) |
| R | Repair control plane | [00-repair/](00-repair/) |
| 8 | Research-Cycle FSM (stub → discovery) | [08-research-cycle/RESEARCH_CYCLE_FSM.md](08-research-cycle/RESEARCH_CYCLE_FSM.md) |
| 8b | Question-Selection (stub → discovery) | [08-research-cycle/QUESTION_SELECTION.md](08-research-cycle/QUESTION_SELECTION.md) |
| 8c | Experiment Protocol (stub → discovery) | [08-research-cycle/EXPERIMENT_PROTOCOL.md](08-research-cycle/EXPERIMENT_PROTOCOL.md) |
| 8d | Cycle binding (B) | [08-research-cycle/CYCLE_BINDING.md](08-research-cycle/CYCLE_BINDING.md) |
| 9 | Theorem Status State Machine | [09-theorem-status/THEOREM_STATUS_FSM.md](09-theorem-status/THEOREM_STATUS_FSM.md) |
| 10 | Lean Verification State Machine | [10-lean/LEAN_FSM.md](10-lean/LEAN_FSM.md) |
| 11 | Integration Audit Specification | [11-integration-audit/INTEGRATION_AUDIT.md](11-integration-audit/INTEGRATION_AUDIT.md) |
| 12 | Counterexample Protocol | [12-counterexample/COUNTEREXAMPLE_PROTOCOL.md](12-counterexample/COUNTEREXAMPLE_PROTOCOL.md) |
| 13 | Proof Review Protocol | [13-proof-review/PROOF_REVIEW.md](13-proof-review/PROOF_REVIEW.md) |
| 14 | Literature Boundary Protocol | [14-literature/LITERATURE_BOUNDARY.md](14-literature/LITERATURE_BOUNDARY.md) |
| 15 | Human Review Gate Specification | [15-human-gates/HUMAN_GATES.md](15-human-gates/HUMAN_GATES.md) |
| 16 | Failure-Recovery Specification | [16-failure-recovery/FAILURE_RECOVERY.md](16-failure-recovery/FAILURE_RECOVERY.md) |
| 17 | Infinite-Operation / Checkpointing | [17-indefinite-ops/INDEFINITE_OPS.md](17-indefinite-ops/INDEFINITE_OPS.md) |
| 18 | Model Interaction Protocols | [18-model-protocols/MODEL_PROTOCOLS.md](18-model-protocols/MODEL_PROTOCOLS.md) |
| 18b | Bullshit Linter | [18-model-protocols/BULLSHIT_LINTER.md](18-model-protocols/BULLSHIT_LINTER.md) |
| 19 | Memory and Retrieval Spec | [19-memory/MEMORY.md](19-memory/MEMORY.md) |
| 20 | Hard Invariants | [20-invariants/INVARIANTS.md](20-invariants/INVARIANTS.md) |
| 20b | Design Convergence | [20-invariants/DESIGN_CONVERGENCE.md](20-invariants/DESIGN_CONVERGENCE.md) |
| 21 | Architecture Acceptance Tests | [21-acceptance-tests/ACCEPTANCE_TESTS.md](21-acceptance-tests/ACCEPTANCE_TESTS.md) |
| 22 | End-to-End Example Trace | [22-example-trace/E2E_TRACE.md](22-example-trace/E2E_TRACE.md) |
| 23 | Limitations and Residual Risks | [23-limitations/LIMITATIONS.md](23-limitations/LIMITATIONS.md) |
| 24 | Interface Contracts | [24-interfaces/INTERFACE_CONTRACTS.md](24-interfaces/INTERFACE_CONTRACTS.md) |
| 25 | Final Independent Audit Report | [25-audit-reports/FINAL_AUDIT.md](25-audit-reports/FINAL_AUDIT.md) |

## Supporting

| Item | Path |
|------|------|
| Implementation block | [IMPLEMENTATION_BLOCK.md](IMPLEMENTATION_BLOCK.md) |
| Adversarial / audit evidence | [adversarial_review_artifacts/](adversarial_review_artifacts/) |
| **Independent breaker audit (current)** | [adversarial_review_artifacts/INDEPENDENT_BREAKER_AUDIT_2026-07-23.md](adversarial_review_artifacts/INDEPENDENT_BREAKER_AUDIT_2026-07-23.md) — **NOT READY** (maturity 3/10) |
| Prior breaker (pre-Iter1 close) | [adversarial_review_artifacts/INDEPENDENT_BREAKER_AUDIT.md](adversarial_review_artifacts/INDEPENDENT_BREAKER_AUDIT.md) |
| **System B information flow (DUAL.2)** | [ARCHITECTURE_INFORMATION_FLOW.md](ARCHITECTURE_INFORMATION_FLOW.md) |
| Critique archive | [critiques/INDEX.md](critiques/INDEX.md) |
| Adversarial rounds | [critiques/ADVERSARIAL_ROUND.md](critiques/ADVERSARIAL_ROUND.md) |
| Iteration records | [iterations/](iterations/) |

## Reading order (human review)

1. This map → [CHARTER](01-charter/CHARTER.md) → [MATH_SCOPE](02-scope/MATH_SCOPE.md)  
2. [AUTHORITY_MATRIX](05-authority/AUTHORITY_MATRIX.md) → [ART-06b MUTATION](06-state/MUTATION_AND_AUTHORITATIVE_STATE.md) (ART-06 quarantined) → [RESEARCH_CYCLE_FSM](08-research-cycle/RESEARCH_CYCLE_FSM.md)  
3. [FINAL_AUDIT](25-audit-reports/FINAL_AUDIT.md) + [DESIGN_CONVERGENCE](20-invariants/DESIGN_CONVERGENCE.md)  
4. [HUMAN_GATES](15-human-gates/HUMAN_GATES.md) / [IMPLEMENTATION_BLOCK](IMPLEMENTATION_BLOCK.md) before any build decision  

Do **not** approve `DESIGN_FINAL` or lift the block without an explicit human gate decision.
