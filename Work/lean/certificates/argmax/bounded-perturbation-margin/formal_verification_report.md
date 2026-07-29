# Formal verification report

- operator: `argmax`
- theorem_id: `bounded-perturbation-margin`
- candidate_digest: `faa9a5a77b6f8815cb976ca9f88e0daf300ed8a8d9cc2eb8f53ef66baa88b4c0`
- bundle_digest: `ddd0c1a3d5a9c5708a499f581fddeb0b1393369dcf319375808bd27b8323c66e`
- crp_digest: `c314fdf85bd54daa993f2767b5eb168cb640d81e8fd79b1c13d58348ccbff7b0`
- verification_run_id: `9761a950-82d5-4802-8ad4-e26b600dcaf5`

## Authority boundaries

- Statement authority: handwritten `*Prop` definitions between STATEMENT markers.
- Proof authority: Lean kernel (`lake build` + `#print axioms`), not this report.
- Manifest store: ART-10b filesystem surrogate (`LEAN_MANIFEST_WITHOUT_COMMIT`).
- Domain: Mathlib `ℝ` (`REAL_MATHLIB`).
- LLM proof generation: not enabled in v1.

## System 2 statement

Let m≥2, s∈ℝ^m with unique maximizer i*=argmax_i s_i and margin γ(s)=s_{i*}−max_{j≠i*}s_j>0. Let ε≥0 and δ∈ℝ^m with ||δ||_∞≤ε. If γ(s)>2ε, then i* is the unique maximizer of s+δ.

## Lean propositions

- `margin_invariance` : `Research.Operators.Argmax.Margin.MarginInvarianceProp`
- `margin_sharpness` : `Research.Operators.Argmax.Margin.MarginSharpnessProp`

## Conclusion tokens

```json
{
  "epsilon_domain": "NONNEG_REAL",
  "invariance_predicate": "GAMMA_GT_TWO_EPSILON_PRESERVES_UNIQUE_MAX",
  "m_min": 2,
  "margin_def": "S_I_STAR_MINUS_MAX_OTHERS",
  "perturbation_norm": "LINF",
  "requires_unique_maximizer": true,
  "schema_id": "ARTLEAN.CONCL.argmax_margin.v1",
  "score_space": "FIN_TO_REAL",
  "sharpness_predicate": "GAMMA_LE_TWO_EPSILON_EXISTS_BREAKING_DELTA"
}
```

- conclusion_digest: `f8470ce2e8b6d5dc9a24b10d3435228f1d051dffb66d06e23ffb849e786d3597`
- semantic_freeze_digest: `544f8197eb55a857cec5f1c62348c6180d5ec5a83f59d93acd0d946500a5ac8d`
- semantic_audit: `YES`

## Conventions

```json
{
  "equality": "REAL_LE",
  "extensionality": "DEFAULT",
  "finiteness": "FIN_M",
  "measure_stage": "NONE",
  "score_encoding": "REAL_MATHLIB",
  "tie_break": "NONE_UNIQUE_REQUIRED"
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
