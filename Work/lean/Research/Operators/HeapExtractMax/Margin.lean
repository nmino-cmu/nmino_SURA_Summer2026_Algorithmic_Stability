import Research.Operators.Argmax.Margin
namespace Research.Operators.HeapExtractMax.Margin
open Research.Operators.Argmax.Margin
/- STATEMENT_BEGIN -/
def HeapExtractMaxMarginInvarianceProp : Prop := MarginInvarianceProp
def HeapExtractMaxMarginSharpnessProp : Prop := MarginSharpnessProp
/- STATEMENT_END -/
theorem heap_extract_max_margin_invariance : HeapExtractMaxMarginInvarianceProp := margin_invariance
theorem heap_extract_max_margin_sharpness : HeapExtractMaxMarginSharpnessProp := margin_sharpness
end Research.Operators.HeapExtractMax.Margin
