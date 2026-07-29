# Formal verification report

- operator: `heap-extract-max`
- theorem_id: `heap-extract-max-margin`
- candidate_digest: `4b72e8a65a1cf091fec01cfd678d4c89cf3a101683f665958b106d2ce129441e`
- bundle_digest: `7a1fe2157dbeaad09575a9ad29628df11b60e391171ba3476b6bbcd6fcd545a3`
- crp_digest: `a42bd5403a15bf40cf15dd012e28af3a131238bcbd61b3de4204c052a4e75fb5`
- verification_run_id: `c1e4d615-f920-4fad-829e-d3b4be82b446`

## Authority boundaries

- Statement authority: handwritten `*Prop` definitions between STATEMENT markers.
- Proof authority: Lean kernel (`lake build` + `#print axioms`), not this report.
- Manifest store: ART-10b filesystem surrogate (`LEAN_MANIFEST_WITHOUT_COMMIT`).
- Domain: Mathlib `ℝ` (`REAL_MATHLIB`).
- LLM proof generation: not enabled in v1.

## System 2 statement

Let m>=2 and let scores be constructed by (heap key scores with unique maximizer). If i* is the unique maximizer with margin gamma>2*epsilon and ||delta||_inf<=epsilon, then i* remains the unique maximizer after perturbation (Heap extract-max reduces to Argmax margin).

## Lean propositions

- `heap_extract_max_margin_invariance` : `Research.Operators.HeapExtractMax.Margin.HeapExtractMaxMarginInvarianceProp`
- `heap_extract_max_margin_sharpness` : `Research.Operators.HeapExtractMax.Margin.HeapExtractMaxMarginSharpnessProp`

## Conclusion tokens

```json
{
  "schema_id": "ARTLEAN.CONCL.heap_extract_max_margin.v1"
}
```

- conclusion_digest: `6eef0a825f1e16c973ce2ac5372d0c1f6b86c3340f4ad32909b2c9bf9bec0343`
- semantic_freeze_digest: `4f1002b602aec066ae557eb251bc10dd1feeed9cb3d3cb95bc9ac7ed59dd9ece`
- semantic_audit: `YES`

## Conventions

```json
{
  "equality": "DEFAULT",
  "extensionality": "DEFAULT",
  "finiteness": "FINITE_VECTOR",
  "measure_stage": "NONE",
  "score_encoding": "REAL_MATHLIB",
  "tie_break": "UNIQUE_REQUIRED"
}
```

## Build

- build_ok: `True`
- sorry_count: `0`
- admit_count: `0`
- lake_log_digest: `87a6ac2ad9231249eb100f5f4d8fba064c72d8c0db7eea0f4f30060be98c0d1a`
- axiom_closure_captured: `True`

## Axiom closure (`#print axioms`)

- `Classical.choice`
- `Quot.sound`
- `propext`

## Derived status (recomputed; not authoritative storage)

- `LEAN_FULL`

## Known gaps

- `DEFINITION_PINS_SURROGATE`

## Limitations of this certificate

- `LEAN_FULL` here means kernel-checked Mathlib `ℝ` propositions.
- Smoke theorems alone never authorize operator LEAN_FULL.
- PDF / markdown reports are derived views, not proof authority.

## Reuse

- `Research.Operators.Argmax.Basic` / `Margin` shared by argmax-family aliases.
