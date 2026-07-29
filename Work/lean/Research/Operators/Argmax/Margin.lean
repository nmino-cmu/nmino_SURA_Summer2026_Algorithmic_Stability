import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Linarith
import Research.Operators.Argmax.Basic

namespace Research.Operators.Argmax.Margin

open Research.Operators.Argmax.Basic

/- STATEMENT_BEGIN -/
/--
If `i*` is the unique maximizer and every rival gap exceeds `2ε`, then every
`‖δ‖_∞ ≤ ε` perturbation preserves unique maximality of `i*`.
(Equivalent to `γ(s) > 2ε` with `γ = s i* − max_{j≠i*} s j`.)
-/
def MarginInvarianceProp : Prop :=
  ∀ (m : Nat) (_hm : 2 ≤ m) (s : Fin m → ℝ) (ε : ℝ) (iStar : Fin m),
    0 ≤ ε →
    IsUniqueMaximizer s iStar →
    (∀ j : Fin m, j ≠ iStar → s iStar - s j > 2 * ε) →
    ∀ δ : Fin m → ℝ, LinfBall δ ε → IsUniqueMaximizer (fun i => s i + δ i) iStar

/--
If some rival gap is at most `2ε`, an adversarial `δ` in the `ε`-ball destroys
uniqueness of `i*` (sharpness).
-/
def MarginSharpnessProp : Prop :=
  ∀ (m : Nat) (_hm : 2 ≤ m) (s : Fin m → ℝ) (ε : ℝ) (iStar : Fin m),
    0 ≤ ε →
    IsUniqueMaximizer s iStar →
    (∃ j : Fin m, j ≠ iStar ∧ s iStar - s j ≤ 2 * ε) →
    ∃ δ : Fin m → ℝ, LinfBall δ ε ∧ ¬ IsUniqueMaximizer (fun i => s i + δ i) iStar
/- STATEMENT_END -/

/-- Perturbation shrinks pairwise gaps by at most `2ε`. -/
theorem gap_shrinks_by_at_most_two_eps {m : Nat}
    (s δ : Fin m → ℝ) (ε : ℝ) (i j : Fin m)
    (hball : LinfBall δ ε) :
    (s i + δ i) - (s j + δ j) ≥ (s i - s j) - 2 * ε := by
  have hi := (abs_le_iff (δ i) ε).mp (hball i)
  have hj := (abs_le_iff (δ j) ε).mp (hball j)
  linarith

theorem margin_invariance : MarginInvarianceProp := by
  intro m _hm s ε iStar _hε _huniq hgaps δ hball
  refine And.intro ?max ?strict
  · intro j
    change s j + δ j ≤ s iStar + δ iStar
    by_cases h : j = iStar
    · subst h; exact le_rfl
    · have hgap := hgaps j h
      have hshr := gap_shrinks_by_at_most_two_eps s δ ε iStar j hball
      linarith
  · intro j hj
    change s j + δ j < s iStar + δ iStar
    have hgap := hgaps j hj
    have hshr := gap_shrinks_by_at_most_two_eps s δ ε iStar j hball
    linarith

/-- Adversarial perturbation: `-ε` at `i*`, `+ε` at a witness rival. -/
def adversarialDelta {m : Nat} (iStar jStar : Fin m) (ε : ℝ) : Fin m → ℝ :=
  fun i =>
    if i = iStar then -ε
    else if i = jStar then ε
    else 0

theorem adversarialDelta_in_ball {m : Nat} (iStar jStar : Fin m) (ε : ℝ)
    (hε : 0 ≤ ε) :
    LinfBall (adversarialDelta iStar jStar ε) ε := by
  intro i
  dsimp only [adversarialDelta]
  by_cases h1 : i = iStar
  · simp [h1, abs_neg, abs_of_nonneg hε]
  · by_cases h2 : i = jStar
    · have hjne : jStar ≠ iStar := by
        intro heq; exact h1 (h2 ▸ heq)
      simp [h1, h2, hjne, abs_of_nonneg hε]
    · simp [h1, h2, abs_zero, hε]

theorem margin_sharpness : MarginSharpnessProp := by
  intro m _hm s ε iStar hε _huniq ⟨jStar, hjne, hgap⟩
  refine ⟨adversarialDelta iStar jStar ε, adversarialDelta_in_ball iStar jStar ε hε, ?_⟩
  intro huniq'
  have hδi : adversarialDelta iStar jStar ε iStar = -ε := by
    simp [adversarialDelta]
  have hδj : adversarialDelta iStar jStar ε jStar = ε := by
    simp [adversarialDelta, hjne]
  have hstrict :
      s jStar + adversarialDelta iStar jStar ε jStar <
        s iStar + adversarialDelta iStar jStar ε iStar :=
    huniq'.2 jStar hjne
  rw [hδi, hδj] at hstrict
  linarith

end Research.Operators.Argmax.Margin
