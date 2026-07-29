import Research.Operators.Argmax.Margin
namespace Research.Operators.GreedyChoiceTieBreak.Margin
open Research.Operators.Argmax.Margin
/- STATEMENT_BEGIN -/
def GreedyChoiceTieBreakMarginInvarianceProp : Prop := MarginInvarianceProp
def GreedyChoiceTieBreakMarginSharpnessProp : Prop := MarginSharpnessProp
/- STATEMENT_END -/
theorem greedy_choice_tie_break_margin_invariance : GreedyChoiceTieBreakMarginInvarianceProp := margin_invariance
theorem greedy_choice_tie_break_margin_sharpness : GreedyChoiceTieBreakMarginSharpnessProp := margin_sharpness
end Research.Operators.GreedyChoiceTieBreak.Margin
