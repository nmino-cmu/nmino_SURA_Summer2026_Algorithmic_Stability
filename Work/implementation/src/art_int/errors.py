"""Integration-layer errors."""


class IntegrationError(Exception):
    code: str = "INTEGRATION_ERROR"

    def __init__(self, message: str, *, code: str | None = None):
        super().__init__(message)
        if code:
            self.code = code


class ValidationError(IntegrationError):
    code = "VALIDATION"


class SchemaVersionError(IntegrationError):
    code = "UNSUPPORTED_SCHEMA_VERSION"


class UnknownFieldError(IntegrationError):
    code = "UNKNOWN_FIELD"


class UnsupportedEnumError(IntegrationError):
    code = "UNSUPPORTED_ENUM"


class IdempotencyConflict(IntegrationError):
    code = "IDEMPOTENCY_CONFLICT"


class ProvenanceError(IntegrationError):
    code = "PROVENANCE"


class AdmissibilityError(IntegrationError):
    code = "PACKAGE_INADMISSIBLE"
