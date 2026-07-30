"""ART-INT-00 shared A↔B integration layer."""

from art_int.canon import (
    CANON_VERSION,
    H,
    H_tagged,
    canonical_serialization,
    digest_object,
    normalize_unicode,
)
from art_int.enums import (
    AuthorKind,
    CrpProfile,
    IntakeStatus,
    TransportResult,
)
from art_int.errors import (
    IdempotencyConflict,
    IntegrationError,
    SchemaVersionError,
    UnknownFieldError,
    UnsupportedEnumError,
    ValidationError,
)
from art_int.crp import (
    CandidateResearchPackage,
    CrpPayload,
    compute_crp_digest,
    normalize_profile_hint,
    validate_crp_admissibility,
)
from art_int.envelope import SubmissionEnvelope, validate_envelope
from art_int.draft import CompileErrorPayload, DraftCRPPayload
from art_int.seal import SealedCRPSnapshotPayload, seal_draft, validate_seal
from art_int.receipt import IntakeReceipt, compute_receipt_digest
from art_int.feedback import VerifierFeedbackExport, compute_export_digest, finalize_export, validate_feedback_for_prior
from art_int.batch import SubmissionAttempt, SubmissionBatch
from art_int.mechanism import apply_perturbation_mechanism_alias
from art_int.idempotency import check_idempotency_replay

__all__ = [
    "CANON_VERSION",
    "H",
    "H_tagged",
    "canonical_serialization",
    "digest_object",
    "normalize_unicode",
    "AuthorKind",
    "CrpProfile",
    "IntakeStatus",
    "TransportResult",
    "IdempotencyConflict",
    "IntegrationError",
    "SchemaVersionError",
    "UnknownFieldError",
    "UnsupportedEnumError",
    "ValidationError",
    "CandidateResearchPackage",
    "CrpPayload",
    "compute_crp_digest",
    "normalize_profile_hint",
    "validate_crp_admissibility",
    "SubmissionEnvelope",
    "validate_envelope",
    "CompileErrorPayload",
    "DraftCRPPayload",
    "SealedCRPSnapshotPayload",
    "seal_draft",
    "validate_seal",
    "IntakeReceipt",
    "compute_receipt_digest",
    "VerifierFeedbackExport",
    "compute_export_digest",
    "finalize_export",
    "validate_feedback_for_prior",
    "SubmissionAttempt",
    "SubmissionBatch",
    "apply_perturbation_mechanism_alias",
    "check_idempotency_replay",
]
