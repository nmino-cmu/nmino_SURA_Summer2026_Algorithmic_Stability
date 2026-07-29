import Research.Operators.OrderStat.Ranking
namespace Research.Operators.MultiCriteriaLexicographic.Preservation
open Research.Operators.OrderStat.Ranking
/- STATEMENT_BEGIN -/
def MultiCriteriaLexicographicMarginInvarianceProp : Prop := RankingInvarianceProp
def MultiCriteriaLexicographicMarginSharpnessProp : Prop := RankingSharpnessProp
/- STATEMENT_END -/
theorem multi_criteria_lexicographic_margin_invariance : MultiCriteriaLexicographicMarginInvarianceProp := ranking_invariance
theorem multi_criteria_lexicographic_margin_sharpness : MultiCriteriaLexicographicMarginSharpnessProp := ranking_sharpness
end Research.Operators.MultiCriteriaLexicographic.Preservation
