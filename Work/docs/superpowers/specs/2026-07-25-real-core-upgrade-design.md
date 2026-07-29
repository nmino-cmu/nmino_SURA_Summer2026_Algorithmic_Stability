# Real-core operator upgrade (Approach A) — Design

**Date:** 2026-07-25  
**Status:** Approved (user: audit, fix, approve all, begin)  
**Main baseline:** Mathlib pinned @ `v4.16.0` (`45bf909`+)

## 1. Goal

Upgrade every complete primitive-library operator (and the reserved Argmax reference theorem) from the **Int ordered-group core** to **Mathlib `ℝ`**, with kernel-checked `LEAN_FULL` proofs matching the published claims as closely as possible. **Commit after each operator** migration.

## 2. Audit findings (fixes applied to this design)

| Issue | Fix |
|-------|-----|
| `lake-manifest` Mathlib pin changed ⇒ existing certs become `LEAN_STALE` vs new `toolchain_head` | Migration ship scripts run **only the target operator’s** Lean e2e + unit + library validators that don’t require global pin freshness; optional one-shot pin-bump later. Do **not** full-suite all Lean e2e mid-migration. |
| `PRESERVE_EXISTING_LEAN_FULL` can block cert overwrite | Add explicit `force_recert=True` (or domain-change) path so ℝ upgrades always persist new manifests. |
| `report.py` hardcodes “Int-core / not ℝ” | Drive report domain from profile (`REAL_MATHLIB` vs Int); stop claiming Int when gap cleared. |
| `omega` does not work on `ℝ` | Use Mathlib (`linarith`, `nlinarith`, `abs_*`, ordered-field lemmas). |
| ε was `Nat` on Int | On ℝ: `ε : ℝ` with `0 ≤ ε`. |
| Replacing Int in place breaks mid-migration aliases | **Move** Int modules to `*Int.lean` (or `Int/` subdir); Real becomes the primary `Margin.lean` / `Preservation.lean` that aliases/operators import. |
| Full Euclidean proj for simplex/ℓp may be heavy | Prove strongest Mathlib-supported statement; if only nonexpansiveness of metric projection onto a closed convex set is available, use that; else keep honest residual gap (never fake ℝ Euclidean completeness). |
| Argmax is `reserved_reference` | Still upgrade its Lean+certificate (canonical core); **do not** change registry to a library package. |
| Mathlib binary cache dyld broken on macOS 26 | Source builds only (already documented). |
| Imported Mathlib axioms (`Classical.choice`, …) | Allowed as **imported** axiom closure; still `LEAN_FULL` if no custom axioms/`sorry`. |

## 3. Architecture (Approach A)

```text
Phase 0  Shared ℝ cores (infra/real-cores)
         Argmax.Basic/Margin, OrderStat.*, Threshold*, Projection.Clamp,
         Projection Euclidean/feasible-on-ℝ
Phase 1+ Per operator: point alias → e2e LEAN_FULL → sync metadata/PDF
         → commit → merge → next (operators.json sequence; Argmax first)
```

Operators remain thin definitional aliases to cores wherever that is mathematically accurate (argmax-reductions, ranking family, clamp family, multi-threshold constraints).

## 4. Concrete Lean API (Phase 0)

### 4.1 `Research.Operators.Argmax.Basic` (ℝ)

- `IsMaximizer` / `IsUniqueMaximizer` on `Fin m → ℝ`
- `LinfBall (δ : Fin m → ℝ) (ε : ℝ)` := `∀ i, |δ i| ≤ ε`
- Helpers for abs arithmetic (Mathlib)

Int originals → `Argmax/BasicInt.lean` (kept until migration complete).

### 4.2 `Research.Operators.Argmax.Margin` (ℝ)

Same propositions as today with `ℝ` scores and `ε : ℝ`, `0 ≤ ε`, strict margin `γ > 2ε`.

### 4.3 OrderStat / Threshold / Clamp

Analogous ℝ ports of existing Int statements (ranking gaps, k-th uniqueness, threshold buffers, clamp 1-Lipschitz).

### 4.4 Simplex / ℓ1 / ℓ2

Prefer Mathlib metric/orthogonal projection nonexpansiveness onto the relevant closed convex set. If unavailable at pin `v4.16.0`, ship the strongest proved ℝ theorem and retain a **named residual gap** (not `MATHLIB_REAL_PENDING`).

## 5. Profile / certificate contract (per migrated operator)

When Lean props are truly on `ℝ`:

- `CONVENTIONS["score_encoding"] = "REAL_MATHLIB"`
- Remove `MATHLIB_REAL_PENDING` from `KNOWN_GAPS`
- Certificate `status_display.domain = "REAL_MATHLIB"`
- Do **not** append `INT_ORDERED_GROUP_CORE_NOT_REAL`
- Papers/metadata: state ℝ; limitations list only residual gaps (if any)

## 6. Branching & commits

| Phase | Branch | Commit policy |
|-------|--------|----------------|
| Plumbing + cores | `infra/real-cores` | Milestone commits; merge when Phase 0 cores `LEAN_FULL` |
| Each operator | `operator/<id>-real` | One commit (or small series) then merge to `main` before next |

Never implement on `main`.

## 7. Per-operator checklist

1. Branch from latest `main`
2. Point operator Lean module at ℝ core; update `lean_profile` gaps/conventions
3. Force re-cert e2e → `LEAN_FULL` with `REAL_MATHLIB` domain
4. Sync metadata + PDF language; clear Int-core claims
5. `validate_metadata` / `validate_index` / operator unit test
6. Commit, push, merge, delete branch
7. Next operator

## 8. Queue order

1. Reserved **argmax** (canonical margin) — Lean+cert only  
2. Remaining complete operators in `operators.json` `sequence` order

## 9. Success criteria

- All complete operators + argmax reference: Lean props on `ℝ`, `LEAN_FULL`, no `MATHLIB_REAL_PENDING` unless an explicit residual (projection edge cases only)
- Library validators PASS on `main`
- Independent audit: BLOCKING=0, MAJOR=0

## 10. Out of scope

Reserved optimization operators; min-alias packages; fixing Mathlib binary cache on macOS 26.
