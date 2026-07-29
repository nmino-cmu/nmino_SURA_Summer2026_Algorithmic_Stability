# 15 — Invariants & interfaces

**Partial:** `ART-20` invariants · `ART-20b` convergence · `ART-24` interfaces · `ART-23` limitations

## Plain English

Hard invariants are the “never break these” list. Interfaces name the public entrypoints (`I.Commit`, `I.CheckpointValidate`, …). Convergence credit is **reset** for repair — do not cite old C12=2.

---

## Core invariants (mental model)

```mermaid
flowchart TB
  I1["Single mutation boundary"]
  I2["No caller booleans"]
  I3["Floor couples to RESULT"]
  I4["CX archive ≠ ignore"]
  I5["Hard-stop is ControlState"]
  I6["Release needs release_digest"]
  I1 & I2 & I3 & I4 & I5 & I6 --> Safe["Fail closed"]
```

---

## Interface map

```mermaid
flowchart LR
  subgraph Writes
    IC["I.Commit"]
  end
  subgraph Reads_pure
    IV["I.CheckpointValidate"]
    IR["I.RoleCeiling"]
    II["I.IndependenceCheck"]
    ICf["I.ConformanceRun"]
  end
  IC --> Stores["Stores"]
  IV --> Stores
```

---

## Limitations posture

```mermaid
flowchart TD
  Known["Known ceilings<br/>ponytail comments"] --> Upgrade["Upgrade path named"]
  Residual["Residual dual dialect<br/>in appendix prose"] --> Seal["ACTIVE paths digest-native"]
```
