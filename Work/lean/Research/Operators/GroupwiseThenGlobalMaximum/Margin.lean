import Research.Operators.Argmax.Margin
namespace Research.Operators.GroupwiseThenGlobalMaximum.Margin
open Research.Operators.Argmax.Margin
/- STATEMENT_BEGIN -/
def GroupwiseThenGlobalMaximumMarginInvarianceProp : Prop := MarginInvarianceProp
def GroupwiseThenGlobalMaximumMarginSharpnessProp : Prop := MarginSharpnessProp
/- STATEMENT_END -/
theorem groupwise_then_global_maximum_margin_invariance : GroupwiseThenGlobalMaximumMarginInvarianceProp := margin_invariance
theorem groupwise_then_global_maximum_margin_sharpness : GroupwiseThenGlobalMaximumMarginSharpnessProp := margin_sharpness
end Research.Operators.GroupwiseThenGlobalMaximum.Margin
