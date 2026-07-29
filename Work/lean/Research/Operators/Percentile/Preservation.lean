import Research.Operators.OrderStat.KthMargin

namespace Research.Operators.Percentile.Preservation

open Research.Operators.OrderStat.KthMargin

/- STATEMENT_BEGIN -/
def PercentileMarginInvarianceProp : Prop := KthMarginInvarianceProp
def PercentileMarginSharpnessProp : Prop := KthMarginSharpnessProp
/- STATEMENT_END -/

theorem percentile_margin_invariance : PercentileMarginInvarianceProp := kth_margin_invariance
theorem percentile_margin_sharpness : PercentileMarginSharpnessProp := kth_margin_sharpness

end Research.Operators.Percentile.Preservation
