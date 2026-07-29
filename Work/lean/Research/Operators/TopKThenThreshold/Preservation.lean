import Research.Operators.OrderStat.Ranking
namespace Research.Operators.TopKThenThreshold.Preservation
open Research.Operators.OrderStat.Ranking
/- STATEMENT_BEGIN -/
def TopKThenThresholdMarginInvarianceProp : Prop := RankingInvarianceProp
def TopKThenThresholdMarginSharpnessProp : Prop := RankingSharpnessProp
/- STATEMENT_END -/
theorem top_k_then_threshold_margin_invariance : TopKThenThresholdMarginInvarianceProp := ranking_invariance
theorem top_k_then_threshold_margin_sharpness : TopKThenThresholdMarginSharpnessProp := ranking_sharpness
end Research.Operators.TopKThenThreshold.Preservation
