import aiohttp
import aiohttp.client_exceptions


async def check_connection() -> bool:
    url = "http://0.0.0.0:8000/api/root"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get("message") == "pong"
                return False
        except aiohttp.client_exceptions.ClientConnectionError:
            return False
