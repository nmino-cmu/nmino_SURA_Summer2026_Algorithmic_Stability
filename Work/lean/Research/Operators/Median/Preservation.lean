import Research.Operators.OrderStat.KthMargin

namespace Research.Operators.Median.Preservation

open Research.Operators.OrderStat.KthMargin

/- STATEMENT_BEGIN -/
def MedianMarginInvarianceProp : Prop := KthMarginInvarianceProp
def MedianMarginSharpnessProp : Prop := KthMarginSharpnessProp
/- STATEMENT_END -/

theorem median_margin_invariance : MedianMarginInvarianceProp := kth_margin_invariance
theorem median_margin_sharpness : MedianMarginSharpnessProp := kth_margin_sharpness

end Research.Operators.Median.Preservation
