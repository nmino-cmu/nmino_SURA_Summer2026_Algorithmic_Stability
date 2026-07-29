import Research.Operators.Argmax.Margin
namespace Research.Operators.TieBrokenWinner.Margin
open Research.Operators.Argmax.Margin
/- STATEMENT_BEGIN -/
def TieBrokenWinnerMarginInvarianceProp : Prop := MarginInvarianceProp
def TieBrokenWinnerMarginSharpnessProp : Prop := MarginSharpnessProp
/- STATEMENT_END -/
theorem tie_broken_winner_margin_invariance : TieBrokenWinnerMarginInvarianceProp := margin_invariance
theorem tie_broken_winner_margin_sharpness : TieBrokenWinnerMarginSharpnessProp := margin_sharpness
end Research.Operators.TieBrokenWinner.Margin
