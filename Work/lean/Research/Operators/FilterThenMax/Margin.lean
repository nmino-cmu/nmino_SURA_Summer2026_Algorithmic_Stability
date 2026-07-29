import Research.Operators.Argmax.Margin
namespace Research.Operators.FilterThenMax.Margin
open Research.Operators.Argmax.Margin
/- STATEMENT_BEGIN -/
def FilterThenMaxMarginInvarianceProp : Prop := MarginInvarianceProp
def FilterThenMaxMarginSharpnessProp : Prop := MarginSharpnessProp
/- STATEMENT_END -/
theorem filter_then_max_margin_invariance : FilterThenMaxMarginInvarianceProp := margin_invariance
theorem filter_then_max_margin_sharpness : FilterThenMaxMarginSharpnessProp := margin_sharpness
end Research.Operators.FilterThenMax.Margin
