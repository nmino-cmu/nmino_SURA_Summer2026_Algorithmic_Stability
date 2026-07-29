import Research.Operators.Argmax.BasicInt

namespace Research.Operators.Argmax.MarginInt

open Research.Operators.Argmax.BasicInt

/- STATEMENT_BEGIN -/
/--
If `i*` is the unique maximizer and every rival gap exceeds `2ε`, then every
`‖δ‖_∞ ≤ ε` perturbation preserves unique maximality of `i*`.
(Equivalent to `γ(s) > 2ε` with `γ = s i* − max_{j≠i*} s j`.)
-/
def MarginInvarianceProp : Prop :=
  ∀ (m : Nat) (_hm : 2 ≤ m) (s : Fin m → Int) (ε : Nat) (iStar : Fin m),
    IsUniqueMaximizer s iStar →
    (∀ j : Fin m, j ≠ iStar → s iStar - s j > 2 * (ε : Int)) →
    ∀ δ : Fin m → Int, LinfBall δ ε → IsUniqueMaximizer (fun i => s i + δ i) iStar

/--
If some rival gap is at most `2ε`, an adversarial `δ` in the `ε`-ball destroys
uniqueness of `i*` (sharpness).
-/
def MarginSharpnessProp : Prop :=
  ∀ (m : Nat) (_hm : 2 ≤ m) (s : Fin m → Int) (ε : Nat) (iStar : Fin m),
    IsUniqueMaximizer s iStar →
    (∃ j : Fin m, j ≠ iStar ∧ s iStar - s j ≤ 2 * (ε : Int)) →
    ∃ δ : Fin m → Int, LinfBall δ ε ∧ ¬ IsUniqueMaximizer (fun i => s i + δ i) iStar
/- STATEMENT_END -/

/-- Perturbation shrinks pairwise gaps by at most `2ε`. -/
theorem gap_shrinks_by_at_most_two_eps {m : Nat}
    (s δ : Fin m → Int) (ε : Nat) (i j : Fin m)
    (hball : LinfBall δ ε) :
    (s i + δ i) - (s j + δ j) ≥ (s i - s j) - 2 * (ε : Int) := by
  have hi := (natAbs_le_iff (δ i) ε).mp (hball i)
  have hj := (natAbs_le_iff (δ j) ε).mp (hball j)
  omega

theorem margin_invariance : MarginInvarianceProp := by
  intro m _hm s ε iStar huniq hgaps δ hball
  change IsUniqueMaximizer (fun i => s i + δ i) iStar
  refine And.intro ?max ?strict
  · intro j
    change s j + δ j ≤ s iStar + δ iStar
    by_cases h : j = iStar
    · subst h; omega
    · have hgap : s iStar - s j > 2 * (ε : Int) := hgaps j h
      have hshr := gap_shrinks_by_at_most_two_eps s δ ε iStar j hball
      omega
  · intro j hj
    change s j + δ j < s iStar + δ iStar
    have hgap : s iStar - s j > 2 * (ε : Int) := hgaps j hj
    have hshr := gap_shrinks_by_at_most_two_eps s δ ε iStar j hball
    omega

/-- Adversarial perturbation: `-ε` at `i*`, `+ε` at a witness rival. -/
def adversarialDelta {m : Nat} (iStar jStar : Fin m) (ε : Nat) : Fin m → Int :=
  fun i =>
    if i = iStar then -((ε : Int))
    else if i = jStar then (ε : Int)
    else 0

private theorem natAbs_coe_nat (ε : Nat) : Int.natAbs (ε : Int) = ε := rfl

private theorem natAbs_neg_coe_nat (ε : Nat) : Int.natAbs (-(ε : Int)) = ε := by
  rw [Int.natAbs_neg, natAbs_coe_nat]

theorem adversarialDelta_in_ball {m : Nat} (iStar jStar : Fin m) (ε : Nat) :
    LinfBall (adversarialDelta iStar jStar ε) ε := by
  intro i
  dsimp only [adversarialDelta]
  by_cases h1 : i = iStar
  · simp [h1, natAbs_neg_coe_nat]
  · by_cases h2 : i = jStar
    · have hjne : jStar ≠ iStar := by
        intro heq; exact h1 (h2 ▸ heq)
      simp [h1, h2, hjne, natAbs_coe_nat]
    · simp [h1, h2]

theorem margin_sharpness : MarginSharpnessProp := by
  intro m _hm s ε iStar _huniq ⟨jStar, hjne, hgap⟩
  refine ⟨adversarialDelta iStar jStar ε, adversarialDelta_in_ball iStar jStar ε, ?_⟩
  intro huniq'
  have hδi : adversarialDelta iStar jStar ε iStar = -((ε : Int)) := by
    simp [adversarialDelta]
  have hδj : adversarialDelta iStar jStar ε jStar = (ε : Int) := by
    simp [adversarialDelta, hjne]
  have hstrict : s jStar + adversarialDelta iStar jStar ε jStar
      < s iStar + adversarialDelta iStar jStar ε iStar :=
    huniq'.2 jStar hjne
  rw [hδi, hδj] at hstrict
  omega

end Research.Operators.Argmax.MarginInt
