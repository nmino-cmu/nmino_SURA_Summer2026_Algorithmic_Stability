import Research.Operators.Argmax.Margin
namespace Research.Operators.PenalizedScoreSelection.Margin
open Research.Operators.Argmax.Margin
/- STATEMENT_BEGIN -/
def PenalizedScoreSelectionMarginInvarianceProp : Prop := MarginInvarianceProp
def PenalizedScoreSelectionMarginSharpnessProp : Prop := MarginSharpnessProp
/- STATEMENT_END -/
theorem penalized_score_selection_margin_invariance : PenalizedScoreSelectionMarginInvarianceProp := margin_invariance
theorem penalized_score_selection_margin_sharpness : PenalizedScoreSelectionMarginSharpnessProp := margin_sharpness
end Research.Operators.PenalizedScoreSelection.Margin
