import Research.Operators.Argmax.Margin
namespace Research.Operators.MaskedMaximum.Margin
open Research.Operators.Argmax.Margin
/- STATEMENT_BEGIN -/
def MaskedMaximumMarginInvarianceProp : Prop := MarginInvarianceProp
def MaskedMaximumMarginSharpnessProp : Prop := MarginSharpnessProp
/- STATEMENT_END -/
theorem masked_maximum_margin_invariance : MaskedMaximumMarginInvarianceProp := margin_invariance
theorem masked_maximum_margin_sharpness : MaskedMaximumMarginSharpnessProp := margin_sharpness
end Research.Operators.MaskedMaximum.Margin
