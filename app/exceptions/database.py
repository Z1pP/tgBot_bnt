import logging
from fastapi import status

from .base import AppException

logger = logging.getLogger(__name__)


class DatabaseOperationException(AppException):
    def __init__(self, operation: str, entity: str, details: str):
        message = f"Database {operation} operation failed"
        super().__init__(
            message=message, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
        # Логируем сразу при создании исключения
        logger.error(
            f"Database error during {operation} operation on {entity}: {details}",
            extra={"operation": operation, "entity": entity, "details": details},
        )
