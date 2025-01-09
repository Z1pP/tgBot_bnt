from fastapi import status

from .base import AppException


class NoPermissionException(AppException):
    def __init__(self, operation: str, details: str) -> None:
        self.operation = operation
        self.details = details
        super().__init__(
            message=f"Access denied for operation: {operation}. {details}",
            status_code=status.HTTP_403_FORBIDDEN,
        )
