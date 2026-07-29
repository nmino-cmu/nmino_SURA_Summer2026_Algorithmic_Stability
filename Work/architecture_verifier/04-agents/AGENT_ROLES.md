# 04 — Agent Role Specification

**Artifact ID:** `ART-04`  
**Version:** `ARCH-0.3`  
**Normative status:** `ACTIVE_PARTIAL` · roster labels here; authenticity → ART-04c

> **INCOMPATIBILITY WARNING (Iter4):** Role **names** alone do not authenticate. Use ART-04c Principal + RoleBinding + IndependenceDomain. “Certifier ≠ Proposer” = I-IND-01 / I-RB-02, not distinct string IDs.

## Purpose
Define design-time and research-time roles, write authority, and anti-collusion constraints.

## IO
**In:** phase (design/research), OPERABLE_MINIMAL expansion requests. **Out:** role roster, `roles_invoked[]` ceiling binding via `I.RoleCeiling`.

## Authority
Human sets roster via charter/`DESIGN_FINAL`. Grok assigns instances within ART-04d ceiling. Full-System Auditor never drafts. No role self-authorizes promotion.

## Failure modes
Sole proposer/prover/auditor; role-name theater without distinct instances; folding Frontier Scheduler into Orchestrator; critics writing ResearchState.

## Audit rules
Promotion/`S02` lock: `I.RoleCeiling` PASS; Certifier ≠ Proposer on major claims (ART-13); EIO may veto missing role separation evidence.

## Human gates
Roster expansion beyond ART-04d day-1 → human ack; `OVERRIDE_EIO` if EIO veto overridden.

## Design-time roles

| Role | Model | Writes canonical? | Duty |
|------|-------|-------------------|------|
| Design Orchestrator | Grok (newest) | Proposals only | Owns DesignState proposals, reconciles critiques, prevents scope drift |
| Research-Scope Critic | Composer 2.5 | No | Scope creep / quarantine |
| Mathematical-Rigor Critic | Composer 2.5 | No | FSM / proof gaps |
| Autonomous-Agent Architecture Critic | Composer 2.5 | No | Hierarchy / collusion |
| Verification and Lean Critic | Composer 2.5 | No | Lean theater |
| Safety and Epistemic Critic | Composer 2.5 | No | Fabrication / laundering |
| State and Memory Critic | Composer 2.5 | No | Authority / pins |
| Research-Workflow Critic | Composer 2.5 | No | Question selection |
| Integration and Composition Critic | Composer 2.5 | No | Chain compatibility |
| Failure-Mode and Adversarial Critic | Composer 2.5 | No | Attack coverage |
| System Simplicity Critic | Composer 2.5 | No | Overbuild |
| Novelty and Literature Critic | Composer 2.5 | No | Rediscovery / novelty theater |
| Full-System Auditor | Composer 2.5 | No | Audits complete packages only; never drafts |

## Research-time roles (post-`DESIGN_FINAL`) — dual system (DUAL.2)

> Discovery roles invent and pack CRPs. Verification roles Commit, attack, audit, certify, promote/demote. Frontier never locks B cycles.

### System A — Research Discovery Assistant

| Role | Duty |
|------|------|
| Discovery Orchestrator | A-local sessions; assemble CRP (ART-04e) |
| Mechanism Designer | ART-A-MECH — \(Q_\psi\) proposals into CRP |
| Automatic Theorem Proposal | ART-A-ATP — theorem/lemma candidates into CRP |
| Conjecture Proposer | ART-A-CONJ — conjectures / falsifiers into CRP |
| Novelty Engine | ART-A-NOV — literature/novelty packaging |
| Frontier Scheduler | A question selection only — **never** B `LOCK_CYCLE` |
| Literature Analyst (discovery) | Prior-art packets for CRP |

### System B — Verification Architecture

| Role | Duty |
|------|------|
| Verification Orchestrator | CRP intake; optional cycle bind; APPLY / demotion orchestration |
| Proof Proposer | Constructive attempts on live claims |
| Proof Certifier | Independent review; ≠ proposer |
| Counterexample Attacker | ART-12 / ART-12-CHAR |
| Integration Auditor | ART-11b / ART-11b-CHAR |
| Epistemic Integrity Officer | Veto promotions; provenance |
| Lean Verifier (read-only) | Manifest rebuild |
| Human Gate Operator | Gates; human CRP submit |
| Research Scope (conditional) | Quarantine challenge on B cycles |

Authority for ResearchState writes: ART-04c + ART-06b only. Discovery has **no** Commit authority except via CRP submit through B Committer.

## Triggered critic policy

- Per design/research round: **5–7** critics, not always 12
- Always include ≥1 of {Scope, Epistemic, Integration} when chain-facing
- Distrust unanimous Composer consensus on CRITICAL math without diverse evidence channel (cx / Lean negation / literature disconfirm)

## Delegation limits

- Max depth 2 (orchestrator → specialist → optional sub-tool)
- No specialist may spawn another “orchestrator”
- Critics never edit canonical design/research state

## Anti-collusion

- Critics receive bounded role + requirements; not asked to rubber-stamp draft
- Full-System Auditor receives completed package only
- Same agent ID cannot be sole proposer, prover, and auditor of a major result
