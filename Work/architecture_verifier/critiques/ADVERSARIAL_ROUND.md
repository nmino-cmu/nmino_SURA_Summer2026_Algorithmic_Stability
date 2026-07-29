# Adversarial False-Convergence Rounds

**Authoritative:** `25-audit-reports/FINAL_AUDIT.md`.  
**Evidence dir:** [../adversarial_review_artifacts/](../adversarial_review_artifacts/)

| Round | Evidence | material_new | Notes |
|-------|----------|--------------|-------|
| ADV-FC-ITER7-..8 | (prior; not in this folder) | mixed | Iter7 hop/quarantine → R17 C12 (later reset) |
| ADV-FC-ITER8-1 | (prior; not in this folder) | false | post-Iter8 polish |
| ADV-FC-ITER9-1 | (prior; not in this folder) | true | P6 soft-freeze → patched |
| ADV-FC-ITER9-2 | [bf868f3f…](../adversarial_review_artifacts/bf868f3f-1478-4bdc-9f7e-b3a06f5e290e.jsonl) | true | H-ADV9-2-01 ART-08 → patched |
| ADV-FC-ITER9-3 | [a11ce32d…](../adversarial_review_artifacts/a11ce32d-1b69-4601-9752-cc69d9beb601.jsonl) | **false** | clean #1 under R20 |
| ADV-FC-ITER9-4 | [7744f780…](../adversarial_review_artifacts/7744f780-9cb3-42b6-ba6d-8f7c83307057.jsonl) | **false** | clean #2 → **C12 = 2** |

R20 PASS evidence: [862084d7…](../adversarial_review_artifacts/862084d7-07ee-4cd1-b29d-b89a6f4955c9.jsonl)

`consecutive_clean_rounds = 2` under `AUDIT-0.3-R20`. C12 ≠ `DESIGN_FINAL`.
