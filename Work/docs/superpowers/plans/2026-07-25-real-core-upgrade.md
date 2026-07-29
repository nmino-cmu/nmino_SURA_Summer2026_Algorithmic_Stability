# Real-core operator upgrade Implementation Plan

**Status: COMPLETE (2026-07-29).** All 52 certificates are `REAL_MATHLIB` / `LEAN_FULL` on `main` (`2a022c2`). Checkboxes below are historical; do not re-execute.


> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [x]`) syntax for tracking.

**Goal:** Port shared operator cores and every library operator theorem from Int to Mathlib `ℝ`, with `LEAN_FULL` and a commit after each operator.

**Architecture:** Approach A — shared ℝ cores first (`infra/real-cores`), then per-operator alias retarget + re-cert on `operator/<id>-real`.

**Tech Stack:** Lean 4.16.0, Mathlib4 `v4.16.0`, existing System 2/3 certificate pipeline, pytest.

## Global Constraints

- Never implement on `main`; branch per phase/operator.
- No `sorry` / `admit` / custom `axiom` in `Research/`.
- Mathlib via **source build** (cache dyld broken on macOS 26).
- Mid-migration: do **not** run full multi-operator Lean e2e suite (STALE pin risk).
- Commit after each operator merge.
- Plan todos stay `pending` until execution marks them.

---

### Task 1: Plumbing for ℝ certs

**Files:**
- `implementation/src/system_b/lean/report.py`
- `implementation/src/system_b/lean/workflow.py`
- Modify: domain/report text; force recert when upgrading

- [x] Update report generator to use profile domain (`REAL_MATHLIB` vs Int)
- [x] Add force-recert path so `PRESERVE_EXISTING_LEAN_FULL` cannot block ℝ upgrades
- [x] Stop emitting `INT_ORDERED_GROUP_CORE_NOT_REAL` when `MATHLIB_REAL_PENDING` absent
- [x] Commit on `infra/real-cores`

### Task 2: Argmax ℝ Basic + Margin

**Files:**
- `lean/Research/Operators/Argmax/BasicInt.lean` (move from Basic)
- `lean/Research/Operators/Argmax/Basic.lean` (ℝ)
- `lean/Research/Operators/Argmax/MarginInt.lean` / `Margin.lean`
- Argmax e2e + certificate

- [x] Move Int modules aside; implement ℝ `LinfBall` / unique max / margin invariance+sharpness
- [x] `lake build` + argmax e2e `LEAN_FULL`
- [x] Update argmax profile gaps; re-cert; sync metadata/PDF
- [x] Commit

### Task 3: OrderStat + Threshold + Clamp (+ Projection) ℝ cores

- [x] Port OrderStat Basic/KthMargin/Ranking to ℝ
- [x] Port Threshold / MultiThreshold / related scalar cores to ℝ
- [x] Port Projection.Clamp to ℝ; strengthen FeasibleId/Constraint or Euclidean proj as Mathlib allows
- [x] Commit / merge `infra/real-cores`

### Task 4+: Per-operator migration

For each operator in registry order (after argmax):

- [x] Branch `operator/<id>-real`
- [x] Retarget Lean alias + profile to ℝ core
- [x] E2E re-cert; sync package; validators
- [x] Commit, merge, next

### Task final: Library audit

- [x] Full validators + sample lake builds + independent audit
- [x] Update `FINAL-VERDICT.md` / ledger
