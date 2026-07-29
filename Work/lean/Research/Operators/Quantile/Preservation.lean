import Research.Operators.OrderStat.KthMargin

namespace Research.Operators.Quantile.Preservation

open Research.Operators.OrderStat.KthMargin

/- STATEMENT_BEGIN -/
/-- Quantile index selection is the strict k-th order statistic; stability is the
pairwise-gap margin theorem (`AllGapsExceed s (2ε)`). -/
def QuantileMarginInvarianceProp : Prop := KthMarginInvarianceProp

def QuantileMarginSharpnessProp : Prop := KthMarginSharpnessProp
/- STATEMENT_END -/

theorem quantile_margin_invariance : QuantileMarginInvarianceProp := kth_margin_invariance
theorem quantile_margin_sharpness : QuantileMarginSharpnessProp := kth_margin_sharpness

end Research.Operators.Quantile.Preservation
