import Research.Operators.Argmax.Margin
namespace Research.Operators.WeightedTournamentWinner.Margin
open Research.Operators.Argmax.Margin
/- STATEMENT_BEGIN -/
def WeightedTournamentWinnerMarginInvarianceProp : Prop := MarginInvarianceProp
def WeightedTournamentWinnerMarginSharpnessProp : Prop := MarginSharpnessProp
/- STATEMENT_END -/
theorem weighted_tournament_winner_margin_invariance : WeightedTournamentWinnerMarginInvarianceProp := margin_invariance
theorem weighted_tournament_winner_margin_sharpness : WeightedTournamentWinnerMarginSharpnessProp := margin_sharpness
end Research.Operators.WeightedTournamentWinner.Margin
