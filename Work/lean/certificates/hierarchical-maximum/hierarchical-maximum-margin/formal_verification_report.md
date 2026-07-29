# Formal verification report

- operator: `hierarchical-maximum`
- theorem_id: `hierarchical-maximum-margin`
- candidate_digest: `8eb7ccc88431c405947d36f7149db51e56e1dfccdff725c5a21aea8c15a74123`
- bundle_digest: `835ebddf81d6d7991e20d435aa38caa9c0e838bf5cc1211b66bbdc87fd972720`
- crp_digest: `f130f31dbd4d03974f586cb0de2af2bfe08643b43f7539cf964075b9dad7098b`
- verification_run_id: `a55b70a0-8781-4a75-a82b-fcb448770906`

## Authority boundaries

- Statement authority: handwritten `*Prop` definitions between STATEMENT markers.
- Proof authority: Lean kernel (`lake build` + `#print axioms`), not this report.
- Manifest store: ART-10b filesystem surrogate (`LEAN_MANIFEST_WITHOUT_COMMIT`).
- Domain: Mathlib `ℝ` (`REAL_MATHLIB`).
- LLM proof generation: not enabled in v1.

## System 2 statement

Let m>=2 and let scores be constructed by (hierarchical stage scores with unique maximizer). If i* is the unique maximizer with margin gamma>2*epsilon and ||delta||_inf<=epsilon, then i* remains the unique maximizer after perturbation (Hierarchical maximum reduces to Argmax margin).

## Lean propositions

- `hierarchical_maximum_margin_invariance` : `Research.Operators.HierarchicalMaximum.Margin.HierarchicalMaximumMarginInvarianceProp`
- `hierarchical_maximum_margin_sharpness` : `Research.Operators.HierarchicalMaximum.Margin.HierarchicalMaximumMarginSharpnessProp`

## Conclusion tokens

```json
{
  "schema_id": "ARTLEAN.CONCL.hierarchical_maximum_margin.v1"
}
```

- conclusion_digest: `a9601ff1f01cac8c7ef7d57bed1bf87cfbf15735d992af539894cee7089d60d8`
- semantic_freeze_digest: `03ab37fc011dc82ed9352c21cf869f424a502f8ce268767245e75736fd9a32bf`
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
