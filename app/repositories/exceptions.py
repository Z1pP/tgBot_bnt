class BaseRepositoryException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class ManagerNotFoundException(BaseRepositoryException):
    def __init__(self, manager_tg_id: str):
        super().__init__(f"Manager с id {manager_tg_id} не найден")


class ManagerAlreadyExistsException(BaseRepositoryException):
    def __init__(self, manager_tg_id: str):
        super().__init__(f"Manager с id {manager_tg_id} уже существует")


class ReportNotFoundException(BaseRepositoryException):
    def __init__(self, report_id: str):
        super().__init__(f"Report с id {report_id} не найден")


class ReportAlreadyExistsException(BaseRepositoryException):
    def __init__(self, report_id: str):
        super().__init__(f"Report с id {report_id} уже существует")
