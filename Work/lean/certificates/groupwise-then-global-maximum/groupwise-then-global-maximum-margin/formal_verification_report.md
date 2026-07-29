# Formal verification report

- operator: `groupwise-then-global-maximum`
- theorem_id: `groupwise-then-global-maximum-margin`
- candidate_digest: `a9962a1ce2092eefefe60c07f724284ec7fd8d57579ffc5ab271bf44ab8ca386`
- bundle_digest: `c15276b65c88c63dfbec8075142c34a8c0b3a33f09c60d9ff70f4f9f81413356`
- crp_digest: `3903731e2f8bc442ea60fc5c2a1a68394c27b6f233d9bd257d4e6312e49af30f`
- verification_run_id: `bce42dbf-a2c3-4926-8403-b965774b12f2`

## Authority boundaries

- Statement authority: handwritten `*Prop` definitions between STATEMENT markers.
- Proof authority: Lean kernel (`lake build` + `#print axioms`), not this report.
- Manifest store: ART-10b filesystem surrogate (`LEAN_MANIFEST_WITHOUT_COMMIT`).
- Domain: Mathlib `ℝ` (`REAL_MATHLIB`).
- LLM proof generation: not enabled in v1.

## System 2 statement

Let m>=2 and let scores be constructed by (groupwise-then-global scores with unique maximizer). If i* is the unique maximizer with margin gamma>2*epsilon and ||delta||_inf<=epsilon, then i* remains the unique maximizer after perturbation (Groupwise-then-global maximum reduces to Argmax margin).

## Lean propositions

- `groupwise_then_global_maximum_margin_invariance` : `Research.Operators.GroupwiseThenGlobalMaximum.Margin.GroupwiseThenGlobalMaximumMarginInvarianceProp`
- `groupwise_then_global_maximum_margin_sharpness` : `Research.Operators.GroupwiseThenGlobalMaximum.Margin.GroupwiseThenGlobalMaximumMarginSharpnessProp`

## Conclusion tokens

```json
{
  "schema_id": "ARTLEAN.CONCL.groupwise_then_global_maximum_margin.v1"
}
```

- conclusion_digest: `e7a25a69b6cb6aba81b24f36287f2dc9aec073417f4eb76648a2603e03daf46f`
- semantic_freeze_digest: `363f530965074dfda3d3ecf305404311fe53f627af2ae9651d0a399b16df43a0`
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
