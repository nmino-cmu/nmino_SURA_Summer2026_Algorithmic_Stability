import Research.Operators.Argmax.Margin
namespace Research.Operators.HierarchicalMaximum.Margin
open Research.Operators.Argmax.Margin
/- STATEMENT_BEGIN -/
def HierarchicalMaximumMarginInvarianceProp : Prop := MarginInvarianceProp
def HierarchicalMaximumMarginSharpnessProp : Prop := MarginSharpnessProp
/- STATEMENT_END -/
theorem hierarchical_maximum_margin_invariance : HierarchicalMaximumMarginInvarianceProp := margin_invariance
theorem hierarchical_maximum_margin_sharpness : HierarchicalMaximumMarginSharpnessProp := margin_sharpness
end Research.Operators.HierarchicalMaximum.Margin
