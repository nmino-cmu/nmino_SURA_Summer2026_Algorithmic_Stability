# Formal verification report

- operator: `feasible-subset-maximum`
- theorem_id: `feasible-subset-maximum-margin`
- candidate_digest: `eb5059f5598985136cbb70575391da86be02be8512daac2a7fe9a31c632f2805`
- bundle_digest: `b4750c0ef66432152bd11cac627646153ead5460f1f3f494787ab0aabcbf27d6`
- crp_digest: `db4c22a02a9b1f78dacfb5c6b4114d2a9e07f8faea73322d64b854d05538a280`
- verification_run_id: `056fa78e-7e55-4aa8-9b1a-6f78da36f855`

## Authority boundaries

- Statement authority: handwritten `*Prop` definitions between STATEMENT markers.
- Proof authority: Lean kernel (`lake build` + `#print axioms`), not this report.
- Manifest store: ART-10b filesystem surrogate (`LEAN_MANIFEST_WITHOUT_COMMIT`).
- Domain: Mathlib `ℝ` (`REAL_MATHLIB`).
- LLM proof generation: not enabled in v1.

## System 2 statement

Let m>=2 and let scores be constructed by (feasible-subset scores with unique maximizer). If i* is the unique maximizer with margin gamma>2*epsilon and ||delta||_inf<=epsilon, then i* remains the unique maximizer after perturbation (Feasible-subset maximum reduces to Argmax margin).

## Lean propositions

- `feasible_subset_maximum_margin_invariance` : `Research.Operators.FeasibleSubsetMaximum.Margin.FeasibleSubsetMaximumMarginInvarianceProp`
- `feasible_subset_maximum_margin_sharpness` : `Research.Operators.FeasibleSubsetMaximum.Margin.FeasibleSubsetMaximumMarginSharpnessProp`

## Conclusion tokens

```json
{
  "schema_id": "ARTLEAN.CONCL.feasible_subset_maximum_margin.v1"
}
```

- conclusion_digest: `1ed5f32cbba8da8b2f7668acbb35c1ed97a46cdbc4c2f87a16ea0c277722b005`
- semantic_freeze_digest: `49ae0ffa55ec1a579348605c34138088123942a8cebd47579d5e368526b0a0e3`
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
