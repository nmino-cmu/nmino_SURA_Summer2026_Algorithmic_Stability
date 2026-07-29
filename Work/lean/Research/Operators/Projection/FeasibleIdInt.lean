import Research.Operators.Argmax.BasicInt

namespace Research.Operators.Projection.FeasibleIdInt

open Research.Operators.Argmax.BasicInt

/- STATEMENT_BEGIN -/
/--
If a projector fixes every feasible point, and the closed `ε`-ball about `x`
lies entirely in the feasible set, then every `x'` in that ball is fixed and
equals its projection (feasible-ball identity; limited Int-core theorem).
-/
def FeasibleBallIdentityProp : Prop :=
  ∀ (x : Int) (ε : Nat) (InSet : Int → Prop) (proj : Int → Int),
    (∀ z : Int, InSet z → proj z = z) →
    (∀ y : Int, Int.natAbs (y - x) ≤ ε → InSet y) →
    ∀ x' : Int, Int.natAbs (x' - x) ≤ ε → proj x' = x' ∧ proj x = x

/--
Sharpness of the ball hypothesis: if some point in the `ε`-ball is infeasible,
the universal feasible-ball premise fails (witness).
-/
def FeasibleBallSharpnessProp : Prop :=
  ∀ (x : Int) (ε : Nat) (InSet : Int → Prop),
    (∃ y : Int, Int.natAbs (y - x) ≤ ε ∧ ¬ InSet y) →
    ¬ (∀ y : Int, Int.natAbs (y - x) ≤ ε → InSet y)
/- STATEMENT_END -/

theorem feasible_ball_identity : FeasibleBallIdentityProp := by
  intro x ε InSet proj hfix hball x' hx'
  refine And.intro ?_ ?_
  · exact hfix x' (hball x' hx')
  · have hx0 : Int.natAbs (x - x) ≤ ε := by simp
    exact hfix x (hball x hx0)

theorem feasible_ball_sharpness : FeasibleBallSharpnessProp := by
  intro x ε InSet ⟨y, hyball, hyout⟩ hball
  exact hyout (hball y hyball)

end Research.Operators.Projection.FeasibleIdInt
