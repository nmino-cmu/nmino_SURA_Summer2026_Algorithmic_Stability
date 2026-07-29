
import Research.Operators.OrderStat.Ranking
namespace Research.Operators.TopK.Preservation
open Research.Operators.OrderStat.Ranking
/- STATEMENT_BEGIN -/
def TopKMarginInvarianceProp : Prop := RankingInvarianceProp
def TopKMarginSharpnessProp : Prop := RankingSharpnessProp
/- STATEMENT_END -/
theorem top_k_margin_invariance : TopKMarginInvarianceProp := ranking_invariance
theorem top_k_margin_sharpness : TopKMarginSharpnessProp := ranking_sharpness
end Research.Operators.TopK.Preservation
