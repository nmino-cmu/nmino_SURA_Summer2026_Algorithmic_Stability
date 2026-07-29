import Research.Operators.Projection.Clamp
namespace Research.Operators.ProjectionBox.Preservation
open Research.Operators.Projection.Clamp
/- STATEMENT_BEGIN -/
def ProjectionBoxStabilityProp : Prop := ClampStabilityProp
def ProjectionBoxSharpnessProp : Prop := ClampSharpnessProp
/- STATEMENT_END -/
theorem projection_box_clamp_stability : ProjectionBoxStabilityProp := clamp_stability
theorem projection_box_clamp_sharpness : ProjectionBoxSharpnessProp := clamp_sharpness
end Research.Operators.ProjectionBox.Preservation
