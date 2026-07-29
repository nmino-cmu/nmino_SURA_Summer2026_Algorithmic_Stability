# 10 — Counterexamples & demotion

**Normative:** `ART-16b` demotion waves · CX objects in ART-07b · protocol labels in ART-12 (migrating)

## Plain English

A **FULL** counterexample supersedes hit claims in the **same Commit**, breaks proof floors for seeds and queued dependents, and opens a durable demotion wave so crashes can resume.

---

## FULL CX mint

```mermaid
sequenceDiagram
  participant O as Orchestrator/Attacker
  participant C as Commit
  participant S as ResearchState

  O->>C: RECORD_COUNTEREXAMPLE FULL
  C->>S: upsert Counterexample
  C->>S: SUPERSEDE seeds
  C->>S: DemotionFloorBreak seeds∪dependents
  C->>S: DemotionWave cursor=0
  C->>S: IrreversibleReceipt FULL_CX
```

---

## Wave advance

```mermaid
stateDiagram-v2
  [*] --> Open: mint / START
  Open --> Open: ADVANCE_DEMOTION_WAVE<br/>OPEN_CLAIM next item
  Open --> Complete: cursor = len(work_items)
  Complete --> [*]
```

Incomplete wave ⇒ `DEMOTION_WAVE_OPEN` on non-noop APPLY.

---

## Floor break (no cert replay)

```mermaid
flowchart TD
  Break["DemotionFloorBreak"] --> Unp["Floor UNPROVED"]
  Unp --> Clear{"Wave unlist<br/>+ NEW ATTACH after break?"}
  Clear -->|replay old cert| Fail["FLOOR_BREAK_REPLAY"]
  Clear -->|new cert| Ok["May restore CERTIFIED"]
```

---

## Closure growth

```mermaid
flowchart LR
  CX["Live FULL CX"] --> Hit["I-CX-01 hits"]
  Rel["RENAMES / EQUIVALENT_TO<br/>or fingerprint collision"] --> Hit
  Hit --> Expand["I-DW-33 CX_EXPAND wave"]
```
