import Research.Operators.Projection.FeasibleId
namespace Research.Operators.ProjectionL1Ball.Preservation
open Research.Operators.Projection.FeasibleId
/- STATEMENT_BEGIN -/
def ProjectionL1BallIdentityProp : Prop := FeasibleBallIdentityProp
def ProjectionL1BallSharpnessProp : Prop := FeasibleBallSharpnessProp
/- STATEMENT_END -/
theorem projection_l1_ball_feasible_ball_identity : ProjectionL1BallIdentityProp := feasible_ball_identity
theorem projection_l1_ball_feasible_ball_sharpness : ProjectionL1BallSharpnessProp := feasible_ball_sharpness
end Research.Operators.ProjectionL1Ball.Preservation
