import Research.Operators.OrderStat.Ranking
namespace Research.Operators.Sorting.Preservation
open Research.Operators.OrderStat.Ranking
/- STATEMENT_BEGIN -/
def SortingMarginInvarianceProp : Prop := RankingInvarianceProp
def SortingMarginSharpnessProp : Prop := RankingSharpnessProp
/- STATEMENT_END -/
theorem sorting_margin_invariance : SortingMarginInvarianceProp := ranking_invariance
theorem sorting_margin_sharpness : SortingMarginSharpnessProp := ranking_sharpness
end Research.Operators.Sorting.Preservation
