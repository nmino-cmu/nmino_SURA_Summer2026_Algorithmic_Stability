# 16 — Conformance & release identity

**Normative:** `ART-21b` conformance · `ART-25b` release identity  
**Historical:** ART-21 T-suite (do not cite as clearance)

## Plain English

Digests are SHA-256 over canonical JSON. Fixtures lock golden digests. A **ReleaseManifest** is the only thing a future `DESIGN_FINAL` may point at.

---

## Conformance

```mermaid
flowchart TD
  Canon["ART21b.CANON.v1"] --> H["SHA-256"]
  H --> GV["GV-* golden vectors"]
  CF["CF-* expect catalog"] --> Run["I.ConformanceRun"]
  GV --> Run
  Run --> Pass["CONFORMANCE_CATALOG_PASS<br/>≠ DESIGN_FINAL"]
```

---

## Release seal

```mermaid
flowchart TD
  Files["ACTIVE_NORMATIVE file set<br/>+ fixtures"] --> Man["ReleaseManifest"]
  Man --> RD["release_digest"]
  RD --> DF["DESIGN_FINAL target_digest"]
  Hist["R20 / old T-suite PASS"] -.->|forbidden| DF
```

---

## False-pass ban

```mermaid
flowchart LR
  Bad["Cite historical PASS<br/>as readiness"] --> Code["FALSE_PASS_CITATION"]
```
