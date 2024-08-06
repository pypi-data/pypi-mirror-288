import asyncio
import aiohttp
import random
from typing import List, Optional
from .scraper import ProxyScraper

class ProxyManager:
    def __init__(self, config_file: str = "config.json"):
        self.scraper = ProxyScraper(config_file)
        self.proxies: List[str] = []
        self.lock = asyncio.Lock()

    async def update_proxies(self):
        async with self.lock:
            self.proxies = await self.scraper.scrape()
            self.proxies = await self._filter_working_proxies(self.proxies)

    async def _filter_working_proxies(self, proxies: List[str]) -> List[str]:
        async def check_proxy(proxy):
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get('http://httpbin.org/ip', proxy=f"http://{proxy}", timeout=5) as response:
                        return proxy if response.status == 200 else None
            except:
                return None

        tasks = [check_proxy(proxy) for proxy in proxies]
        results = await asyncio.gather(*tasks)
        return [proxy for proxy in results if proxy]

    async def get_proxy(self) -> Optional[str]:
        async with self.lock:
            return random.choice(self.proxies) if self.proxies else None

    def save_proxies(self, filename: str = "proxies.txt"):
        with open(filename, "w") as f:
            f.write("\n".join(self.proxies))

    @classmethod
    async def load_proxies(cls, filename: str = "proxies.txt") -> 'ProxyManager':
        manager = cls()
        try:
            with open(filename, "r") as f:
                manager.proxies = [line.strip() for line in f]
        except FileNotFoundError:
            await manager.update_proxies()
        return manager