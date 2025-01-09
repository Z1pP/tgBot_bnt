import logging
from fastapi import status

from .base import AppException


logger = logging.getLogger(__name__)


class RepositoryException(AppException):
    def __init__(self, message: str, status_code: int, **kwargs):
        super().__init__(message=message, status_code=status_code)
        # Логируем дополнительную информацию
        logger.error(
            f"Repository error: {message}", extra={"status_code": status_code, **kwargs}
        )


class EntityNotFoundException(RepositoryException):
    def __init__(self, entity: str, entity_id: int):
        message = f"{entity} with ID {entity_id} not found"
        super().__init__(
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
            entity=entity,
            entity_id=entity_id,
            error_type="not_found",
        )


class EntityAlreadyExistsException(RepositoryException):
    def __init__(self, entity: str, entity_id: str):
        message = f"{entity} with ID {entity_id} already exist"
        super().__init__(
            message=message,
            status_code=status.HTTP_409_CONFLICT,
            entity=entity,
            entity_id=entity_id,
            error_type="already_exists",
        )


class InvalidReturnTypeException(RepositoryException):
    def __init__(self, allowed_types: list[type], received_type: type):
        message = (
            f"Unsupported return type: {received_type}. Allowed types: {allowed_types}"
        )
        super().__init__(
            message=message,
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            allowed_types=str(allowed_types),
            received_type=str(received_type),
            error_type="invalid_return_type",
        )
