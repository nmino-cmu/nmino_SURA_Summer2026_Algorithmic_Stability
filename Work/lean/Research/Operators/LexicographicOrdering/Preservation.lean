import Research.Operators.OrderStat.Ranking
namespace Research.Operators.LexicographicOrdering.Preservation
open Research.Operators.OrderStat.Ranking
/- STATEMENT_BEGIN -/
def LexicographicOrderingMarginInvarianceProp : Prop := RankingInvarianceProp
def LexicographicOrderingMarginSharpnessProp : Prop := RankingSharpnessProp
/- STATEMENT_END -/
theorem lexicographic_ordering_margin_invariance : LexicographicOrderingMarginInvarianceProp := ranking_invariance
theorem lexicographic_ordering_margin_sharpness : LexicographicOrderingMarginSharpnessProp := ranking_sharpness
end Research.Operators.LexicographicOrdering.Preservation
