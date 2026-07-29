from operators.bucket_assignment.math import EVALUATION_METHOD, OPERATOR, SHARPNESS_STATEMENT, THEOREM_ID, THEOREM_STATEMENT
from operators.bucket_assignment.verify import verify_bucket_assignment_margin
def test_verifier():
    claim={"operator":OPERATOR,"theorem_id":THEOREM_ID,"evaluation":EVALUATION_METHOD,"statement":THEOREM_STATEMENT,"sharpness_statement":SHARPNESS_STATEMENT}
    vr=verify_bucket_assignment_margin(claim); assert vr.ok,(vr.detail,vr.counterexamples)
