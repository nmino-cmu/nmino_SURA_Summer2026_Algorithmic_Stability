import Research.Operators.OrderStat.KthMargin

namespace Research.Operators.KthOrderStatistic.Preservation

open Research.Operators.OrderStat.KthMargin

/- STATEMENT_BEGIN -/
def KthOrderStatisticMarginInvarianceProp : Prop := KthMarginInvarianceProp
def KthOrderStatisticMarginSharpnessProp : Prop := KthMarginSharpnessProp
/- STATEMENT_END -/

theorem kth_order_statistic_margin_invariance : KthOrderStatisticMarginInvarianceProp := kth_margin_invariance
theorem kth_order_statistic_margin_sharpness : KthOrderStatisticMarginSharpnessProp := kth_margin_sharpness

end Research.Operators.KthOrderStatistic.Preservation
