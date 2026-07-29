import Research.Operators.OrderStat.Ranking
namespace Research.Operators.PartialSorting.Preservation
open Research.Operators.OrderStat.Ranking
/- STATEMENT_BEGIN -/
def PartialSortingMarginInvarianceProp : Prop := RankingInvarianceProp
def PartialSortingMarginSharpnessProp : Prop := RankingSharpnessProp
/- STATEMENT_END -/
theorem partial_sorting_margin_invariance : PartialSortingMarginInvarianceProp := ranking_invariance
theorem partial_sorting_margin_sharpness : PartialSortingMarginSharpnessProp := ranking_sharpness
end Research.Operators.PartialSorting.Preservation
