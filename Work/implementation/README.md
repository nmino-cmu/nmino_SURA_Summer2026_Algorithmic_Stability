# Implementation — Research Architecture Runtime

**Package:** `research-architecture`  
**Governs:** System A · System B · ART-INT-00  
**Status:** Executable implementation complete — **PASS WITH MINOR ITEMS**
**Release:** [`docs/RELEASE_READINESS.md`](docs/RELEASE_READINESS.md)

## Layout

```text
implementation/
  src/
    art_int/        # Shared integration layer — ART-INT-00
    system_a/       # Discovery runtime + engines
    system_b/       # Verification adapters + engines
    operators/      # Operator-specific math + dischargers (argmax, …)
    conformance/    # ART-INT TRACE_MATRIX harness
    integration/    # End-to-end A↔B workflows
  tests/
  docs/
```

## Authority

Cross-system wire/digests/feedback: `architecture-integration/00-A-B-INTEGRATION.md`  
Canonicalization: ART-21b (SHA-256, sorted JSON keys, omit-absent).

## Known limitations

1. **DEMO_* evaluation** — Demo PASS/FAIL still requires explicit `evaluation` markers (`DEMO_TAUTOLOGY`, …). That path is scaffolding, not a formal proof assistant. Unmarked statements never PASS.
2. **Operator dischargers** — Argmax margin theorem uses `ARGMAX_MARGIN_COMPUTATIONAL_V1` (computational certification) alongside a Lean `LEAN_FULL` certificate on Mathlib ℝ (`REAL_MATHLIB`); Phase B `selection-stability-linf` reuses that same certificate. Lean formalization remains a separate System 3 path (`system_b.lean`, repo `lean/`). See `docs/operators/argmax.md`.
3. **TR-INT-07** — Conformance exercises stale-content safety via `DIGEST_MISMATCH` as a **surrogate** for ART-06b Commit `STALE_WRITE`.

## Dev / clean verify

```bash
cd implementation
python -m venv .venv
.venv/bin/pip install -e ".[dev]"
.venv/bin/pytest -q -m "not lean"
```

### Lean (System 3)

Requires [elan](https://lean-lang.org/lean4/doc/setup.html). Then:

```bash
cd lean && lake build
cd ../implementation && .venv/bin/pytest -q -m lean
```
