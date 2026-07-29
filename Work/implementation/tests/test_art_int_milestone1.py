"""Milestone 1 tests — ART-INT-00 shared integration layer."""

from __future__ import annotations

import pytest

from art_int.batch import SubmissionAttempt, SubmissionBatch, recompute_batch_status
from art_int.canon import H, canonical_serialization, digest_object, normalize_unicode
from art_int.crp import (
    CandidateResearchPackage,
    CrpPayload,
    compute_crp_digest,
    normalize_profile_hint,
    validate_crp_admissibility,
)
from art_int.draft import DraftCRPPayload
from art_int.enums import (
    AuthorKind,
    BatchStatus,
    CrpProfile,
    IntakeStatus,
    TransportResult,
)
from art_int.envelope import SubmissionEnvelope, strip_or_reject_unknown, validate_envelope
from art_int.errors import (
    AdmissibilityError,
    IdempotencyConflict,
    ProvenanceError,
    SchemaVersionError,
    UnknownFieldError,
    UnsupportedEnumError,
)
from art_int.feedback import (
    VerifierFeedbackExport,
    compute_export_digest,
    finalize_export,
    validate_feedback_for_prior,
)
from art_int.idempotency import check_idempotency_replay
from art_int.mechanism import apply_perturbation_mechanism_alias
from art_int.receipt import IntakeReceipt, compute_receipt_digest
from art_int.seal import seal_draft


SCOPE = "a" * 64
PRINCIPAL = "b" * 64
BINDING = "c" * 64


def _phase_a_payload(**kw) -> CrpPayload:
    claims = kw.pop("claims", [{"chain_segment": "characterization", "kind": "instability"}])
    return CrpPayload(claims=claims, **kw)


def _make_crp(profile=CrpProfile.PHASE_A_CHARACTERIZATION, **kw) -> CandidateResearchPackage:
    payload = kw.pop("payload", _phase_a_payload())
    crp = CandidateResearchPackage(
        author_kind=kw.pop("author_kind", AuthorKind.HUMAN),
        author_principal_digest=PRINCIPAL,
        author_binding_digest=kw.pop("author_binding_digest", None),
        profile=profile,
        math_scope_pin_digest=SCOPE,
        payload=payload,
        sealed_at="2026-07-25T12:00:00Z",
        prior_crp_digest=kw.pop("prior_crp_digest", None),
    )
    crp.crp_digest = compute_crp_digest(crp)
    return crp


def test_canonical_round_trip_and_digest_stability():
    obj = {"z": 1, "a": {"y": 2, "b": 3}, "list": [1, 2]}
    b1 = canonical_serialization(obj)
    b2 = canonical_serialization({"list": [1, 2], "a": {"b": 3, "y": 2}, "z": 1})
    assert b1 == b2
    assert digest_object(obj) == digest_object({"z": 1, "list": [1, 2], "a": {"y": 2, "b": 3}})


def test_same_content_same_digest_changed_differs():
    a = _make_crp()
    b = _make_crp()
    assert a.crp_digest == b.crp_digest
    c = _make_crp(payload=_phase_a_payload(claims=[{"chain_segment": "characterization", "kind": "other"}]))
    assert a.crp_digest != c.crp_digest


def test_omit_null_not_serialized():
    raw = canonical_serialization({"a": 1, "b": None})
    assert b'"b"' not in raw


def test_null_raises():
    with pytest.raises(ValueError):
        canonical_serialization(None)


def test_unicode_nfc():
    # café composed vs decomposed
    c1 = "caf\u00e9"
    c2 = "cafe\u0301"
    assert normalize_unicode(c1) == normalize_unicode(c2)
    assert H(canonical_serialization({"t": c1})) == H(canonical_serialization({"t": c2}))


def test_idempotency_replay_same_key_same_digest():
    d = "ab" * 32
    assert check_idempotency_replay(
        idempotency_key=d, incoming_digest=d, prior_key=d, prior_digest=d
    ) == "replay"


def test_idempotency_same_key_different_digest_rejected():
    with pytest.raises(IdempotencyConflict):
        check_idempotency_replay(
            idempotency_key="aa" * 32,
            incoming_digest="aa" * 32,
            prior_key="aa" * 32,
            prior_digest="bb" * 32,
        )


def test_unknown_schema_version_rejected():
    crp = _make_crp()
    crp.schema_version = "ARTCRP.v999"
    with pytest.raises(SchemaVersionError):
        validate_crp_admissibility(crp, live_scope_pin=SCOPE)


def test_unsupported_profile_hint():
    with pytest.raises(UnsupportedEnumError):
        normalize_profile_hint("NOT_A_PROFILE")


def test_profile_alias_mapping():
    assert normalize_profile_hint("PHASE_A") == CrpProfile.PHASE_A_CHARACTERIZATION
    assert normalize_profile_hint("PHASE_B") == CrpProfile.PHASE_B_STABILIZATION


def test_phase_b_missing_mechanism():
    crp = _make_crp(profile=CrpProfile.PHASE_B_STABILIZATION)
    with pytest.raises(AdmissibilityError) as e:
        validate_crp_admissibility(crp, live_scope_pin=SCOPE)
    assert e.value.code == "MECHANISM_REQUIRED"


def test_phase_a_empty_mechanism_ok():
    crp = _make_crp()
    validate_crp_admissibility(crp, live_scope_pin=SCOPE)


def test_assistant_requires_binding():
    crp = _make_crp(author_kind=AuthorKind.RESEARCH_DISCOVERY_ASSISTANT)
    with pytest.raises(AdmissibilityError) as e:
        validate_crp_admissibility(crp, live_scope_pin=SCOPE, assistant_binding_live=True)
    assert e.value.code == "CRP_AUTHOR"


def test_mechanism_alias():
    p = _phase_a_payload()
    apply_perturbation_mechanism_alias(p, perturbation_mechanism_id="mech-1", mechanism_body={"kind": "Qpsi"})
    assert any(m.get("local_id") == "mech-1" for m in p.mechanism_proposals)
    apply_perturbation_mechanism_alias(p, perturbation_mechanism_id=None)
    assert len(p.mechanism_proposals) == 1


def test_seal_digest_equals_crp_digest():
    draft = DraftCRPPayload(
        branch_id="br1",
        profile_hint="PHASE_A_CHARACTERIZATION",
        math_scope_pin_digest=SCOPE,
        tip_pins=["t1"],
        dep_closure_digest="d" * 64,
        payload=_phase_a_payload(),
        created_at="2026-07-25T12:00:00Z",
    )
    snap = seal_draft(
        draft,
        draft_crp_version_id="draft1",
        gate_record_id="g3",
        sealed_at="2026-07-25T12:00:00Z",
        author_kind=AuthorKind.HUMAN,
        author_principal_digest=PRINCIPAL,
        author_binding_digest=None,
        live_scope_pin=SCOPE,
    )
    assert snap.sealed_digest == snap.crp.crp_digest == compute_crp_digest(snap.crp)


def test_envelope_idempotency_key():
    crp = _make_crp()
    env = SubmissionEnvelope(crp=crp, idempotency_key=crp.crp_digest, a_batch_id="batch-1")
    validate_envelope(env)
    assert "a_batch_id" in env.to_wire()  # telemetry allowed on wire from A
    with pytest.raises(UnknownFieldError):
        strip_or_reject_unknown({"schema_version": "ARTINT.ENV.v1", "crp": {}, "idempotency_key": "x", "evil": 1})
    cleaned = strip_or_reject_unknown(
        {"schema_version": "ARTINT.ENV.v1", "crp": {}, "idempotency_key": "x", "a_extra_tele": "y"}
    )
    assert "a_extra_tele" not in cleaned


def test_batch_cardinality_fan_out():
    batch = SubmissionBatch(
        batch_id="B1", session_id="S1", gate_record_id="G1", seal_set=["d1", "d2"]
    )
    attempts = [
        SubmissionAttempt(
            attempt_id="a1",
            batch_id="B1",
            session_id="S1",
            sealed_snapshot_version_id="s1",
            sealed_digest="11" * 32,
            idempotency_key="11" * 32,
            logical_submission_id="11" * 32,
            b_intake_result=IntakeStatus.ACCEPTED_DRAFT,
        ),
        SubmissionAttempt(
            attempt_id="a2",
            batch_id="B1",
            session_id="S1",
            sealed_snapshot_version_id="s2",
            sealed_digest="22" * 32,
            idempotency_key="22" * 32,
            logical_submission_id="22" * 32,
            b_intake_result=IntakeStatus.REJECTED,
        ),
    ]
    digests = batch.fan_out_digests(attempts)
    assert len(digests) == 2
    assert recompute_batch_status(attempts) == BatchStatus.COMPLETED_MIXED


def test_receipt_digest_sorted_claims():
    r = IntakeReceipt(
        crp_digest="aa" * 32,
        event_seq=1,
        draft_claim_digests=["c2", "c1"],
        status=IntakeStatus.ACCEPTED_DRAFT,
        obligation_digests=["o1"],
    )
    d1 = compute_receipt_digest(r)
    r2 = IntakeReceipt(
        crp_digest="aa" * 32,
        event_seq=1,
        draft_claim_digests=["c1", "c2"],
        status=IntakeStatus.ACCEPTED_DRAFT,
    )
    assert compute_receipt_digest(r2) == d1


def test_feedback_provenance_and_forged_receipt():
    fb = VerifierFeedbackExport(
        crp_digest="aa" * 32,
        sealed_digest="aa" * 32,
        intake_status=IntakeStatus.ACCEPTED_DRAFT,
        profile=CrpProfile.PHASE_A_CHARACTERIZATION.value,
        receipt_digest="rr" * 32,
    )
    finalize_export(fb)
    validate_feedback_for_prior(fb, expected_crp_digest="aa" * 32, expected_receipt="rr" * 32)
    with pytest.raises(ProvenanceError):
        validate_feedback_for_prior(fb, expected_crp_digest="bb" * 32)
    with pytest.raises(ProvenanceError):
        validate_feedback_for_prior(fb, expected_receipt="ff" * 32)
    bad = VerifierFeedbackExport(
        crp_digest="aa" * 32,
        sealed_digest="bb" * 32,
        intake_status=IntakeStatus.ACCEPTED_DRAFT,
        profile="PHASE_A_CHARACTERIZATION",
    )
    with pytest.raises(ProvenanceError):
        finalize_export(bad)


def test_transport_enum():
    assert TransportResult.EXHAUSTED.value == "EXHAUSTED"


def test_validate_seal_rejects_embedded_digest_mismatch():
    draft = DraftCRPPayload(
        branch_id="br1",
        profile_hint="PHASE_A_CHARACTERIZATION",
        math_scope_pin_digest=SCOPE,
        tip_pins=["t1"],
        dep_closure_digest="d" * 64,
        payload=_phase_a_payload(),
        created_at="2026-07-25T12:00:00Z",
    )
    snap = seal_draft(
        draft,
        draft_crp_version_id="draft1",
        gate_record_id="g3",
        sealed_at="2026-07-25T12:00:00Z",
        author_kind=AuthorKind.HUMAN,
        author_principal_digest=PRINCIPAL,
        author_binding_digest=None,
        live_scope_pin=SCOPE,
    )
    from art_int.seal import validate_seal
    from art_int.errors import ValidationError

    validate_seal(snap)
    snap.crp.crp_digest = "ff" * 32
    with pytest.raises(ValidationError):
        validate_seal(snap)


def test_feedback_keeps_required_empty_arrays():
    fb = VerifierFeedbackExport(
        crp_digest="aa" * 32,
        sealed_digest="aa" * 32,
        intake_status=IntakeStatus.ACCEPTED_DRAFT,
        profile=CrpProfile.PHASE_A_CHARACTERIZATION.value,
    )
    body = fb.body_for_digest()
    assert body["draft_claim_digests"] == []
    assert body["obligation_digests"] == []
    assert body["obligations"] == []
    finalize_export(fb)
    assert fb.export_digest


def test_receipt_hash_verify_in_feedback():
    crp_d = "aa" * 32
    receipt = IntakeReceipt(
        crp_digest=crp_d,
        event_seq=7,
        draft_claim_digests=["c1"],
        status=IntakeStatus.ACCEPTED_DRAFT,
        obligation_digests=["o1"],
    )
    receipt.receipt_digest = compute_receipt_digest(receipt)
    fb = VerifierFeedbackExport(
        crp_digest=crp_d,
        sealed_digest=crp_d,
        intake_status=IntakeStatus.ACCEPTED_DRAFT,
        profile=CrpProfile.PHASE_A_CHARACTERIZATION.value,
        receipt_digest=receipt.receipt_digest,
        draft_claim_digests=["c1"],
        obligation_digests=["o1"],
    )
    finalize_export(fb)
    validate_feedback_for_prior(fb, receipt=receipt)
    forged = IntakeReceipt(
        crp_digest=crp_d,
        event_seq=7,
        draft_claim_digests=["c1"],
        status=IntakeStatus.ACCEPTED_DRAFT,
    )
    # wrong digest string on export
    fb.receipt_digest = "00" * 32
    with pytest.raises(ProvenanceError):
        validate_feedback_for_prior(fb, receipt=forged)
    # missing export_digest must not validate
    fb2 = VerifierFeedbackExport(
        crp_digest=crp_d,
        sealed_digest=crp_d,
        intake_status=IntakeStatus.ACCEPTED_DRAFT,
        profile=CrpProfile.PHASE_A_CHARACTERIZATION.value,
        receipt_digest=receipt.receipt_digest,
        draft_claim_digests=["c1"],
        obligation_digests=["o1"],
    )
    with pytest.raises(ProvenanceError, match="export_digest required"):
        validate_feedback_for_prior(fb2, receipt=receipt)


def test_cannot_seal_failed_draft():
    from art_int.errors import ValidationError

    draft = DraftCRPPayload(
        branch_id="br1",
        profile_hint="PHASE_A_CHARACTERIZATION",
        math_scope_pin_digest=SCOPE,
        tip_pins=["t1"],
        dep_closure_digest="d" * 64,
        payload=_phase_a_payload(),
        compile_ok=False,
        created_at="2026-07-25T12:00:00Z",
    )
    with pytest.raises(ValidationError):
        seal_draft(
            draft,
            draft_crp_version_id="draft1",
            gate_record_id="g3",
            sealed_at="2026-07-25T12:00:00Z",
            author_kind=AuthorKind.HUMAN,
            author_principal_digest=PRINCIPAL,
            author_binding_digest=None,
            live_scope_pin=SCOPE,
        )


def test_schema_version_envelope_and_feedback():
    crp = _make_crp()
    env = SubmissionEnvelope(crp=crp, idempotency_key=crp.crp_digest, schema_version="BAD")
    with pytest.raises(SchemaVersionError):
        validate_envelope(env)
    fb = VerifierFeedbackExport(
        crp_digest="aa" * 32,
        sealed_digest="aa" * 32,
        intake_status=IntakeStatus.ACCEPTED_DRAFT,
        profile="PHASE_A_CHARACTERIZATION",
        schema_version="BAD",
    )
    with pytest.raises(SchemaVersionError):
        compute_export_digest(fb)