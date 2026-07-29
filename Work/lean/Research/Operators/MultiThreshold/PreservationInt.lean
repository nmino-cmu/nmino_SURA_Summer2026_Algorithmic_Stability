import Research.Operators.Threshold.PreservationInt
import Research.Operators.Argmax.BasicInt

namespace Research.Operators.MultiThreshold.PreservationInt

open Research.Operators.Threshold.PreservationInt
open Research.Operators.Argmax.BasicInt

/-- Pass bit as `Nat`. -/
def passBit (x T : Int) : Nat :=
  if decide (x ≥ T) then 1 else 0

/-- Pass-count over a finite threshold list: `#{T ∈ Ts | x ≥ T}`. -/
def countPasses : Int → List Int → Nat
  | _, [] => 0
  | x, T :: Ts => passBit x T + countPasses x Ts

/-- Coordinatewise stability: each cut is outside the half-open unstable band. -/
def allCoordsStable (x : Int) (Ts : List Int) (ε : Nat) : Prop :=
  ∀ T ∈ Ts, x ≥ T + (ε : Int) ∨ x < T - (ε : Int)

/- STATEMENT_BEGIN -/
/--
If `|x' - x| ≤ ε` and every threshold coordinate is ε-stable for `x`, then
`countPasses x' Ts = countPasses x Ts`.
-/
def MultiThresholdPreservationProp : Prop :=
  ∀ (x : Int) (Ts : List Int) (ε : Nat) (x' : Int),
    Int.natAbs (x' - x) ≤ ε →
    allCoordsStable x Ts ε →
    countPasses x' Ts = countPasses x Ts

/--
Sharpness: if a listed cut `T` lies in the unstable band, some admissible
perturbation flips the pass-count of the singleton list `[T]`.
-/
def MultiThresholdSharpnessProp : Prop :=
  ∀ (x T : Int) (ε : Nat),
    (T - (ε : Int) ≤ x ∧ x < T + (ε : Int)) →
    ∃ x' : Int, Int.natAbs (x' - x) ≤ ε ∧ countPasses x' [T] ≠ countPasses x [T]
/- STATEMENT_END -/

theorem passBit_eq_of_stable
    (x T : Int) (ε : Nat) (x' : Int)
    (hball : Int.natAbs (x' - x) ≤ ε)
    (hT : x ≥ T + (ε : Int) ∨ x < T - (ε : Int)) :
    passBit x' T = passBit x T := by
  cases hT with
  | inl hpass =>
    have hx'true : x' ≥ T := by
      have := (threshold_preservation x T ε x' hball).1 hpass
      simpa [aboveThreshold] using this
    have hxtrue : x ≥ T := by omega
    simp [passBit, hx'true, hxtrue]
  | inr hfail =>
    have hx'false : ¬ (x' ≥ T) := by
      have := (threshold_preservation x T ε x' hball).2 hfail
      simpa [aboveThreshold] using this
    have hxfalse : ¬ (x ≥ T) := by omega
    simp [passBit, hx'false, hxfalse]

theorem multi_threshold_preservation : MultiThresholdPreservationProp := by
  intro x Ts ε x' hball hstable
  induction Ts with
  | nil =>
    simp [countPasses]
  | cons T Ts ih =>
    have hT : x ≥ T + (ε : Int) ∨ x < T - (ε : Int) := hstable T (by simp)
    have hrest : allCoordsStable x Ts ε := by
      intro U hU
      exact hstable U (List.mem_cons_of_mem T hU)
    have ih' := ih hrest
    have hbit := passBit_eq_of_stable x T ε x' hball hT
    simp [countPasses, hbit, ih']

theorem multi_threshold_sharpness : MultiThresholdSharpnessProp := by
  intro x T ε ⟨hlo, hhi⟩
  by_cases hx : x ≥ T
  · refine ⟨x - (ε : Int), ?_, ?_⟩
    · have : x - (ε : Int) - x = - (ε : Int) := by omega
      simp [this, Int.natAbs_neg]
    · have hxpass : countPasses x [T] = 1 := by
        simp [countPasses, passBit, hx]
      have hx' : ¬ (x - (ε : Int) ≥ T) := by omega
      have hx'fail : countPasses (x - (ε : Int)) [T] = 0 := by
        simp [countPasses, passBit, hx']
      omega
  · refine ⟨x + (ε : Int), ?_, ?_⟩
    · have : x + (ε : Int) - x = (ε : Int) := by omega
      simp [this]
    · have hxfail : countPasses x [T] = 0 := by
        simp [countPasses, passBit, hx]
      have hx' : x + (ε : Int) ≥ T := by omega
      have hx'pass : countPasses (x + (ε : Int)) [T] = 1 := by
        simp [countPasses, passBit, hx']
      omega

end Research.Operators.MultiThreshold.PreservationInt
