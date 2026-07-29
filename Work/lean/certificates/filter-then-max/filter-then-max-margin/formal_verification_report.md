# Formal verification report

- operator: `filter-then-max`
- theorem_id: `filter-then-max-margin`
- candidate_digest: `08ca311379d74b3f8218abf1ad6bac91439fc27a274bc5a56c21d583da622852`
- bundle_digest: `5a56f065c146e7d7c5cc39d5460233324fdd6283847f70412471081f4a7e9e1e`
- crp_digest: `7c3658ce392aa493665ba45f82bd53ebfe9cc4ffdf65cf92e0585978671d6dd2`
- verification_run_id: `dcf25da7-0f67-4ec6-b21a-f3a14069ea17`

## Authority boundaries

- Statement authority: handwritten `*Prop` definitions between STATEMENT markers.
- Proof authority: Lean kernel (`lake build` + `#print axioms`), not this report.
- Manifest store: ART-10b filesystem surrogate (`LEAN_MANIFEST_WITHOUT_COMMIT`).
- Domain: Mathlib `ℝ` (`REAL_MATHLIB`).
- LLM proof generation: not enabled in v1.

## System 2 statement

Let m>=2 and let scores be constructed by (filtered candidate scores with unique maximizer). If i* is the unique maximizer with margin gamma>2*epsilon and ||delta||_inf<=epsilon, then i* remains the unique maximizer after perturbation (Filter-then-max reduces to Argmax margin).

## Lean propositions

- `filter_then_max_margin_invariance` : `Research.Operators.FilterThenMax.Margin.FilterThenMaxMarginInvarianceProp`
- `filter_then_max_margin_sharpness` : `Research.Operators.FilterThenMax.Margin.FilterThenMaxMarginSharpnessProp`

## Conclusion tokens

```json
{
  "schema_id": "ARTLEAN.CONCL.filter_then_max_margin.v1"
}
```

- conclusion_digest: `e202c4e19eb95a91fe54ee84de74bbd67a8489d3f61c864f2bb6157225f77689`
- semantic_freeze_digest: `b3386d6b3df3dd0a842853561b95f91722acb71d1475babb6b7f9d3890194d3c`
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
