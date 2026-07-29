import Research.Operators.Projection.FeasibleId
namespace Research.Operators.ProjectionSimplex.Preservation
open Research.Operators.Projection.FeasibleId
/- STATEMENT_BEGIN -/
def ProjectionSimplexIdentityProp : Prop := FeasibleBallIdentityProp
def ProjectionSimplexSharpnessProp : Prop := FeasibleBallSharpnessProp
/- STATEMENT_END -/
theorem projection_simplex_feasible_ball_identity : ProjectionSimplexIdentityProp := feasible_ball_identity
theorem projection_simplex_feasible_ball_sharpness : ProjectionSimplexSharpnessProp := feasible_ball_sharpness
end Research.Operators.ProjectionSimplex.Preservation
