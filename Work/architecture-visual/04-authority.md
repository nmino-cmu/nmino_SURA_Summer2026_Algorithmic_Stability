# 04 — Authority & escalation

**Normative / partial:** `architecture/05-authority/AUTHORITY_MATRIX.md`

## Plain English

Who can overrule whom. EIO can veto dishonest provenance/pin/gate claims. Humans sit above agents. Critics do not write research state.

---

## Escalation ladder

```mermaid
flowchart TB
  Agent["Agent act"] --> Orch["Orchestrator reconcile"]
  Orch --> EIO["EIO veto?"]
  EIO -->|veto| Hold["Blocked until OVERRIDE_EIO"]
  EIO -->|allow| Commit["I.Commit"]
  Commit --> Human["Human gates when required"]
  Human -->|HARD_STOP| Freeze["ControlState.hard_stop"]
```

---

## Independence (certify)

```mermaid
flowchart LR
  Prop["Proposer atom"] --- Ind["Independence check"]
  Cert["Certifier atom"] --- Ind
  Ind -->|disjoint| OK["May CERTIFY"]
  Ind -->|overlap| NO["Reject"]
```
