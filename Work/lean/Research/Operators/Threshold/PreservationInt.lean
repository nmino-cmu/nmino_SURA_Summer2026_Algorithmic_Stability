import Research.Operators.Argmax.BasicInt

namespace Research.Operators.Threshold.PreservationInt

open Research.Operators.Argmax.BasicInt

/-- Pass when score ≥ threshold (`A_T(x)=1 ↔ x ≥ T`). -/
def aboveThreshold (x T : Int) : Bool :=
  decide (x ≥ T)

/- STATEMENT_BEGIN -/
/--
If `|x' - x| ≤ ε` and `x ≥ T + ε`, then `aboveThreshold x' T = true`.
Fail-side: `x < T - ε` ⇒ false.
-/
def ThresholdPreservationProp : Prop :=
  ∀ (x T : Int) (ε : Nat) (x' : Int),
    Int.natAbs (x' - x) ≤ ε →
    ((x ≥ T + (ε : Int) → aboveThreshold x' T = true) ∧
     (x < T - (ε : Int) → aboveThreshold x' T = false))
/- STATEMENT_END -/

theorem threshold_preservation : ThresholdPreservationProp := by
  intro x T ε x' hball
  refine And.intro ?pass ?fail
  · intro hx
    have hx' : x' ≥ T := by
      have := (natAbs_le_iff (x' - x) ε).mp hball
      omega
    simp [aboveThreshold, hx']
  · intro hx
    have hx' : ¬ (x' ≥ T) := by
      have := (natAbs_le_iff (x' - x) ε).mp hball
      omega
    simp [aboveThreshold, hx']

end Research.Operators.Threshold.PreservationInt
