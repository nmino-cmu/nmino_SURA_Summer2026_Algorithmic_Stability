"""LLM repair splice guards."""

import pytest

from system_b.lean.llm_repair import ProofBodyRepair


def test_refuse_propose():
    with pytest.raises(NotImplementedError):
        ProofBodyRepair().propose_proof_body("P", "sorry", "err")


def test_splice_rejects_statement_markers():
    src = "theorem t : True := by\n  trivial\n"
    with pytest.raises(ValueError):
        ProofBodyRepair().splice_proof_body(src, "t", "/- STATEMENT_BEGIN -/\ntrivial")
