"""Custom exceptions for business logic errors.

Services raise these exceptions. The API layer catches them
and converts to appropriate HTTP responses.
"""


class BusinessError(Exception):
    """Base exception for all business logic errors."""

    def __init__(self, message: str, code: str = "BUSINESS_ERROR") -> None:
        self.message = message
        self.code = code
        super().__init__(message)


class ValidationError(BusinessError):
    """Raised when input data violates business rules."""

    def __init__(self, message: str, field: str | None = None) -> None:
        self.field = field
        super().__init__(message, code="VALIDATION_ERROR")


class NotFoundError(BusinessError):
    """Raised when a requested entity does not exist."""

    def __init__(self, entity: str, identifier: str) -> None:
        super().__init__(f"{entity} not found: {identifier}", code="NOT_FOUND")


class DuplicateError(BusinessError):
    """Raised when attempting to create a duplicate entity."""

    def __init__(self, entity: str, field: str, value: str) -> None:
        super().__init__(
            f"{entity} with {field}='{value}' already exists",
            code="DUPLICATE",
        )


class UnauthorizedError(BusinessError):
    """Raised when authentication fails."""

    def __init__(self, message: str = "Invalid credentials") -> None:
        super().__init__(message, code="UNAUTHORIZED")


class ForbiddenError(BusinessError):
    """Raised when the user lacks permission for an action."""

    def __init__(self, message: str = "Insufficient permissions") -> None:
        super().__init__(message, code="FORBIDDEN")
