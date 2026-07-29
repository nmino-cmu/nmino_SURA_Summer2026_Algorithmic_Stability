import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Linarith
import Research.Operators.Argmax.Basic

namespace Research.Operators.AbsThreshold.Preservation

open Research.Operators.Argmax.Basic

/-- `A(x) = 1{|x| ≥ T}` with nonnegative threshold `T`. -/
def absThreshold (x T : ℝ) : Prop :=
  T ≤ |x|

/- STATEMENT_BEGIN -/
def AbsThresholdPreservationProp : Prop :=
  ∀ (x T ε x' : ℝ),
    0 ≤ T →
    0 ≤ ε →
    |x' - x| ≤ ε →
    ((T + ε ≤ |x| → absThreshold x' T) ∧
     (|x| + ε < T → ¬ absThreshold x' T))

def AbsThresholdSharpnessProp : Prop :=
  ∀ (x T ε : ℝ),
    0 ≤ T →
    0 ≤ ε →
    (ε ≤ x ∧ T ≤ x ∧ x < T + ε) →
    ∃ x' : ℝ, |x' - x| ≤ ε ∧ ¬ absThreshold x' T
/- STATEMENT_END -/

theorem abs_threshold_preservation : AbsThresholdPreservationProp := by
  intro x T ε x' _hT hε hball
  refine And.intro ?pass ?fail
  · intro hx
    -- |x| ≤ |x'| + |x - x'| = |x'| + |x' - x|
    have htri : |x| ≤ |x'| + |x - x'| :=
      (le_add_of_sub_left_le (abs_sub_abs_le_abs_sub x x'))
    have : |x - x'| = |x' - x| := abs_sub_comm x x'
    have : T ≤ |x'| := by linarith
    exact this
  · intro hx
    intro hpass
    have htri : |x'| ≤ |x| + |x' - x| :=
      (le_add_of_sub_left_le (abs_sub_abs_le_abs_sub x' x))
    have : T ≤ |x'| := hpass
    linarith

theorem abs_threshold_sharpness : AbsThresholdSharpnessProp := by
  intro x T ε _hT hε ⟨hεx, hxT, hxhi⟩
  refine ⟨x - ε, ?_, ?_⟩
  · simp [abs_of_nonneg hε]
  · have hx'0 : 0 ≤ x - ε := by linarith
    have habs : |x - ε| = x - ε := abs_of_nonneg hx'0
    intro hpass
    have : T ≤ |x - ε| := hpass
    linarith

end Research.Operators.AbsThreshold.Preservation
