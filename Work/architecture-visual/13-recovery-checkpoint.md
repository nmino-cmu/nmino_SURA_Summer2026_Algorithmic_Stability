# 13 — Failure recovery & checkpoint

**Normative:** `ART-16b` demotion · `ART-17b` checkpoint/restore  
**Appendix:** ART-16 / ART-17 prose

## Plain English

Demotion is crash-resumable. Restore cannot accept a fake short history that drops irreversible events. Hard-stop after restore still comes from ControlState.

---

## Checkpoint create / validate

```mermaid
flowchart TD
  Tip["Committed tip"] --> Create["I.CheckpointCreate"]
  Create --> CP["CheckpointRecord<br/>merkle + IR head at create"]
  CP --> Val["I.CheckpointValidate"]
  Val --> M["merkle ok"]
  Val --> IR["prefix covers irreversible_head<br/>+ receipt digests match"]
  Val --> HS["hard_stop snapshot check"]
  M & IR & HS --> Pass["PASS or S15"]
```

---

## Mid-wave crash resume

```mermaid
sequenceDiagram
  participant Sys as System
  participant CP as Checkpoint
  participant Log as EventLog+IR
  participant W as DemotionWave

  Note over W: crash mid ADVANCE
  Sys->>CP: last CP
  Sys->>Log: forward-fix to irreversible head
  Sys->>Sys: I.CheckpointValidate PASS
  Sys->>W: continue ADVANCE
  Note over W: APPLY still fenced until COMPLETE
```

---

## Truncation attack blocked

```mermaid
flowchart LR
  Attacker["Self-presented prefix<br/>missing FULL CX"] --> V["Validate"]
  Anchor["IrreversibleSafetyLog head"] --> V
  V --> Fail["IRREVERSIBLE_PREFIX"]
```
