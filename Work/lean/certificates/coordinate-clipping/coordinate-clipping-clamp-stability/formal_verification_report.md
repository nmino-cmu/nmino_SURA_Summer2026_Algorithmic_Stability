# Formal verification report

- operator: `coordinate-clipping`
- theorem_id: `coordinate-clipping-clamp-stability`
- candidate_digest: `70af3c8a8aa10a909bac6aea694179c9596c202690032449595e8dca2c45023b`
- bundle_digest: `8688ebb7f634a974c4e2240206066998def84c312d0b9efe68a1709e22f8ae33`
- crp_digest: `2fe46c2fc6edf323423055f58a399dcfa0c5dd3e4d9d348ad4e408ca1dbcb809`
- verification_run_id: `07630772-f40d-424a-bc80-3e168ac8dedc`

## Authority boundaries

- Statement authority: handwritten `*Prop` definitions between STATEMENT markers.
- Proof authority: Lean kernel (`lake build` + `#print axioms`), not this report.
- Manifest store: ART-10b filesystem surrogate (`LEAN_MANIFEST_WITHOUT_COMMIT`).
- Domain: Mathlib `ℝ` (`REAL_MATHLIB`).
- LLM proof generation: not enabled in v1.

## System 2 statement

Let lo<=hi and |x'-x|<=epsilon. Then |clamp(x';lo,hi)-clamp(x;lo,hi)|<=epsilon (Coordinate clipping is 1-Lipschitz / nonexpansive on Int).

## Lean propositions

- `coordinate_clipping_clamp_stability` : `Research.Operators.CoordinateClipping.Preservation.CoordinateClippingStabilityProp`
- `coordinate_clipping_clamp_sharpness` : `Research.Operators.CoordinateClipping.Preservation.CoordinateClippingSharpnessProp`

## Conclusion tokens

```json
{
  "schema_id": "ARTLEAN.CONCL.coordinate_clipping.v1"
}
```

- conclusion_digest: `bd002e36d838dc7066aa33121a8149b825df97bc3c8602751a4c8ca9d4f4ed6e`
- semantic_freeze_digest: `27bd4f4aead214d97a3ac61c3b4b66865d17caf9604f371b328242026143787d`
- semantic_audit: `YES`

## Conventions

```json
{
  "equality": "DEFAULT",
  "extensionality": "DEFAULT",
  "finiteness": "SCALAR_OR_LIST",
  "measure_stage": "NONE",
  "score_encoding": "REAL_MATHLIB",
  "tie_break": "NONE"
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
