import Research.Operators.Argmax.Margin
namespace Research.Operators.PriorityQueueMaximum.Margin
open Research.Operators.Argmax.Margin
/- STATEMENT_BEGIN -/
def PriorityQueueMaximumMarginInvarianceProp : Prop := MarginInvarianceProp
def PriorityQueueMaximumMarginSharpnessProp : Prop := MarginSharpnessProp
/- STATEMENT_END -/
theorem priority_queue_maximum_margin_invariance : PriorityQueueMaximumMarginInvarianceProp := margin_invariance
theorem priority_queue_maximum_margin_sharpness : PriorityQueueMaximumMarginSharpnessProp := margin_sharpness
end Research.Operators.PriorityQueueMaximum.Margin
