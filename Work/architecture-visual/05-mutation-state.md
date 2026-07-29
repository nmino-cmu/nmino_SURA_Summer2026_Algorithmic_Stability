# 05 — Mutation & authoritative state

**Normative:** `ART-06b` `MUTATION_AND_AUTHORITATIVE_STATE.md`

## Plain English

Nothing important is true because an agent said so. The only mutator is **`I.Commit`**. Four stores move together in one atomic accept.

---

## Stores

```mermaid
flowchart TB
  CMD["Command"] --> COMMIT["I.Commit"]
  COMMIT --> CTRL["ControlState<br/>hard_stop, role ceiling"]
  COMMIT --> RES["ResearchState<br/>claims, audits, CX…"]
  COMMIT --> DES["DesignState"]
  COMMIT --> IR["IrreversibleSafetyLog"]
  COMMIT --> LOG["EventLog / MutationEvent"]
```

---

## Commit pipeline

```mermaid
flowchart TD
  A["1. Head match<br/>else STALE_WRITE"] --> B["2. Auth + RoleCeiling"]
  B --> C["3. Hard-stop fence"]
  C --> D["4. Ban caller *_ok"]
  D --> E["5. DeriveEffects"]
  E --> F["6. Reduce tentative"]
  F -->|fail| R["REJECT — nothing appended"]
  F -->|ok| G["7. Atomic accept:<br/>EventLog + stores + IR receipt"]
```

---

## Hard-stop

```mermaid
stateDiagram-v2
  [*] --> Running
  Running --> Stopped: HARD_STOP_SET
  Stopped --> Running: HARD_STOP_CLEAR<br/>+ HARD_STOP_RELEASE HD
  Stopped --> Stopped: only CONTROL + IRREVERSIBLE<br/>(+ EventLog)
```

While stopped: no research object upserts (provenance writers blocked).

---

## Digest cycle (irreversible)

```mermaid
flowchart LR
  Eff["research_control_design_effects"] --> ED["effects_digest"]
  ED --> Ev["event_digest"]
  Ev --> Rec["IrreversibleReceipt<br/>cites event_digest"]
  Rec -.->|"not hashed into effects_digest"| Eff
```
