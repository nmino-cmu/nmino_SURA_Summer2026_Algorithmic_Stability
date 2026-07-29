# 02 — System context

**Normative / narrative:** `architecture/03-context/SYSTEM_CONTEXT.md` · info-flow: `architecture/ARCHITECTURE_INFORMATION_FLOW.md`

## Plain English

Two worlds: **design** (how the architecture is written) and **research** (claims inside the machine). Both talk to humans and external literature, but research cannot silently write itself.

---

## Context diagram

```mermaid
flowchart TB
  Lit["Literature / imports"] -->|quarantine until provenance| Res["Research store"]
  Hum["Humans"] -->|gates / hard-stop| Ctrl["Control"]
  Crit["Critics / auditors"] -->|design critiques| Des["Design store"]
  Agents["Runtime agents"] -->|Commands| Commit["I.Commit"]
  Commit --> Ctrl & Res & Des
  Res --> Out["Derived views<br/>frontier, floors, audits"]
```

---

## Information flow (simplified)

```mermaid
sequenceDiagram
  participant A as Agent
  participant C as Commit
  participant R as ResearchState
  participant V as Derived validators

  A->>C: typed Command
  C->>V: DeriveEffects + ValidationPreimage
  V-->>C: ok / reason_code
  C->>R: accept or reject
```
