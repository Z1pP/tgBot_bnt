from aiohttp import ClientSession
from typing import Optional

from entities.manager import ManagerEntity
from utils.logger import bot_logger


class ManagerApiService:
    def __init__(self, base_url: str, endpoint: str):
        self.base_url = base_url
        self.endpoint = endpoint

    def _json_to_dto(self, data: dict) -> ManagerEntity:
        """
        Преобразование JSON в DTO
        """
        return ManagerEntity(**data)

    async def _make_request(
        self, id: int = None, data: dict = None, method: str = "GET"
    ) -> Optional[ManagerEntity]:
        async with ClientSession() as session:
            url = f"{self.base_url}/{self.endpoint}/"

            if id is not None:
                url += f"{id}/"

            method_map = {
                "GET": (session.get, 200),
                "POST": (session.post, 201),
                "PUT": (session.put, 200),
                "DELETE": (session.delete, 204),
            }

            try:
                method_func, expected_status = method_map.get(
                    method.upper(), (None, None)
                )

                if not method_func:
                    raise ValueError(f'Метод "{method}" не поддерживается')

                kwargs = (
                    {"json": data} if method.upper() in ["POST", "PUT", "PATCH"] else {}
                )

                async with method_func(url, **kwargs) as response:
                    if response.status == expected_status:
                        if method.upper() == "DELETE":
                            return True
                        response_data = await response.json()
                        return self._json_to_dto(response_data)

                    return None

            except Exception as e:
                bot_logger.error(f"Ошибка в make_request: {e}")

    async def get_manager_by_id(self, id: int) -> Optional[ManagerEntity]:
        return await self._make_request(id=id)

    async def create_manager(self, data: dict) -> Optional[ManagerEntity]:
        return await self._make_request(data=data, method="POST")

    async def update_manager(self, id: int, data: dict) -> Optional[ManagerEntity]:
        return await self._make_request(id=id, data=data, method="PUT")

    async def delete_manager(self, id: int):
        return await self._make_request(id=id, method="DELETE")
