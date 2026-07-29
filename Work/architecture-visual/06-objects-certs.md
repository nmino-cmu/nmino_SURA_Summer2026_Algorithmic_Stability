# 06 — Objects, certificates, bridges

**Normative:** `ART-07b` canonical objects · `ART-07c` typed certs/bridges · digests: `ART-21b`

## Plain English

Everything important is a **digest**. Claims carry pins, assumptions, domains. Certificates and bridges are typed Claims — not free labels.

---

## Object map (core)

```mermaid
flowchart TB
  Def["DefinitionVersion"] --> Pin["DefPin"]
  Claim["Claim"] --> Pin
  Claim --> Asm["Assumption / Discharge"]
  Claim --> Mech["MechanismInstance"]
  Claim --> Rel["ClaimRelation<br/>RENAMES / EQUIVALENT_TO / …"]
  Claim --> Floor["DerivedProofFloor"]
  PE["ProofEvidence"] --> Floor
  CR["CertificationRecord"] --> Floor
  CX["Counterexample"] --> Claim
```

---

## Proof floor ladder

```mermaid
flowchart LR
  U["UNPROVED"] --> I["INFORMAL"]
  I --> C["CERTIFIED_INFORMAL"]
```

Lean (`LEAN_REF`) can yield INFORMAL when FULL/CORE — it cannot launder into CERTIFIED without real certify.

---

## Bridge use

```mermaid
flowchart LR
  Src["Source cert / claim"] --> BR["Bridge Claim<br/>+ transforms"]
  BR --> Eval["BridgeApplicabilityEvaluate"]
  Eval -->|APPLICABLE| Use["Inference / transfer consumer"]
  Eval -->|not| Block["APPLICABILITY_NOT_APPLICABLE"]
```

---

## Hashing

```mermaid
flowchart TD
  Fields["Normative fields"] --> Canon["ART21b.CANON.v1<br/>sorted JSON"]
  Canon --> H["SHA-256"]
  H --> Dig["object_digest"]
```
