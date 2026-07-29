# 07 — Research cycle (visual)

Companion to ART-08d (B) and `architecture-discovery/` ART-08 (A).

## Dual path

```mermaid
flowchart LR
  A["System A discovery cycle"] -->|CRP| Intake["SUBMIT_CANDIDATE_PACKAGE"]
  H["Human"] -->|CRP| Intake
  Intake --> ClaimPath["Claim-direct verification<br/>CX · audit · APPLY"]
  Intake -.->|optional| Lock["LOCK_CYCLE<br/>VERIFICATION_ORCHESTRATOR only"]
  Lock --> CycleCmds["ART-08d cycle cmds"]
```

## Who locks B cycles

```mermaid
flowchart LR
  VO["VERIFICATION_ORCHESTRATOR"] -->|LOCK_CYCLE optional| Cycle
  FS["FRONTIER_SCHEDULER"] -.->|forbidden| Cycle
```

Frontier selects questions **only inside System A**. It never locks or controls verifier cycles.
