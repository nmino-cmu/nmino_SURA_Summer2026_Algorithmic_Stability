import Research.Operators.Projection.Clamp
namespace Research.Operators.CoordinateClipping.Preservation
open Research.Operators.Projection.Clamp
/- STATEMENT_BEGIN -/
def CoordinateClippingStabilityProp : Prop := ClampStabilityProp
def CoordinateClippingSharpnessProp : Prop := ClampSharpnessProp
/- STATEMENT_END -/
theorem coordinate_clipping_clamp_stability : CoordinateClippingStabilityProp := clamp_stability
theorem coordinate_clipping_clamp_sharpness : CoordinateClippingSharpnessProp := clamp_sharpness
end Research.Operators.CoordinateClipping.Preservation
