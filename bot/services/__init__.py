import aiohttp
import aiohttp.client_exceptions

from core.config import setting


async def check_connection() -> bool:
    url = f"{setting.API_URL}/health"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("status") == "healthy"
                return False
        except aiohttp.client_exceptions.ClientConnectionError:
            return False
