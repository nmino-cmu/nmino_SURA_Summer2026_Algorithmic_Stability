# Implementation status

| Milestone | Status | Tests | Audit | Commit |
|-----------|--------|-------|-------|--------|
| 1 Shared integration | Done | art_int | PASS WITH MINOR | `f100e37` |
| 2 System A runtime | Done | system_a | PASS WITH MINOR | `f246219` |
| 3 System B adapters | Done | system_b intake | PASS WITH MINOR | `36e9353` |
| 4 Conformance harness | Done | conformance | PASS WITH MINOR | `a417aea` |
| 5 A engines | Done | engines A | PASS WITH MINOR | `6b1c834` |
| 6 B engines | Done | engines B | PASS WITH MINOR | `c6d93bd` + M8 honesty |
| 7 Full integration | Done | integration | PASS | `065c4f5` + M8 honesty |
| 8 Final dual audit | Done | suite 85 | Dual PASS WITH MINOR | `f535fc4` |
| Release verification | Done | suite **86** | Dual PASS WITH MINOR | `37276d2` |
| Argmax margin theorem | Done on `feature/argmax` | suite **97** | Dual PASS WITH MINOR + paper PASS | see merge |
| Lean formalization runtime | Done on `feature/lean-formalization-runtime`; audit repairs on `audit/lean-formalization-impl` | suite **148** + `@pytest.mark.lean` | Trust repairs: axiom capture, skip_lake fail-closed, cert re-verify, ID sanitization | this branch |
| Mathlib ℝ migration | Done | suite **299** | 52/52 certificates `REAL_MATHLIB` + `LEAN_FULL` | on `main` |
| Argmax Phase B packaging | Done | suite **299** | `selection-stability-linf` reuses the `bounded-perturbation-margin` certificate; no new mathematics | on `main` |

## Known limitations (MINOR)

- Demo PASS still uses `DEMO_*` markers (scaffolding, not Lean).
- Argmax PASS uses `ARGMAX_MARGIN_COMPUTATIONAL_V1` (computational) **and** a Lean `LEAN_FULL` certificate on Mathlib ℝ (`REAL_MATHLIB`).
- Lean manifests use filesystem surrogate (`LEAN_MANIFEST_WITHOUT_COMMIT`) until ART-06b Commit exists. On-disk status JSON is not authority; recompute / `verify_certificate`.
- LLM proof repair is not enabled (Phase 5 stub refuses).
- TR-INT-07 uses DIGEST_MISMATCH as STALE_WRITE surrogate.
- Full ART-06b Commit EventLog not in this package scope.
