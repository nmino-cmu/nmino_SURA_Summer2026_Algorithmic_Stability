import Research.Operators.Projection.Clamp
namespace Research.Operators.ProjectionInterval.Preservation
open Research.Operators.Projection.Clamp
/- STATEMENT_BEGIN -/
def ProjectionIntervalStabilityProp : Prop := ClampStabilityProp
def ProjectionIntervalSharpnessProp : Prop := ClampSharpnessProp
/- STATEMENT_END -/
theorem projection_interval_clamp_stability : ProjectionIntervalStabilityProp := clamp_stability
theorem projection_interval_clamp_sharpness : ProjectionIntervalSharpnessProp := clamp_sharpness
end Research.Operators.ProjectionInterval.Preservation
