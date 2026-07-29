# 11 — Promotion

**Normative:** `ART-13b` `PROMOTION_INTENT.md`

## Plain English

Raising research maturity is a **proof-carrying Commit**. The intent is content-addressed; every `*_ok` in the validation preimage is recomputed — never trusted from the caller.

---

## APPLY flow

```mermaid
flowchart TD
  PI["PromotionIntent<br/>target, policy, basis_digests"] --> CMD["APPLY_PROMOTION"]
  CMD --> VP["ValidationPreimageAPPLY.v7"]
  VP --> F1["floor ≥ policy"]
  VP --> F2["RequiredGates HD"]
  VP --> F3["EIO assessment / veto"]
  VP --> F4["audit_ok / cycle_ok"]
  VP --> F5["dd_ok / psi_ok / model_prov_ok"]
  VP --> F6["roles_invoked_ok"]
  VP --> F7["CX + demotion fences"]
  F1 & F2 & F3 & F4 & F5 & F6 & F7 --> Write["One maturity upsert"]
```

---

## Basis = evidence refs

```mermaid
flowchart LR
  Basis["basis_digests[]"] --> Ev["I-EV-01 provenance"]
  Ev -->|bad ref| Fail["EVIDENCE_PROV_FAIL"]
  Ev -->|ok| Use["Counts toward policy kinds"]
```

---

## Forbidden shortcuts

```mermaid
flowchart TB
  Bad["payload.audit_ok = true<br/>payload.basis_ok = true<br/>…"] --> Rej["CALLER_BOOLEAN_FORBIDDEN"]
```
