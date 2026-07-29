from operators.sorting.math import EVALUATION_METHOD, OPERATOR, SHARPNESS_STATEMENT, THEOREM_ID, THEOREM_STATEMENT
from operators.sorting.verify import verify_sorting_margin
def test_verifier():
    claim={"operator":OPERATOR,"theorem_id":THEOREM_ID,"evaluation":EVALUATION_METHOD,"statement":THEOREM_STATEMENT,"sharpness_statement":SHARPNESS_STATEMENT}
    vr=verify_sorting_margin(claim); assert vr.ok,(vr.detail,vr.counterexamples)
