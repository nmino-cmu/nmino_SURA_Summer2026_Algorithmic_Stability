# Operable Minimal Profile (Simplicity)

**Artifact ID:** `ART-04b`  
**Version:** `ARCH-0.3`  
**Normative status:** `PENDING_MIGRATION` · descriptive only  
**Response to:** System Simplicity Critic — package is charter-complete (25 artifacts) but day-1 operation uses a reduced control plane.

> **INCOMPATIBILITY WARNING:** Authoritative operable minimal binding = **ART-04d**. This file is appendix/descriptive. Bridge identity = ART-07c; all registry mutations via ART-06b `I.Commit`.

## Purpose
Hard runtime role/registry ceiling for day-1 **verification** operation. Authoritative = ART-04d. Discovery roster = ART-04e.

## IO
**In:** phase + proposed `roles_invoked[]`. **Out:** allow/deny via `I.RoleCeiling`; expansion requires human_dec_id.

## Authority
ART-04d ceiling binds Verification Orchestrator assignments. Discovery engines are not on B day-1. Expansion beyond day-1 roster needs human ack.

## Failure modes
Collapsing Certifier into Proposer; putting Frontier Scheduler on B `LOCK_CYCLE`; opaque literature/bridge registries.

## Audit rules
Every promotion lists `roles_invoked[]` ⊆ B profile (or logged expansion); `I.RoleCeiling` FAIL → block.

## Human gates
Day-1 expansion; any permanent roster change.

## Charter vs operable core

### Day-1 B runtime roles (≤8) — ART-04d

1. Verification Orchestrator  
2. Proof Proposer  
3. Proof Certifier (≠ proposer)  
4. Counterexample Attacker  
5. Integration Auditor  
6. Epistemic Integrity Officer  
7. Human Gate Operator  
8. Committer  

**Not on B day-1:** Frontier Scheduler, Mechanism Designer, Novelty Engine (System A / ART-04e).

**Conditional:** Literature Analyst (B audit of lit-cited CRP); Lean Verifier; Research Scope.

### Day-1 registries

`definitions`, `claims` (theorems+conjectures+bridges), `mechanisms`, `experiments`, `audits`, `counterexamples`, `open_questions/frontier`, `quarantine` (keyed by `q_id`), `human_decisions`, `literature_claims`, `lean_manifests` (when used).

**Forbidden:** collapsing `literature_claims` or `bridges` to opaque views without EIO-readable provenance path.

### Critic subset selection algorithm (design-time)

1. Always include: Scope **or** Epistemic, plus Integration if chain-facing  
2. Add Lean critic if any LEAN_* change  
3. Add Failure-Mode if mechanism or bridge changed  
4. Add Simplicity if artifact count or roles increased  
5. Add Novelty if mechanism family or PLAUSIBLE_NOVELTY involved  
6. Cap at 7; Full-System Auditor only on complete package  

## Non-deletion rule

Do not delete charter-required artifact files to “simplify”; mark appendix and route day-1 ops through this profile.

## Hard runtime contract (ITER5 R-11)

```text
roles_invoked[] ⊆ day1_profile ∪ conditional_roles_with_trigger
each conditional role requires trigger_id + (human_dec_id if expansion beyond profile)
promotion rolls back if roles_invoked violates profile
role_expansion_log append-only
```

Orchestrator may not silently invoke Literature Analyst / Lean Verifier / Mechanism Designer outside triggers.
