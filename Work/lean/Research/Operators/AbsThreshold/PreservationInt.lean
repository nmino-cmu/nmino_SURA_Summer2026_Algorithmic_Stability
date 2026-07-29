import Research.Operators.Argmax.BasicInt

namespace Research.Operators.AbsThreshold.PreservationInt

open Research.Operators.Argmax.BasicInt

/-- `A(x) = 1{|x| ≥ T}` with nonnegative threshold `T`. -/
def absThreshold (x : Int) (T : Nat) : Bool :=
  decide (Int.natAbs x ≥ T)

/- STATEMENT_BEGIN -/
/--
If `|x'-x|≤ε`: `|x|≥T+ε` ⇒ abs-threshold passes; `|x|+ε<T` ⇒ fails.
-/
def AbsThresholdPreservationProp : Prop :=
  ∀ (x : Int) (T : Nat) (ε : Nat) (x' : Int),
    Int.natAbs (x' - x) ≤ ε →
    ((Int.natAbs x ≥ T + ε → absThreshold x' T = true) ∧
     (Int.natAbs x + ε < T → absThreshold x' T = false))

/--
Sharpness on the nonnegative ray with room to push down without crossing zero:
if `ε ≤ x` and `T ≤ x < T+ε`, then `x' = x-ε` fails the absolute threshold.
-/
def AbsThresholdSharpnessProp : Prop :=
  ∀ (x : Int) (T : Nat) (ε : Nat),
    ((ε : Int) ≤ x ∧ (T : Int) ≤ x ∧ x < (T : Int) + (ε : Int)) →
    ∃ x' : Int, Int.natAbs (x' - x) ≤ ε ∧ absThreshold x' T = false
/- STATEMENT_END -/

theorem natAbs_le_add (x x' : Int) (ε : Nat)
    (h : Int.natAbs (x' - x) ≤ ε) :
    Int.natAbs x' ≤ Int.natAbs x + ε := by
  have hx' : x' = x + (x' - x) := by omega
  rw [hx']
  exact Nat.le_trans (Int.natAbs_add_le x (x' - x)) (Nat.add_le_add_left h _)

theorem natAbs_ge_sub (x x' : Int) (ε : Nat)
    (h : Int.natAbs (x' - x) ≤ ε) :
    Int.natAbs x ≤ Int.natAbs x' + ε := by
  have hx : x = x' + (x - x') := by omega
  have hneg : Int.natAbs (x - x') = Int.natAbs (x' - x) := by
    have h1 : x - x' = -(x' - x) := by omega
    rw [h1, Int.natAbs_neg]
  rw [hx]
  have := Int.natAbs_add_le x' (x - x')
  have := Nat.le_trans this (Nat.add_le_add_left (by simpa [hneg] using h) _)
  exact this

theorem abs_threshold_preservation : AbsThresholdPreservationProp := by
  intro x T ε x' hball
  refine And.intro ?pass ?fail
  · intro hx
    have hge := natAbs_ge_sub x x' ε hball
    have : T ≤ Int.natAbs x' := Nat.le_of_add_le_add_right (Nat.le_trans hx hge)
    simp [absThreshold, this]
  · intro hx
    have hle := natAbs_le_add x x' ε hball
    have hlt : Int.natAbs x' < T := Nat.lt_of_le_of_lt hle hx
    have : ¬ (Int.natAbs x' ≥ T) := Nat.not_le_of_gt hlt
    simp [absThreshold, this]

theorem abs_threshold_sharpness : AbsThresholdSharpnessProp := by
  intro x T ε ⟨hεx, hxT, hxhi⟩
  refine ⟨x - (ε : Int), ?_, ?_⟩
  · have : x - (ε : Int) - x = - (ε : Int) := by omega
    simp [this, Int.natAbs_neg]
  · have hx'0 : 0 ≤ x - (ε : Int) := by omega
    have heq : (Int.natAbs (x - (ε : Int)) : Int) = x - (ε : Int) :=
      Int.natAbs_of_nonneg hx'0
    have hltInt : (Int.natAbs (x - (ε : Int)) : Int) < (T : Int) := by
      rw [heq]; omega
    have hlt : Int.natAbs (x - (ε : Int)) < T := Int.ofNat_lt.mp hltInt
    have : ¬ (Int.natAbs (x - (ε : Int)) ≥ T) := Nat.not_le_of_gt hlt
    simp [absThreshold, this]

end Research.Operators.AbsThreshold.PreservationInt
