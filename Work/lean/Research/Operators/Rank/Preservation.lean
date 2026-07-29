import Research.Operators.OrderStat.Ranking
namespace Research.Operators.Rank.Preservation
open Research.Operators.OrderStat.Ranking
/- STATEMENT_BEGIN -/
def RankMarginInvarianceProp : Prop := RankingInvarianceProp
def RankMarginSharpnessProp : Prop := RankingSharpnessProp
/- STATEMENT_END -/
theorem rank_margin_invariance : RankMarginInvarianceProp := ranking_invariance
theorem rank_margin_sharpness : RankMarginSharpnessProp := ranking_sharpness
end Research.Operators.Rank.Preservation
