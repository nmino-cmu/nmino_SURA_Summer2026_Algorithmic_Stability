import Mathlib.Data.Real.Basic
import Research.Operators.OrderStat.Basic
import Research.Operators.OrderStat.KthMargin
import Research.Operators.Argmax.Basic

namespace Research.Operators.OrderStat.Ranking

open Research.Operators.OrderStat.Basic
open Research.Operators.OrderStat.KthMargin
open Research.Operators.Argmax.Basic

/- STATEMENT_BEGIN -/
/-- Full pairwise ranking is preserved when every pairwise gap exceeds `2ε`. -/
def RankingInvarianceProp : Prop :=
  ∀ (n : Nat) (_hn : 2 ≤ n) (s : Fin n → ℝ) (ε : ℝ),
    0 ≤ ε →
    AllGapsExceed s (2 * ε) →
    ∀ δ : Fin n → ℝ, LinfBall δ ε →
      ∀ i j : Fin n, s i < s j ↔ s i + δ i < s j + δ j

/-- If some pairwise gap is at most `2ε`, an adversary can force a value collision. -/
def RankingSharpnessProp : Prop :=
  ∀ (n : Nat) (_hn : 2 ≤ n) (s : Fin n → ℝ) (ε : ℝ),
    0 ≤ ε →
    (∃ i j : Fin n, i ≠ j ∧ |s i - s j| ≤ 2 * ε) →
    ∃ δ : Fin n → ℝ, LinfBall δ ε ∧
      ∃ i j : Fin n, i ≠ j ∧ s i + δ i = s j + δ j
/- STATEMENT_END -/

theorem ranking_invariance : RankingInvarianceProp := by
  intro n _hn s ε hε hgaps δ hball i j
  by_cases h : i = j
  · subst h; constructor <;> intro hlt <;> linarith
  · exact pairwise_lt_iff s δ ε i j hε hball h (hgaps i j h)

theorem ranking_sharpness : RankingSharpnessProp := by
  intro n _hn s ε hε ⟨i, j, hne, hgap⟩
  have hne' : j ≠ i := Ne.symm hne
  refine ⟨tieDelta i j s, tieDelta_in_ball i j ε s hε hgap, i, j, hne, ?_⟩
  exact tieDelta_ties i j s hne'

end Research.Operators.OrderStat.Ranking
