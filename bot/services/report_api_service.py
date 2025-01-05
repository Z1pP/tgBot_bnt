from typing import Optional
import aiohttp

from entities.report import ReportEnriry


class ReportApiService:
    def __init__(self, base_url: str, endpoint: str):
        self.base_url = base_url
        self.endpoint = endpoint

    async def get_reports(self) -> list[ReportEnriry]:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/{self.endpoint}") as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise

    async def create_report(self, data: dict) -> Optional[ReportEnriry]:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.base_url}/{self.endpoint}", json=data
            ) as response:
                if response.status == 201:
                    return await response.json()
                else:
                    raise
