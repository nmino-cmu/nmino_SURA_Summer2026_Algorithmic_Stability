import Research.Operators.Projection.FeasibleId
namespace Research.Operators.FeasibilityIndicator.Preservation
open Research.Operators.Projection.FeasibleId
/- STATEMENT_BEGIN -/
def FeasibilityIndicatorIdentityProp : Prop := FeasibleBallIdentityProp
def FeasibilityIndicatorSharpnessProp : Prop := FeasibleBallSharpnessProp
/- STATEMENT_END -/
theorem feasibility_indicator_feasible_ball_identity : FeasibilityIndicatorIdentityProp := feasible_ball_identity
theorem feasibility_indicator_feasible_ball_sharpness : FeasibilityIndicatorSharpnessProp := feasible_ball_sharpness
end Research.Operators.FeasibilityIndicator.Preservation
