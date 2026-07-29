import Research.Operators.Argmax.BasicInt

namespace Research.Operators.Sign.PreservationInt

open Research.Operators.Argmax.BasicInt

/-- Trichotomy sign on `Int`: `+1` / `-1` / `0`. -/
def signInt (x : Int) : Int :=
  if x > 0 then (1 : Int) else if x < 0 then (-1 : Int) else (0 : Int)

/- STATEMENT_BEGIN -/
/--
If `|x' - x| ≤ ε`:
- `x > ε` ⇒ `signInt x' = 1`
- `x < -ε` ⇒ `signInt x' = -1`
- `ε = 0 ∧ x = 0` ⇒ `signInt x' = 0`
-/
def SignPreservationProp : Prop :=
  ∀ (x : Int) (ε : Nat) (x' : Int),
    Int.natAbs (x' - x) ≤ ε →
    ((x > (ε : Int) → signInt x' = 1) ∧
     (x < -((ε : Int)) → signInt x' = -1) ∧
     (ε = 0 ∧ x = 0 → signInt x' = 0))

/--
Sharpness on the open unstable bands around 0:
- if `0 < x ∧ x ≤ ε` then some admissible `x'` has `signInt x' ≠ 1`
- if `-ε ≤ x ∧ x < 0` then some admissible `x'` has `signInt x' ≠ -1`
- if `x = 0 ∧ ε > 0` then some admissible `x'` has `signInt x' ≠ 0`
-/
def SignSharpnessProp : Prop :=
  ∀ (x : Int) (ε : Nat),
    ((0 < x ∧ x ≤ (ε : Int)) →
      ∃ x' : Int, Int.natAbs (x' - x) ≤ ε ∧ signInt x' ≠ 1) ∧
    ((-((ε : Int)) ≤ x ∧ x < 0) →
      ∃ x' : Int, Int.natAbs (x' - x) ≤ ε ∧ signInt x' ≠ -1) ∧
    ((x = 0 ∧ 0 < ε) →
      ∃ x' : Int, Int.natAbs (x' - x) ≤ ε ∧ signInt x' ≠ 0)
/- STATEMENT_END -/

theorem sign_preservation : SignPreservationProp := by
  intro x ε x' hball
  refine And.intro ?plus (And.intro ?minus ?zero)
  · intro hx
    have hx' : x' > 0 := by
      have := (natAbs_le_iff (x' - x) ε).mp hball
      omega
    simp [signInt, hx']
  · intro hx
    have hx' : x' < 0 := by
      have := (natAbs_le_iff (x' - x) ε).mp hball
      omega
    have hnpos : ¬ (x' > 0) := by omega
    simp [signInt, hnpos, hx']
  · intro ⟨hε, hx⟩
    have : x' = x := by
      have := (natAbs_le_iff (x' - x) ε).mp hball
      simp [hε] at this
      omega
    subst this
    simp [signInt, hx]

theorem sign_of_nonpos (y : Int) (h : y ≤ 0) : signInt y ≠ 1 := by
  by_cases hpos : y > 0
  · omega
  · by_cases hneg : y < 0
    · simp [signInt, hpos, hneg]
    · simp [signInt, hpos, hneg]

theorem sign_of_nonneg (y : Int) (h : y ≥ 0) : signInt y ≠ -1 := by
  by_cases hpos : y > 0
  · simp [signInt, hpos]
  · by_cases hneg : y < 0
    · omega
    · simp [signInt, hpos, hneg]

theorem sign_sharpness : SignSharpnessProp := by
  intro x ε
  refine And.intro ?pos (And.intro ?neg ?zero)
  · intro ⟨hxpos, hxle⟩
    refine ⟨x - (ε : Int), ?_, sign_of_nonpos _ (by omega)⟩
    · have : x - (ε : Int) - x = - (ε : Int) := by omega
      simp [this, Int.natAbs_neg]
  · intro ⟨hxge, hxneg⟩
    refine ⟨x + (ε : Int), ?_, sign_of_nonneg _ (by omega)⟩
    · have : x + (ε : Int) - x = (ε : Int) := by omega
      simp [this]
  · intro ⟨hx, hε⟩
    refine ⟨(ε : Int), ?_, ?_⟩
    · subst hx
      simp
    · subst hx
      have hpos : (ε : Int) > 0 := by omega
      have : signInt (ε : Int) = 1 := by simp [signInt, hpos]
      omega

end Research.Operators.Sign.PreservationInt
