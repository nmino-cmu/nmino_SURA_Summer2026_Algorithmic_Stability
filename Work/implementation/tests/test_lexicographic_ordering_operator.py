from operators.lexicographic_ordering.math import EVALUATION_METHOD, OPERATOR, SHARPNESS_STATEMENT, THEOREM_ID, THEOREM_STATEMENT
from operators.lexicographic_ordering.verify import verify_lexicographic_ordering_margin
def test_verifier():
    claim={"operator":OPERATOR,"theorem_id":THEOREM_ID,"evaluation":EVALUATION_METHOD,"statement":THEOREM_STATEMENT,"sharpness_statement":SHARPNESS_STATEMENT}
    vr=verify_lexicographic_ordering_margin(claim); assert vr.ok,(vr.detail,vr.counterexamples)
