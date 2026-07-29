import Research.Operators.OrderStat.BasicInt
import Research.Operators.OrderStat.KthMarginInt
import Research.Operators.Argmax.BasicInt

namespace Research.Operators.OrderStat.RankingInt

open Research.Operators.OrderStat.BasicInt
open Research.Operators.OrderStat.KthMarginInt
open Research.Operators.Argmax.BasicInt

/- STATEMENT_BEGIN -/
/-- Full pairwise ranking is preserved when every pairwise gap exceeds `2ε`. -/
def RankingInvarianceProp : Prop :=
  ∀ (n : Nat) (_hn : 2 ≤ n) (s : Fin n → Int) (ε : Nat),
    AllGapsExceed s (2 * ε) →
    ∀ δ : Fin n → Int, LinfBall δ ε →
      ∀ i j : Fin n, s i < s j ↔ s i + δ i < s j + δ j

/-- If some pairwise gap is at most `2ε`, an adversary can force a value collision. -/
def RankingSharpnessProp : Prop :=
  ∀ (n : Nat) (_hn : 2 ≤ n) (s : Fin n → Int) (ε : Nat),
    (∃ i j : Fin n, i ≠ j ∧ Int.natAbs (s i - s j) ≤ 2 * ε) →
    ∃ δ : Fin n → Int, LinfBall δ ε ∧
      ∃ i j : Fin n, i ≠ j ∧ s i + δ i = s j + δ j
/- STATEMENT_END -/

theorem ranking_invariance : RankingInvarianceProp := by
  intro n _hn s ε hgaps δ hball i j
  by_cases h : i = j
  · subst h; constructor <;> intro hlt <;> omega
  · exact pairwise_lt_iff s δ ε i j hball h (hgaps i j h)

theorem ranking_sharpness : RankingSharpnessProp := by
  intro n _hn s ε ⟨i, j, hne, hgap⟩
  have hne' : j ≠ i := Ne.symm hne
  refine ⟨tieDelta i j ε s, tieDelta_in_ball i j ε s hne' hgap, i, j, hne, ?_⟩
  exact tieDelta_ties i j ε s hne'

end Research.Operators.OrderStat.RankingInt
