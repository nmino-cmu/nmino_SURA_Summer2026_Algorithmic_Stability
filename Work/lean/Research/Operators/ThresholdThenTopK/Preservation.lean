import Research.Operators.OrderStat.Ranking
namespace Research.Operators.ThresholdThenTopK.Preservation
open Research.Operators.OrderStat.Ranking
/- STATEMENT_BEGIN -/
def ThresholdThenTopKMarginInvarianceProp : Prop := RankingInvarianceProp
def ThresholdThenTopKMarginSharpnessProp : Prop := RankingSharpnessProp
/- STATEMENT_END -/
theorem threshold_then_top_k_margin_invariance : ThresholdThenTopKMarginInvarianceProp := ranking_invariance
theorem threshold_then_top_k_margin_sharpness : ThresholdThenTopKMarginSharpnessProp := ranking_sharpness
end Research.Operators.ThresholdThenTopK.Preservation
