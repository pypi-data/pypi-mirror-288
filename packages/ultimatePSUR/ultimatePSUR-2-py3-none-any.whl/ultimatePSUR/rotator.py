import aiohttp
from .manager import ProxyManager

class ProxyRotator:
    def __init__(self, config_file: str = "config.json"):
        self.manager = ProxyManager(config_file)

    async def get_proxy(self):
        return await self.manager.get_proxy()

    async def use_proxy(self, url: str, max_retries: int = 3) -> Optional[aiohttp.ClientResponse]:
        for _ in range(max_retries):
            proxy = await self.get_proxy()
            if not proxy:
                return None
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url, proxy=f"http://{proxy}", timeout=10) as response:
                        if response.status == 200:
                            return response
            except:
                continue
        return None