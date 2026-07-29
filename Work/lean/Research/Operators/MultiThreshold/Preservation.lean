import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Linarith
import Research.Operators.Threshold.Preservation
import Research.Operators.Argmax.Basic

noncomputable section

namespace Research.Operators.MultiThreshold.Preservation

open Research.Operators.Threshold.Preservation
open Research.Operators.Argmax.Basic

/-- Pass bit as `Nat`. -/
def passBit (x T : ℝ) : Nat :=
  if x ≥ T then 1 else 0

/-- Pass-count over a finite threshold list. -/
def countPasses : ℝ → List ℝ → Nat
  | _, [] => 0
  | x, T :: Ts => passBit x T + countPasses x Ts

/-- Coordinatewise stability. -/
def allCoordsStable (x : ℝ) (Ts : List ℝ) (ε : ℝ) : Prop :=
  ∀ T ∈ Ts, x ≥ T + ε ∨ x < T - ε

/- STATEMENT_BEGIN -/
def MultiThresholdPreservationProp : Prop :=
  ∀ (x : ℝ) (Ts : List ℝ) (ε x' : ℝ),
    0 ≤ ε →
    |x' - x| ≤ ε →
    allCoordsStable x Ts ε →
    countPasses x' Ts = countPasses x Ts

def MultiThresholdSharpnessProp : Prop :=
  ∀ (x T ε : ℝ),
    0 ≤ ε →
    (T - ε ≤ x ∧ x < T + ε) →
    ∃ x' : ℝ, |x' - x| ≤ ε ∧ countPasses x' [T] ≠ countPasses x [T]
/- STATEMENT_END -/

theorem passBit_eq_of_stable
    (x T ε x' : ℝ)
    (hε : 0 ≤ ε)
    (hball : |x' - x| ≤ ε)
    (hT : x ≥ T + ε ∨ x < T - ε) :
    passBit x' T = passBit x T := by
  cases hT with
  | inl hpass =>
    have hx'true : aboveThreshold x' T := (threshold_preservation x T ε x' hε hball).1 hpass
    have hxtrue : x ≥ T := by linarith
    unfold aboveThreshold at hx'true
    simp [passBit, hx'true, hxtrue]
  | inr hfail =>
    have hx'false : ¬ aboveThreshold x' T := (threshold_preservation x T ε x' hε hball).2 hfail
    have hxfalse : ¬ (x ≥ T) := by linarith
    unfold aboveThreshold at hx'false
    simp [passBit, hx'false, hxfalse]

theorem multi_threshold_preservation : MultiThresholdPreservationProp := by
  intro x Ts ε x' hε hball hstable
  induction Ts with
  | nil =>
    rfl
  | cons T Ts ih =>
    have hT : x ≥ T + ε ∨ x < T - ε := hstable T (by simp)
    have hrest : allCoordsStable x Ts ε := by
      intro U hU
      exact hstable U (List.mem_cons_of_mem T hU)
    have ih' := ih hrest
    have hbit := passBit_eq_of_stable x T ε x' hε hball hT
    change passBit x' T + countPasses x' Ts = passBit x T + countPasses x Ts
    rw [hbit, ih']

theorem multi_threshold_sharpness : MultiThresholdSharpnessProp := by
  intro x T ε hε ⟨hlo, hhi⟩
  by_cases hx : x ≥ T
  · refine ⟨x - ε, ?_, ?_⟩
    · simp [abs_of_nonneg hε]
    · have hxpass : passBit x T = 1 := by simp [passBit, hx]
      have hx' : ¬ (x - ε ≥ T) := by linarith
      have hx'fail : passBit (x - ε) T = 0 := by simp [passBit, hx']
      simp [countPasses, hxpass, hx'fail]
  · refine ⟨x + ε, ?_, ?_⟩
    · simp [abs_of_nonneg hε]
    · have hxfail : passBit x T = 0 := by simp [passBit, hx]
      have hx' : x + ε ≥ T := by linarith
      have hx'pass : passBit (x + ε) T = 1 := by simp [passBit, hx']
      simp [countPasses, hxfail, hx'pass]

end Research.Operators.MultiThreshold.Preservation
