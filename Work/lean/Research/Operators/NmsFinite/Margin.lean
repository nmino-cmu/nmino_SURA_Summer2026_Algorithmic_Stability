import Research.Operators.Argmax.Margin
namespace Research.Operators.NmsFinite.Margin
open Research.Operators.Argmax.Margin
/- STATEMENT_BEGIN -/
def NmsFiniteMarginInvarianceProp : Prop := MarginInvarianceProp
def NmsFiniteMarginSharpnessProp : Prop := MarginSharpnessProp
/- STATEMENT_END -/
theorem nms_finite_margin_invariance : NmsFiniteMarginInvarianceProp := margin_invariance
theorem nms_finite_margin_sharpness : NmsFiniteMarginSharpnessProp := margin_sharpness
end Research.Operators.NmsFinite.Margin
