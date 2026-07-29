import Research.Operators.OrderStat.Ranking
namespace Research.Operators.BeamPruning.Preservation
open Research.Operators.OrderStat.Ranking
/- STATEMENT_BEGIN -/
def BeamPruningMarginInvarianceProp : Prop := RankingInvarianceProp
def BeamPruningMarginSharpnessProp : Prop := RankingSharpnessProp
/- STATEMENT_END -/
theorem beam_pruning_margin_invariance : BeamPruningMarginInvarianceProp := ranking_invariance
theorem beam_pruning_margin_sharpness : BeamPruningMarginSharpnessProp := ranking_sharpness
end Research.Operators.BeamPruning.Preservation
