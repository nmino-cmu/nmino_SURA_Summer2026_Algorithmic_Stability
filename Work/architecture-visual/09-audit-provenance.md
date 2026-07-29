# 09 — Audit & provenance

**Normative:** `ART-11b` audit binding · `ART-11c` provenance binding

## Plain English

Major promotions need an **intent-bound audit** with fixed questions. Data-independence needs a **VERIFIED** DD record. Model swaps invalidate old credited acts.

---

## Audit bind

```mermaid
flowchart TD
  PI["PromotionIntent"] --> AR["AuditRecord<br/>answers Q01–Q17 set"]
  AR --> Bind["I-BIND-01"]
  Bind --> Fresh["Fresh vs state head"]
  Bind --> Ind["Auditor independence"]
  Bind --> CX["Live CX ∩ evidence"]
  Bind -->|fail| Codes["AUDIT_* reason codes"]
```

Q04 is not attestation-alone — it follows ART-11c (`I-Q04-01`).

---

## DD verification

```mermaid
flowchart LR
  DD["DataDependenceRecord<br/>reads[]"] --> Reg["REGISTER_DD_VERIFICATION"]
  Reg --> V["DdVerificationRecord VERIFIED"]
  V --> Core["I-DDV-11 core match"]
  Core --> Apply["dd_ok on APPLY"]
```

FIXED ⇒ empty reads; hidden declared reads ⇒ `DD_HIDDEN_READ`.

---

## Model provenance

```mermaid
flowchart TD
  MP["ModelProvenanceRecord"] --> Bind["RoleBinding.model_prov"]
  Bind --> Act["Credited act pins prov"]
  MP -->|replace/revoke| Inv["ModelProvInvalidation"]
  Inv --> Stale["MODEL_PROV_STALE on APPLY"]
```

---

## ψ / DATA_DEP_PSI

```mermaid
flowchart TD
  Snap["Mechanism/domain snapshot"] --> Req["requires_DATA_DEP_PSI?"]
  Req -->|yes| Need["HD DATA_DEP_PSI<br/>+ CalibrationSubmechanismCert<br/>+ DD if claims FIXED"]
  Need --> PsiOk["psi_ok"]
```
