import Research.Operators.Argmax.Margin
namespace Research.Operators.HeapTop.Margin
open Research.Operators.Argmax.Margin
/- STATEMENT_BEGIN -/
def HeapTopMarginInvarianceProp : Prop := MarginInvarianceProp
def HeapTopMarginSharpnessProp : Prop := MarginSharpnessProp
/- STATEMENT_END -/
theorem heap_top_margin_invariance : HeapTopMarginInvarianceProp := margin_invariance
theorem heap_top_margin_sharpness : HeapTopMarginSharpnessProp := margin_sharpness
end Research.Operators.HeapTop.Margin
