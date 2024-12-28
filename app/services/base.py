from abc import ABC, abstractmethod
from typing import Sequence, Optional

from app.schemas.managers import ManagerSchema
from app.schemas.reports import ReportSchemaInput, ReportSchemaOutput


class IManagersService(ABC):
    @abstractmethod
    async def get_managers(self) -> Sequence[ManagerSchema]:
        """
        Получить всех менеджеров из источника данных.

        Возвращает:
            Sequence[ManagerSchema]: Список схем менеджеров
        """
        pass

    @abstractmethod
    async def get_by_tg_id(self, tg_id: int) -> Optional[ManagerSchema]:
        """
        Получить менеджера по его Telegram ID.

        Аргументы:
            tg_id (int): ID пользователя в Telegram

        Возвращает:
            Optional[ManagerSchema]: Схема менеджера, если найден, иначе None
        """
        pass

    @abstractmethod
    async def create_manager(self, schema: ManagerSchema) -> Optional[ManagerSchema]:
        """
        Создать нового менеджера.

        Аргументы:
            schema (ManagerSchema): Данные для создания менеджера

        Возвращает:
            ManagerSchema: Схема созданного менеджера
        """
        pass

    @abstractmethod
    async def change_name_by_tg_id(
        self, tg_id: int, name: str
    ) -> Optional[ManagerSchema]:
        """
        Изменить имя менеджера по его Telegram ID.

        Аргументы:
            tg_id (int): ID пользователя в Telegram
            name (str): Новое имя менеджера

        Возвращает:
            Optional[ManagerSchema]: Обновленная схема менеджера, если найден, иначе None
        """
        pass

    @abstractmethod
    async def delete_manager(self, tg_id: int) -> bool:
        """
        Удалить менеджера по его Telegram ID.

        Аргументы:
            tg_id (int): ID пользователя в Telegram

        Возвращает:
            bool: True, если удаление прошло успешно, иначе False
        """
        pass


class IReportsService(ABC):
    @abstractmethod
    async def get_reports_by_tg_id(self, tg_id: int) -> list[ReportSchemaOutput]:
        pass

    @abstractmethod
    async def create_report(self, report: ReportSchemaInput) -> ReportSchemaOutput:
        pass
