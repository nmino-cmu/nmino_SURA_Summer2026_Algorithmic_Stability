import Research.Operators.Argmax.Margin
namespace Research.Operators.LexicographicBestFirst.Margin
open Research.Operators.Argmax.Margin
/- STATEMENT_BEGIN -/
def LexicographicBestFirstMarginInvarianceProp : Prop := MarginInvarianceProp
def LexicographicBestFirstMarginSharpnessProp : Prop := MarginSharpnessProp
/- STATEMENT_END -/
theorem lexicographic_best_first_margin_invariance : LexicographicBestFirstMarginInvarianceProp := margin_invariance
theorem lexicographic_best_first_margin_sharpness : LexicographicBestFirstMarginSharpnessProp := margin_sharpness
end Research.Operators.LexicographicBestFirst.Margin
