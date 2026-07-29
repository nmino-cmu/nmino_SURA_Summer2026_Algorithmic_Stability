import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Linarith
import Research.Operators.Argmax.Basic

noncomputable section

namespace Research.Operators.Sign.Preservation

open Research.Operators.Argmax.Basic

/-- Trichotomy sign on `ℝ`: `+1` / `-1` / `0`. -/
def signReal (x : ℝ) : ℝ :=
  if 0 < x then (1 : ℝ) else if x < 0 then (-1 : ℝ) else (0 : ℝ)

/- STATEMENT_BEGIN -/
def SignPreservationProp : Prop :=
  ∀ (x ε x' : ℝ),
    0 ≤ ε →
    |x' - x| ≤ ε →
    ((ε < x → signReal x' = 1) ∧
     (x < -ε → signReal x' = -1) ∧
     (ε = 0 ∧ x = 0 → signReal x' = 0))

def SignSharpnessProp : Prop :=
  ∀ (x ε : ℝ),
    0 ≤ ε →
    ((0 < x ∧ x ≤ ε) → ∃ x' : ℝ, |x' - x| ≤ ε ∧ signReal x' ≠ 1) ∧
    ((-ε ≤ x ∧ x < 0) → ∃ x' : ℝ, |x' - x| ≤ ε ∧ signReal x' ≠ -1) ∧
    ((x = 0 ∧ 0 < ε) → ∃ x' : ℝ, |x' - x| ≤ ε ∧ signReal x' ≠ 0)
/- STATEMENT_END -/

theorem sign_preservation : SignPreservationProp := by
  intro x ε x' hε hball
  have hb := (abs_le_iff (x' - x) ε).mp hball
  refine And.intro ?plus (And.intro ?minus ?zero)
  · intro hx
    have : 0 < x' := by linarith
    simp [signReal, this]
  · intro hx
    have hx' : x' < 0 := by linarith
    have hnpos : ¬ (0 < x') := by linarith
    simp [signReal, hnpos, hx']
  · intro ⟨hε0, hx0⟩
    have : x' = x := by
      have : |x' - x| ≤ 0 := by simpa [hε0] using hball
      exact sub_eq_zero.mp (abs_nonpos_iff.mp this)
    simp [this, hx0, signReal]

theorem sign_of_nonpos (y : ℝ) (h : y ≤ 0) : signReal y ≠ 1 := by
  intro hs
  unfold signReal at hs
  split_ifs at hs with hpos hneg
  · linarith
  · exact absurd hs (by norm_num)
  · exact absurd hs (by norm_num)

theorem sign_of_nonneg (y : ℝ) (h : 0 ≤ y) : signReal y ≠ -1 := by
  intro hs
  unfold signReal at hs
  split_ifs at hs with hpos hneg
  · exact absurd hs (by norm_num)
  · linarith
  · exact absurd hs (by norm_num)

theorem sign_sharpness : SignSharpnessProp := by
  intro x ε hε
  refine And.intro ?pos (And.intro ?neg ?zero)
  · intro ⟨hxpos, hxle⟩
    refine ⟨x - ε, ?_, sign_of_nonpos _ (by linarith)⟩
    · simp [abs_of_nonneg hε]
  · intro ⟨hxge, hxneg⟩
    refine ⟨x + ε, ?_, sign_of_nonneg _ (by linarith)⟩
    · simp [abs_of_nonneg hε]
  · intro ⟨hx, hεpos⟩
    refine ⟨ε, ?_, ?_⟩
    · simp [hx, abs_of_nonneg hε]
    · have : signReal ε = 1 := by
        simp [signReal, hεpos]
      simp [this]

end Research.Operators.Sign.Preservation
