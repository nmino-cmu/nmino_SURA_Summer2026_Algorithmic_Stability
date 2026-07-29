import Research.Operators.Argmax.Margin
namespace Research.Operators.FeasibleSubsetMaximum.Margin
open Research.Operators.Argmax.Margin
/- STATEMENT_BEGIN -/
def FeasibleSubsetMaximumMarginInvarianceProp : Prop := MarginInvarianceProp
def FeasibleSubsetMaximumMarginSharpnessProp : Prop := MarginSharpnessProp
/- STATEMENT_END -/
theorem feasible_subset_maximum_margin_invariance : FeasibleSubsetMaximumMarginInvarianceProp := margin_invariance
theorem feasible_subset_maximum_margin_sharpness : FeasibleSubsetMaximumMarginSharpnessProp := margin_sharpness
end Research.Operators.FeasibleSubsetMaximum.Margin
