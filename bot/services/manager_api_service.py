from aiohttp import ClientSession
from typing import Optional

from bot.dto.manager import ManagerDTO


class ManagerApiService:
    def __init__(self, base_url: str, endpoint: str):
        self.base_url = base_url
        self.endpoint = endpoint

    def _json_to_dto(self, data: dict) -> ManagerDTO:
        """
        Преобразование JSON в DTO
        """
        return ManagerDTO(**data)

    async def get_manager_by_id(self, id: int) -> Optional[ManagerDTO]:
        async with ClientSession() as session:
            async with session.get(
                f"{self.base_url}/{self.endpoint}/{id}/"
            ) as response:
                data = await response.json()
                return self._json_to_dto(data)

    async def create_manager(self, data: dict) -> Optional[ManagerDTO]:
        async with ClientSession() as session:
            async with session.post(
                f"{self.base_url}/{self.endpoint}/", json=data
            ) as response:
                data = await response.json()
                return self._json_to_dto(data)

    async def update_manager_name(self, id: int, data: dict) -> Optional[ManagerDTO]:
        async with ClientSession() as session:
            async with session.put(
                f"{self.base_url}/{self.endpoint}/{id}/", json=data
            ) as response:
                data = await response.json()
                return self._json_to_dto(data)
