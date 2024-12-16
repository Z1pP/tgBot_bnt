from dataclasses import dataclass


@dataclass
class ManagerDTO:
    tg_id: int
    username: str
    name: str
    role: str
