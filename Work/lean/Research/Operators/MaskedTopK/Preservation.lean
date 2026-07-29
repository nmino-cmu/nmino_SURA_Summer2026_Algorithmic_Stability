import Research.Operators.OrderStat.Ranking
namespace Research.Operators.MaskedTopK.Preservation
open Research.Operators.OrderStat.Ranking
/- STATEMENT_BEGIN -/
def MaskedTopKMarginInvarianceProp : Prop := RankingInvarianceProp
def MaskedTopKMarginSharpnessProp : Prop := RankingSharpnessProp
/- STATEMENT_END -/
theorem masked_top_k_margin_invariance : MaskedTopKMarginInvarianceProp := ranking_invariance
theorem masked_top_k_margin_sharpness : MaskedTopKMarginSharpnessProp := ranking_sharpness
end Research.Operators.MaskedTopK.Preservation
