import Research.Operators.OrderStat.Ranking
namespace Research.Operators.BucketAssignment.Preservation
open Research.Operators.OrderStat.Ranking
/- STATEMENT_BEGIN -/
def BucketAssignmentMarginInvarianceProp : Prop := RankingInvarianceProp
def BucketAssignmentMarginSharpnessProp : Prop := RankingSharpnessProp
/- STATEMENT_END -/
theorem bucket_assignment_margin_invariance : BucketAssignmentMarginInvarianceProp := ranking_invariance
theorem bucket_assignment_margin_sharpness : BucketAssignmentMarginSharpnessProp := ranking_sharpness
end Research.Operators.BucketAssignment.Preservation
