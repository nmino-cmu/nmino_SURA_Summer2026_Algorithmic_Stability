import Research.Operators.OrderStat.Ranking
namespace Research.Operators.StableSorting.Preservation
open Research.Operators.OrderStat.Ranking
/- STATEMENT_BEGIN -/
def StableSortingMarginInvarianceProp : Prop := RankingInvarianceProp
def StableSortingMarginSharpnessProp : Prop := RankingSharpnessProp
/- STATEMENT_END -/
theorem stable_sorting_margin_invariance : StableSortingMarginInvarianceProp := ranking_invariance
theorem stable_sorting_margin_sharpness : StableSortingMarginSharpnessProp := ranking_sharpness
end Research.Operators.StableSorting.Preservation
