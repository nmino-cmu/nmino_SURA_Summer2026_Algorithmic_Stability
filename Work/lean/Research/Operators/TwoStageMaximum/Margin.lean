import Research.Operators.Argmax.Margin
namespace Research.Operators.TwoStageMaximum.Margin
open Research.Operators.Argmax.Margin
/- STATEMENT_BEGIN -/
def TwoStageMaximumMarginInvarianceProp : Prop := MarginInvarianceProp
def TwoStageMaximumMarginSharpnessProp : Prop := MarginSharpnessProp
/- STATEMENT_END -/
theorem two_stage_maximum_margin_invariance : TwoStageMaximumMarginInvarianceProp := margin_invariance
theorem two_stage_maximum_margin_sharpness : TwoStageMaximumMarginSharpnessProp := margin_sharpness
end Research.Operators.TwoStageMaximum.Margin
