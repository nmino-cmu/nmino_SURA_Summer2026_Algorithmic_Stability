# 01 — Charter & math scope

**Normative:** `architecture/01-charter/CHARTER.md`, `architecture/02-scope/MATH_SCOPE.md`

## Plain English

The charter says *what the system is allowed to care about*. Math scope locks the scientific chain (data → scores → selection → certificates → inference) and default finite Λ.

---

## Scope chain

```mermaid
flowchart LR
  Data["Data / domains"] --> FD["F_D scores"]
  FD --> Qψ["Q_ψ selection"]
  Qψ --> Stab["Stability certificate"]
  Stab --> Comp["Composition"]
  Comp --> Obj["Selected object / policy"]
  Obj --> Inf["Post-hoc inference"]
```

Non-finite Λ needs a `CONTINUOUS_LAMBDA` human gate.

---

## Charter boundaries

```mermaid
flowchart TB
  In["In scope:<br/>theoretical research<br/>claims + evidence"] 
  Out["Out of scope:<br/>product DB choices,<br/>running research before gates"]
  In --> Commit["Everything mutable goes<br/>through I.Commit later"]
  Out --> Block["IMPLEMENTATION_BLOCK"]
```

---

## Major milestone targets

Only these maturity raises count as *major* for audit/cycle binds:

```mermaid
flowchart LR
  C["CONJECTURE"] --> P["PARTIAL_RESULT"]
  P --> R["RESULT"]
```
