# Formal verification report

- operator: `heap-top`
- theorem_id: `heap-top-margin`
- candidate_digest: `96d17aa61b4441e776ba5c15cb9ba97d2a141861cd2691d8097c55871c2f6443`
- bundle_digest: `1d2f3d1b074dd22e444081193246f06013e594ed44dada628ccc194a23549309`
- crp_digest: `1e1dfbc6cb5a0d18e918dc056e71b9a052512d16eadf5f107051f9da4ba809b5`
- verification_run_id: `0b995329-d8ef-45b3-893e-57378078f72c`

## Authority boundaries

- Statement authority: handwritten `*Prop` definitions between STATEMENT markers.
- Proof authority: Lean kernel (`lake build` + `#print axioms`), not this report.
- Manifest store: ART-10b filesystem surrogate (`LEAN_MANIFEST_WITHOUT_COMMIT`).
- Domain: Mathlib `ℝ` (`REAL_MATHLIB`).
- LLM proof generation: not enabled in v1.

## System 2 statement

Let m>=2 and let scores be constructed by (heap key scores with unique maximizer). If i* is the unique maximizer with margin gamma>2*epsilon and ||delta||_inf<=epsilon, then i* remains the unique maximizer after perturbation (Heap top reduces to Argmax margin).

## Lean propositions

- `heap_top_margin_invariance` : `Research.Operators.HeapTop.Margin.HeapTopMarginInvarianceProp`
- `heap_top_margin_sharpness` : `Research.Operators.HeapTop.Margin.HeapTopMarginSharpnessProp`

## Conclusion tokens

```json
{
  "schema_id": "ARTLEAN.CONCL.heap_top_margin.v1"
}
```

- conclusion_digest: `7b4cbbdc8a0a87c32cea60357089bc3497f919a8ac0cc6ebcd00b16291b4c6c0`
- semantic_freeze_digest: `f52173268e4d1e6e8c320e9407d0b719890da76ecb41f43ee26bb7feda19817e`
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
