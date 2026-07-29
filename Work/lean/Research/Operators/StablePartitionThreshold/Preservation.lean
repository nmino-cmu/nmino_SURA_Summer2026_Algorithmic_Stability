import Research.Operators.OrderStat.Ranking
namespace Research.Operators.StablePartitionThreshold.Preservation
open Research.Operators.OrderStat.Ranking
/- STATEMENT_BEGIN -/
def StablePartitionThresholdMarginInvarianceProp : Prop := RankingInvarianceProp
def StablePartitionThresholdMarginSharpnessProp : Prop := RankingSharpnessProp
/- STATEMENT_END -/
theorem stable_partition_threshold_margin_invariance : StablePartitionThresholdMarginInvarianceProp := ranking_invariance
theorem stable_partition_threshold_margin_sharpness : StablePartitionThresholdMarginSharpnessProp := ranking_sharpness
end Research.Operators.StablePartitionThreshold.Preservation
