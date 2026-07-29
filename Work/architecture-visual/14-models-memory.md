# 14 — Model protocols & memory

**Partial / migrating:** `ART-18` model protocols · `ART-18b` linter · `ART-19` memory

## Plain English

Critics produce reports; orchestrator reconciles. Credit requires act-time principal/binding/model pins (`I-MP-02`). Memory retrieval must not quietly serve SUPERSEDED/REFUTED evidence into promotion.

---

## Critic loop (design-time)

```mermaid
sequenceDiagram
  participant C as Critic
  participant O as Orchestrator
  participant L as Ledger

  C->>O: report (CRITICAL/HIGH/…)
  O->>O: accept / reject / defer each CRITICAL
  O->>L: reconciliation record
```

Unpinned or mismatched author fields ⇒ **not a credited act**.

---

## Memory tiers

```mermaid
flowchart TB
  Q["Query"] --> Tier["Retrieval tiers"]
  Tier --> Live["Live claims / audits"]
  Tier --> Arch["Archive"]
  Tier -.->|default exclude| Bad["SUPERSEDED / REFUTED<br/>NEEDS_REVIEW / quarantine"]
```

Promotion evidence must still pass ART-11c `I-EV-01` on `basis_digests`.
