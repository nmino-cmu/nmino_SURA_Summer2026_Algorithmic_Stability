
from operators.top_k.math import EVALUATION_METHOD, OPERATOR, SHARPNESS_STATEMENT, THEOREM_ID, THEOREM_STATEMENT, ranking_preserved, top_k_indices
from operators.top_k.verify import verify_top_k_margin
def test_topk():
    assert top_k_indices((1.0,5.0,3.0),2)==(1,2)
    assert ranking_preserved((0.0,3.0,6.0),1.0)
def test_verifier():
    claim={"operator":OPERATOR,"theorem_id":THEOREM_ID,"evaluation":EVALUATION_METHOD,"statement":THEOREM_STATEMENT,"sharpness_statement":SHARPNESS_STATEMENT}
    vr=verify_top_k_margin(claim); assert vr.ok,(vr.detail,vr.counterexamples)
