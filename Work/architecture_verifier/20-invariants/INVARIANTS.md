# 20 — Security and Integrity Invariants

**Artifact ID:** `ART-20`  
**Version:** `ARCH-0.3`  
**Responsible iteration residual:** 14 (full rewrite); promo rows → ART-13b now

> **INCOMPATIBILITY WARNING:** Rows that cite ART-11 Q11 / legacy bridge registry / Q5 are **non-authoritative for cert/bridge enforcement**. Use ART-07c `I.BridgeApplicabilityEvaluate` + endpoint match. ART-11 PASS cannot authorize promotion.

## Purpose
Map hard integrity rules to detectors/blockers; EIO standing veto.

## IO
**In:** promotion / synthesis / restore attempts. **Out:** allow/block + interface calls (`I.*`).

## Authority
EIO standing veto on provenance/pin/gate honesty. Interfaces in ART-24 bind runtime checks.

## Failure modes
Missing detector for a numbered rule; theater interfaces; promoting past EIO veto.

## Audit rules
Rules table below must have enforcement path; Full-System Auditor checks coverage vs charter hard rules.

## Human gates
`OVERRIDE_EIO`; `HARD_STOP`; `DESIGN_FINAL` (does not lift these rules).

## Hard rules → detectors/blockers

| # | Rule | Enforcement |
|---|------|-------------|
| 1 | No fabricated proof/citation/Lean/novelty | EIO + ground-truth channels; fail-closed |
| 2 | No sensitivity→inference without bridge | **ART-07c** inference bridge + covering anchor; ART-11 Q11 legacy only |
| 3 | No silent definition change | Pin system + invalid mid-cycle edit |
| 3b | No mid-cycle quarantine hop edit | `quarantine.frozen_at_s02` (set on `I.Frontier` S02 write) + ART-08 invalid transition |
| 3c | No post-gate card hop-swap | Card freeze (ART-08) + ART-06b Commit-derived hop check (legacy `hop_chain_ok` caller boolean forbidden) + ART-11 Q16 non-authoritative for promotion |
| 4 | Data-dep noise = sub-mechanism | Mechanism schema field |
| 5 | Heterogeneous/correlated normalization | CX.hetero_norm in applicable set (ART-12) → must be in `mandatory_attack_classes[]` |
| 6 | Support-change / zero-prob | CX classes + audit |
| 7 | Index ≠ policy without proof | object_stabilized field + CX.index_vs_policy |
| 8 | Post-processing only if cert allows | **ART-07c** endpoint/exclusions; Q5 legacy only |
| 9 | Composition via registered rules | Q6–Q7 |
| 10 | No PROVED with essential conjecture deps | DAG closure check |
| 11 | No Lean verified with sorry/admit/target axiom | Manifest predicate |
| 12 | Never discard failures | Append-only + archive |
| 13 | No autonomous novelty confirm | ART-14 + human gate |
| 14 | No silent scope expand | Quarantine + SCOPE_CHANGE |
| 15 | Info value > volume | Question policy + stagnation |
| 16 | No sole proposer/prover/auditor | ART-13 |
| 17 | Milestone needs integration PASS | ART-11 |
| 18 | Path failure ≠ terminate program | Frontier continues |
| 19 | No design convergence from agreement alone | ≥2 adversarial rounds; `material_new` non-orchestrator |
| 20 | Human interruptibility | **ART-06b** ControlState `HardStopRecord` + `I.Commit` HARD_STOP_*; release decision digest (auth Iter4) |
| 21 | OPERABLE_MINIMAL role ceiling | `I.RoleCeiling` derived inside `I.Commit` |
| 22 | Speculative prose control | `I.BullshitLinter` on synthesis |
| 23 | Checkpoint integrity | `I.CheckpointValidate` (trust anchor Iter10) |
| 24 | No write outside mutation boundary | **ART-06b** `I-MUT-01` |
| 25 | No caller-trusted commit booleans | **ART-06b** `I-BOOL-01` |

## Integrity officer standing veto

EIO may block any promotion lacking provenance, pin match, or gate trigger honesty.
