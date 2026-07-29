import Research.Operators.Projection.FeasibleId
namespace Research.Operators.ProjectionL2Ball.Preservation
open Research.Operators.Projection.FeasibleId
/- STATEMENT_BEGIN -/
def ProjectionL2BallIdentityProp : Prop := FeasibleBallIdentityProp
def ProjectionL2BallSharpnessProp : Prop := FeasibleBallSharpnessProp
/- STATEMENT_END -/
theorem projection_l2_ball_feasible_ball_identity : ProjectionL2BallIdentityProp := feasible_ball_identity
theorem projection_l2_ball_feasible_ball_sharpness : ProjectionL2BallSharpnessProp := feasible_ball_sharpness
end Research.Operators.ProjectionL2Ball.Preservation
