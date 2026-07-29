# 08 — Lean & theorem status

**Normative:** `ART-10b` Lean binding · maturity via `ART-13b`  
**Appendix:** ART-09 / ART-10 FSM sketches

## Plain English

Lean status is **computed** from a claim-bound manifest + toolchain — never a free label. Lean evidence is INFORMAL-grade for floor purposes; RESULT still needs CERTIFIED.

---

## Lean status (derived)

```mermaid
flowchart TD
  M["LeanManifest<br/>claim + transcript"] --> S["DerivedLeanStatus"]
  T["LeanToolchainHead"] --> S
  S --> Full["LEAN_FULL / CORE"]
  S --> Stale["LEAN_STALE / gap"]
  Full --> Floor["DerivedProofFloor → INFORMAL<br/>via LEAN_REF"]
  Stale --> Gap["I-DW-32 LEAN_GAP demotion wave"]
```

---

## Status axes (two dials)

```mermaid
flowchart LR
  subgraph Maturity["Research maturity"]
    O[OPEN] --> Cj[CONJECTURE]
    Cj --> PR[PARTIAL_RESULT]
    PR --> R[RESULT]
    R --> Sup[SUPERSEDED]
  end
  subgraph Floor["Proof floor"]
    U[UNPROVED] --> I[INFORMAL]
    I --> C[CERTIFIED_INFORMAL]
  end
  R -.->|"requires"| C
```

---

## Commands

```mermaid
sequenceDiagram
  participant O as Orchestrator
  participant L as Lean Verifier
  participant C as Commit

  O->>C: SET_LEAN_TOOLCHAIN
  L->>C: RECORD_LEAN_MANIFEST
  C->>C: maybe mint LEAN_GAP wave
```
