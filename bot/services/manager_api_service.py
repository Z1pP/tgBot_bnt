from aiohttp import ClientSession
from typing import Optional

from entities.manager import ManagerEntity


class ManagerApiService:
    def __init__(self, base_url: str, endpoint: str):
        self.base_url = base_url
        self.endpoint = endpoint

    def _json_to_dto(self, data: dict) -> ManagerEntity:
        """
        Преобразование JSON в DTO
        """
        return ManagerEntity(**data)

    async def get_manager_by_id(self, id: int) -> Optional[ManagerEntity]:
        async with ClientSession() as session:
            async with session.get(
                f"{self.base_url}/{self.endpoint}/{id}/"
            ) as response:
                data = await response.json()

                if not data:
                    return None

                return self._json_to_dto(data)

    async def create_manager(self, data: dict) -> Optional[ManagerEntity]:
        async with ClientSession() as session:
            async with session.post(
                f"{self.base_url}/{self.endpoint}/", json=data
            ) as response:
                if response.status == 201:
                    data = await response.json()
                    return self._json_to_dto(data)
                return None

    async def update_manager_name(self, id: int, data: dict) -> Optional[ManagerEntity]:
        async with ClientSession() as session:
            async with session.put(
                f"{self.base_url}/{self.endpoint}/{id}/", json=data
            ) as response:
                data = await response.json()
                return self._json_to_dto(data)
