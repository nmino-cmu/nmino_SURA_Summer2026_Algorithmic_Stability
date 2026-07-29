import Research.Operators.Argmax.Margin
namespace Research.Operators.WeightedScoreSelection.Margin
open Research.Operators.Argmax.Margin
/- STATEMENT_BEGIN -/
def WeightedScoreSelectionMarginInvarianceProp : Prop := MarginInvarianceProp
def WeightedScoreSelectionMarginSharpnessProp : Prop := MarginSharpnessProp
/- STATEMENT_END -/
theorem weighted_score_selection_margin_invariance : WeightedScoreSelectionMarginInvarianceProp := margin_invariance
theorem weighted_score_selection_margin_sharpness : WeightedScoreSelectionMarginSharpnessProp := margin_sharpness
end Research.Operators.WeightedScoreSelection.Margin
