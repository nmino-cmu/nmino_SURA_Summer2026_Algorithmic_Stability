# Lean formalization package (`Research`)

Pinned toolchain: see `lean-toolchain` (Lean 4.16.0).

## Build

```bash
# install elan: https://lean-lang.org/lean4/doc/setup.html
cd lean
lake build
python scripts/forbid_placeholders.py
```

## Notes

- Mathlib is pinned at tag `v4.16.0` (see `lakefile.lean` / `lake-manifest.json`). Smoke: `Research.MathlibSmoke`.
- On macOS 26, `lake exe cache get` still fails (`dyld`: `__DATA_CONST` missing `SG_READ_ONLY` on Mathlib’s `cache` binary). **Workaround:** compile Mathlib from source with `lake build` (no cache). Oleán library builds succeed.
- Operator proofs are on Mathlib ℝ. All 52 accepted certificates recompute to `domain = REAL_MATHLIB`, `derived_lean_status = LEAN_FULL`.
- `scripts/recompute_status.py` derives `domain` from each profile's `score_encoding`, so re-running it preserves `REAL_MATHLIB`. Keep it that way: a profile whose `score_encoding` drifts will silently downgrade its certificate domain.
- `Research/` must contain no `sorry` / `admit` / custom `axiom`.
- Certificates under `certificates/` are ART-10b surrogate manifests (`LEAN_MANIFEST_WITHOUT_COMMIT`).
