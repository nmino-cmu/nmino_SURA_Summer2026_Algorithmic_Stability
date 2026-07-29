import Research.Operators.Argmax.Margin
namespace Research.Operators.GreedyMaximumSelection.Margin
open Research.Operators.Argmax.Margin
/- STATEMENT_BEGIN -/
def GreedyMaximumSelectionMarginInvarianceProp : Prop := MarginInvarianceProp
def GreedyMaximumSelectionMarginSharpnessProp : Prop := MarginSharpnessProp
/- STATEMENT_END -/
theorem greedy_maximum_selection_margin_invariance : GreedyMaximumSelectionMarginInvarianceProp := margin_invariance
theorem greedy_maximum_selection_margin_sharpness : GreedyMaximumSelectionMarginSharpnessProp := margin_sharpness
end Research.Operators.GreedyMaximumSelection.Margin
