from dataclasses import dataclass, field
from typing import Optional

from app.models.manager_models import Manager, Role


@dataclass
class ManagerDTO:
    tg_id: int
    username: str
    name: Optional[str] = None
    role: Role = Role.MANAGER

    is_admin: bool = field(init=False)

    def __post_init__(self):
        self.is_admin = self.role in [Role.SUPER_MANAGER, Role.ADMIN]

    @classmethod
    def create(
        cls,
        tg_id: int,
        username: str,
        name: Optional[str] = None,
        role: Role = Role.MANAGER,
    ) -> "ManagerDTO":
        """
        Создание DTO модели для менеджера
        """
        return cls(tg_id=tg_id, username=username, name=name, role=role)

    @classmethod
    def from_model(cls, model: Manager) -> "ManagerDTO":
        """
        Создание DTO из ORM модели
        """
        return cls(
            tg_id=model.tg_id, username=model.username, name=model.name, role=model.role
        )
