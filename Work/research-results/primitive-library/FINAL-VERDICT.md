# Primitive Operator Library — Final Verdict

**Date:** 2026-07-29  
**Git HEAD (Work):** `c2f46352e7c28598606884693111d0f2b7cff8da`  
**Registry:** [operators.json](operators.json) · **Index:** [index.json](index.json) (generated; do not hand-edit)  
**Validators:** [validate_index.py](validation/validate_index.py) · [validate_metadata.py](validation/validate_metadata.py) — **PASS** (rechecked 2026-07-29)  
**Library README:** [README.md](README.md) · **Package map:** [../../../README.md](../../../README.md)

---

## Verdict

**Library complete (with named, intentional residuals).**

| Quantity | Value |
|----------|------:|
| Complete operators | **50** |
| Reserved reference | **1** ([`argmax`](../argmax/)) |
| Indexed theorem packages | **53** |
| `lean_status = LEAN_FULL` | **53 / 53** |
| Score encoding | Mathlib \(\mathbb{R}\) (`REAL_MATHLIB`) |
| Blocking / major | **0 / 0** |

Lean is the formal authority. Each `*_paper.pdf` under [research-results/](../) explains the claim and must not strengthen it.

---

## What this is

A finite catalog of **selection primitives** with a **stability theorem** each: under a stated perturbation budget, the selected object (or region membership) is preserved.

**Not** a full formalization of [Problem_Writeup.pdf](../../../Formulation/writeup/Problem_Writeup.pdf). That writeup states the research problem; this library certifies the primitive catalog that underwrites it.

---

## How to read one result

Example: **median**

| Artifact | Link |
|----------|------|
| Paper | [median_paper.pdf](../median/median-margin/median_paper.pdf) |
| Metadata | [metadata.json](../median/median-margin/metadata.json) |
| Lean module | [Preservation.lean](../../lean/Research/Operators/Median/Preservation.lean) |
| Certificate | [lean/certificates/median/median-margin/](../../lean/certificates/median/median-margin/) |
| Formal report | [formal_verification_report.md](../../lean/certificates/median/median-margin/formal_verification_report.md) |

Treat `LEAN_FULL` + digests in the certificate as the proof of record. Build: [lean/README.md](../../lean/README.md).

### Other clean entry points

| Paper | Lean | Certificate |
|-------|------|-------------|
| [thresholding — bounded noise](../thresholding/bounded-noise-threshold/thresholding_paper.pdf) | [BoundedNoise.lean](../../lean/Research/Operators/Threshold/BoundedNoise.lean) | [cert](../../lean/certificates/thresholding/bounded-noise-threshold/) |
| [quantile — margin](../quantile/quantile-margin/quantile_paper.pdf) | [Preservation.lean](../../lean/Research/Operators/Quantile/Preservation.lean) | [cert](../../lean/certificates/quantile/quantile-margin/) |

---

## Coverage by family

| Family | Proof pattern |
|--------|----------------|
| Scalar / region | Threshold-style buffers |
| Order statistics / ranking / top-\(k\) | `OrderStat` ranking / \(k\)-th margin cores |
| Unique-max / greedy / heaps / NMS / masks | Definitional `Argmax.Margin` reductions |
| Interval / box / clipping | `Projection.Clamp` (1-Lipschitz) |
| Simplex / \(\ell_2\) / \(\ell_1\) / feasibility | `Projection.FeasibleId` (\(\varepsilon\)-interior identity; limited) |
| Threshold ∧ / ∨ | `Projection.Constraint` → multi-threshold |

---

## Intentional omissions (not defects)

1. Reserved optimization operators (LP, matching, flows, DP, A\*, …) — out of scope.
2. Min-aliases (bottom-\(k\), extract-min, …) — use score negation of max variants.
3. Simplex / \(\ell_2\) / \(\ell_1\) / feasibility-indicator — honest **feasible-ball identity**, not full Euclidean projection nonexpansiveness.
4. [`argmax`](../argmax/) is `reserved_reference`. Packages are indexed and `LEAN_FULL` (e.g. [bounded-perturbation-margin](../argmax/bounded-perturbation-margin/), Phase B hop [selection-stability-linf](../argmax/selection-stability-linf/)) but argmax is **not** one of the 50 complete primitives.

---

## Complete operators (50)

[`thresholding`](../thresholding/) · [`multi-threshold`](../multi-threshold/) · [`sign`](../sign/) · [`absolute-value-threshold`](../absolute-value-threshold/) · [`interval-membership`](../interval-membership/) · [`quantile`](../quantile/) · [`median`](../median/) · [`percentile`](../percentile/) · [`kth-order-statistic`](../kth-order-statistic/) · [`top-k`](../top-k/) · [`sorting`](../sorting/) · [`stable-sorting`](../stable-sorting/) · [`partial-sorting`](../partial-sorting/) · [`rank`](../rank/) · [`lexicographic-ordering`](../lexicographic-ordering/) · [`tournament-winner`](../tournament-winner/) · [`weighted-tournament-winner`](../weighted-tournament-winner/) · [`tie-broken-winner`](../tie-broken-winner/) · [`projection-interval`](../projection-interval/) · [`projection-box`](../projection-box/) · [`projection-simplex`](../projection-simplex/) · [`projection-l2-ball`](../projection-l2-ball/) · [`projection-l1-ball`](../projection-l1-ball/) · [`coordinate-clipping`](../coordinate-clipping/) · [`feasibility-indicator`](../feasibility-indicator/) · [`constraint-threshold-conjunction`](../constraint-threshold-conjunction/) · [`constraint-threshold-disjunction`](../constraint-threshold-disjunction/) · [`heap-top`](../heap-top/) · [`heap-extract-max`](../heap-extract-max/) · [`priority-queue-maximum`](../priority-queue-maximum/) · [`greedy-maximum-selection`](../greedy-maximum-selection/) · [`greedy-choice-tie-break`](../greedy-choice-tie-break/) · [`beam-pruning`](../beam-pruning/) · [`best-first-node-selection`](../best-first-node-selection/) · [`lexicographic-best-first`](../lexicographic-best-first/) · [`nms-finite`](../nms-finite/) · [`filter-then-max`](../filter-then-max/) · [`masked-maximum`](../masked-maximum/) · [`feasible-subset-maximum`](../feasible-subset-maximum/) · [`masked-top-k`](../masked-top-k/) · [`hierarchical-maximum`](../hierarchical-maximum/) · [`two-stage-maximum`](../two-stage-maximum/) · [`groupwise-then-global-maximum`](../groupwise-then-global-maximum/) · [`multi-criteria-lexicographic`](../multi-criteria-lexicographic/) · [`weighted-score-selection`](../weighted-score-selection/) · [`penalized-score-selection`](../penalized-score-selection/) · [`threshold-then-top-k`](../threshold-then-top-k/) · [`top-k-then-threshold`](../top-k-then-threshold/) · [`stable-partition-threshold`](../stable-partition-threshold/) · [`bucket-assignment`](../bucket-assignment/)

**Reserved:** [`argmax`](../argmax/)

---

## Skip on first read

[architecture-discovery/](../../architecture-discovery/) · [architecture_verifier/](../../architecture_verifier/) · [architecture-integration/](../../architecture-integration/) · [docs/superpowers/](../../docs/superpowers/)
