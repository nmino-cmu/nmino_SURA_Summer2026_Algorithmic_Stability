import Research.Operators.Argmax.Margin
namespace Research.Operators.TournamentWinner.Margin
open Research.Operators.Argmax.Margin
/- STATEMENT_BEGIN -/
def TournamentWinnerMarginInvarianceProp : Prop := MarginInvarianceProp
def TournamentWinnerMarginSharpnessProp : Prop := MarginSharpnessProp
/- STATEMENT_END -/
theorem tournament_winner_margin_invariance : TournamentWinnerMarginInvarianceProp := margin_invariance
theorem tournament_winner_margin_sharpness : TournamentWinnerMarginSharpnessProp := margin_sharpness
end Research.Operators.TournamentWinner.Margin
