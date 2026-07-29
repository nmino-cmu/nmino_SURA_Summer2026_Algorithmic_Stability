# Formal verification report

- operator: `lexicographic-best-first`
- theorem_id: `lexicographic-best-first-margin`
- candidate_digest: `e002e337dd65e4328438b6558383d164176cdf961bb8d987fd8406b9b4d7182e`
- bundle_digest: `b47d9cb0a48e5fff5b8df8c8019eb1dd21a30cefba0c5f9e6670087e622a816f`
- crp_digest: `285f1738d21c77ae77db5f2e7eeb28665b90c7c8c6ff10b6c09555aa07262a52`
- verification_run_id: `4b7f9a87-7fc2-4f78-8221-8c397914c920`

## Authority boundaries

- Statement authority: handwritten `*Prop` definitions between STATEMENT markers.
- Proof authority: Lean kernel (`lake build` + `#print axioms`), not this report.
- Manifest store: ART-10b filesystem surrogate (`LEAN_MANIFEST_WITHOUT_COMMIT`).
- Domain: Mathlib `ℝ` (`REAL_MATHLIB`).
- LLM proof generation: not enabled in v1.

## System 2 statement

Let m>=2 and let scores be constructed by (lex-encoded best-first scores with unique maximizer). If i* is the unique maximizer with margin gamma>2*epsilon and ||delta||_inf<=epsilon, then i* remains the unique maximizer after perturbation (Lexicographic best-first reduces to Argmax margin).

## Lean propositions

- `lexicographic_best_first_margin_invariance` : `Research.Operators.LexicographicBestFirst.Margin.LexicographicBestFirstMarginInvarianceProp`
- `lexicographic_best_first_margin_sharpness` : `Research.Operators.LexicographicBestFirst.Margin.LexicographicBestFirstMarginSharpnessProp`

## Conclusion tokens

```json
{
  "schema_id": "ARTLEAN.CONCL.lexicographic_best_first_margin.v1"
}
```

- conclusion_digest: `7034512c5bb3178e0354542b2409e709c2e44e4eeb48b7aeaf5c1240c1cecb50`
- semantic_freeze_digest: `322a5dfdb197a2f27bc0ee25c5e8cbe0a919ecab9e177748e74115bf111edc54`
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
