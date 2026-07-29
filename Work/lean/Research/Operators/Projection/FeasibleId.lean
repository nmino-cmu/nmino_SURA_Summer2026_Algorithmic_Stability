import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Linarith
import Research.Operators.Argmax.Basic

namespace Research.Operators.Projection.FeasibleId

open Research.Operators.Argmax.Basic

/- STATEMENT_BEGIN -/
/--
If a projector fixes every feasible point, and the closed `ε`-ball about `x`
lies entirely in the feasible set, then every `x'` in that ball is fixed.
-/
def FeasibleBallIdentityProp : Prop :=
  ∀ (x ε : ℝ) (InSet : ℝ → Prop) (proj : ℝ → ℝ),
    0 ≤ ε →
    (∀ z : ℝ, InSet z → proj z = z) →
    (∀ y : ℝ, |y - x| ≤ ε → InSet y) →
    ∀ x' : ℝ, |x' - x| ≤ ε → proj x' = x' ∧ proj x = x

def FeasibleBallSharpnessProp : Prop :=
  ∀ (x ε : ℝ) (InSet : ℝ → Prop),
    0 ≤ ε →
    (∃ y : ℝ, |y - x| ≤ ε ∧ ¬ InSet y) →
    ¬ (∀ y : ℝ, |y - x| ≤ ε → InSet y)
/- STATEMENT_END -/

theorem feasible_ball_identity : FeasibleBallIdentityProp := by
  intro x ε InSet proj hε hfix hball x' hx'
  refine And.intro ?_ ?_
  · exact hfix x' (hball x' hx')
  · have hx0 : |x - x| ≤ ε := by simpa [sub_self, abs_zero] using hε
    exact hfix x (hball x hx0)

theorem feasible_ball_sharpness : FeasibleBallSharpnessProp := by
  intro x ε InSet _hε ⟨y, hyball, hyout⟩ hball
  exact hyout (hball y hyball)

end Research.Operators.Projection.FeasibleId
