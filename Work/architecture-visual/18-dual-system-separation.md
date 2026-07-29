# 18 — Dual-system separation (visual)

Companion to [`../architecture/00-repair/DUAL_SYSTEM_SEPARATION_PLAN.md`](../architecture/00-repair/DUAL_SYSTEM_SEPARATION_PLAN.md).

## Two systems

```mermaid
flowchart LR
  A["System A<br/>Discovery Assistant<br/>speculate · invent · pack"] -->|"CandidateResearchPackage"| B["System B<br/>Verification Architecture<br/>validate · attack · certify"]
  H["Human"] -->|"CandidateResearchPackage"| B
  B -->|"certified digests<br/>read-only"| A
```

## What moves where

```mermaid
flowchart TB
  subgraph StayB["STAY IN VERIFIER"]
    Commit["I.Commit"]
    Obj["Claims / deps / certs"]
    CX["CX + demotion"]
    Lean["Lean"]
    Audit["Audit + provenance"]
    Promo["Promotion"]
  end

  subgraph MoveA["MOVE TO DISCOVERY ASSISTANT"]
    Q["Question selection"]
    F["Frontier scoring"]
    M["Mechanism designer"]
    N["Novelty engine"]
    O["Discovery orchestrator"]
    Cyc["Autonomous idea cycle"]
  end

  subgraph Bridge["SHARED"]
    CRP["CandidateResearchPackage"]
    Scope["Area-1 scope pins"]
    Gates["Human gate IDs"]
  end

  MoveA --> CRP
  CRP --> StayB
```

## Intake pipeline

```mermaid
flowchart TD
  CRP --> Schema --> Canon --> Typed --> Deps --> Obl --> CX --> Audit --> Promo --> Lib["Certified library"]
```

## Phase A vs Phase B packages

```mermaid
flowchart LR
  subgraph PhaseA["Phase A — characterization"]
    A1["Instability theorems"]
    A2["Structural lemmas"]
    A3["Proof obligations"]
  end
  subgraph PhaseB["Phase B — stabilization"]
    B1["MechanismInstance"]
    B2["Stability / utility certs"]
  end
  PhaseA --> CRP["CRP profile"]
  PhaseB --> CRP
```

Mechanism is **optional** on Phase A.

## Ownership after M4

- Discovery FSM / frontier / cards → `../architecture-discovery/`
- Verification Commit / cycle bind / CRP intake → `../architecture/`
- Visuals remain explanatory only
