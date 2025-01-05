from dataclasses import dataclass


@dataclass
class ManagerEntity:
    tg_id: int
    username: str
    name: str
    role: str
