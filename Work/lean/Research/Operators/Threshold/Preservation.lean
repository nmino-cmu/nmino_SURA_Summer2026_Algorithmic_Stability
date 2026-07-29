import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Linarith
import Research.Operators.Argmax.Basic

namespace Research.Operators.Threshold.Preservation

open Research.Operators.Argmax.Basic

/-- Pass when score ≥ threshold (`A_T(x)=1 ↔ x ≥ T`). -/
def aboveThreshold (x T : ℝ) : Prop :=
  x ≥ T

/- STATEMENT_BEGIN -/
/--
If `|x' - x| ≤ ε` and `x ≥ T + ε`, then `aboveThreshold x' T`.
Fail-side: `x < T - ε` ⇒ not above threshold.
-/
def ThresholdPreservationProp : Prop :=
  ∀ (x T ε x' : ℝ),
    0 ≤ ε →
    |x' - x| ≤ ε →
    ((x ≥ T + ε → aboveThreshold x' T) ∧
     (x < T - ε → ¬ aboveThreshold x' T))
/- STATEMENT_END -/

theorem threshold_preservation : ThresholdPreservationProp := by
  intro x T ε x' hε hball
  have hb := (abs_le_iff (x' - x) ε).mp hball
  refine And.intro ?pass ?fail
  · intro hx
    have : x' ≥ T := by linarith
    exact this
  · intro hx
    intro hpass
    have : x' ≥ T := hpass
    linarith

end Research.Operators.Threshold.Preservation
