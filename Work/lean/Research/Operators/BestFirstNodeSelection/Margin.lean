import Research.Operators.Argmax.Margin
namespace Research.Operators.BestFirstNodeSelection.Margin
open Research.Operators.Argmax.Margin
/- STATEMENT_BEGIN -/
def BestFirstNodeSelectionMarginInvarianceProp : Prop := MarginInvarianceProp
def BestFirstNodeSelectionMarginSharpnessProp : Prop := MarginSharpnessProp
/- STATEMENT_END -/
theorem best_first_node_selection_margin_invariance : BestFirstNodeSelectionMarginInvarianceProp := margin_invariance
theorem best_first_node_selection_margin_sharpness : BestFirstNodeSelectionMarginSharpnessProp := margin_sharpness
end Research.Operators.BestFirstNodeSelection.Margin
