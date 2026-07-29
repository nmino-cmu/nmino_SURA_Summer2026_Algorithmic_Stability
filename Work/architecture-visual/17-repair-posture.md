# 17 — Repair posture & gates

**Control plane:** `architecture/00-repair/` · `ART-25` · `IMPLEMENTATION_BLOCK.md` · Sol evidence under `adversarial_review_artifacts/`

## Plain English

The package finished Iter1–14 repair and a **Sol package gate PASS**. That does **not** lift implementation. You still own `DESIGN_FINAL`.

---

## Current status

```mermaid
flowchart TD
  I["Iter1–14 FREEZE_OK"] --> S["Sol PACKAGE_GATE PASS"]
  S --> Seal["Seal ReleaseManifest"]
  Seal --> You{"DESIGN_FINAL?"}
  You -->|approve| Plan["Planning allowed"]
  You -->|no| Stay["NON-RELEASE"]
  Plan --> Imp["IMPLEMENTATION_START"]
  Imp --> Res["RESEARCH_EXECUTION_START"]
```

---

## Blocker ledger shape

```mermaid
flowchart LR
  Closed["Most B-* CLOSED"] --> Partial["PARTIAL leftovers<br/>B-OBJ-DUAL appendix<br/>B-BRIDGE-PROOF residual"]
  Closed --> Human["Human: DESIGN_FINAL"]
```

---

## Where to look

| Need | Path |
|------|------|
| Status pins | `architecture/25-audit-reports/FINAL_AUDIT.md` |
| Blockers | `architecture/00-repair/BLOCKER_LEDGER.md` |
| Sol PASS note | `architecture/adversarial_review_artifacts/REPAIR_PACKAGE_SOL_GATE_PASS_2026-07-24.md` |
| Visual overview | [00-GENERAL.md](00-GENERAL.md) |
