import asyncio
import aiohttp
from bs4 import BeautifulSoup
import re
from typing import List, Dict
import json

class ProxyScraper:
    def __init__(self, config_file: str = "config.json"):
        with open(config_file, "r") as f:
            self.config = json.load(f)
        self.urls = self.config.get("proxy_sources", [
            "https://free-proxy-list.net/",
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt",
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt"
        ])
        self.custom_apis = self.config.get("custom_apis", {})

    async def scrape(self) -> List[str]:
        async with aiohttp.ClientSession() as session:
            tasks = [self._scrape_url(session, url) for url in self.urls]
            tasks += [self._scrape_custom_api(session, name, api_info) for name, api_info in self.custom_apis.items()]
            proxy_lists = await asyncio.gather(*tasks)
        return list(set([proxy for sublist in proxy_lists for proxy in sublist]))

    async def _scrape_url(self, session: aiohttp.ClientSession, url: str) -> List[str]:
        try:
            async with session.get(url, timeout=10) as response:
                content = await response.text()
                return self._parse_proxies(content)
        except:
            return []

    def _parse_proxies(self, content: str) -> List[str]:
        proxies = re.findall(r'\d+\.\d+\.\d+\.\d+:\d+', content)
        soup = BeautifulSoup(content, 'html.parser')
        for row in soup.select('table tr'):
            cols = row.find_all('td')
            if len(cols) >= 2:
                ip = cols[0].text.strip()
                port = cols[1].text.strip()
                if re.match(r'\d+\.\d+\.\d+\.\d+', ip) and port.isdigit():
                    proxies.append(f"{ip}:{port}")
        return proxies

    async def _scrape_custom_api(self, session: aiohttp.ClientSession, name: str, api_info: Dict) -> List[str]:
        try:
            url = api_info['url']
            headers = api_info.get('headers', {})
            params = api_info.get('params', {})
            
            async with session.get(url, headers=headers, params=params, timeout=10) as response:
                if response.status == 200:
                    content = await response.text()
                    if api_info.get('format') == 'json':
                        data = json.loads(content)
                        return self._parse_json_response(data, api_info.get('json_path', []))
                    else:
                        return self._parse_proxies(content)
        except:
            return []

    def _parse_json_response(self, data: Dict, json_path: List[str]) -> List[str]:
        for key in json_path:
            if isinstance(data, dict):
                data = data.get(key, [])
            elif isinstance(data, list):
                data = data[0].get(key, []) if data else []
        
        if isinstance(data, list):
            return [f"{item['ip']}:{item['port']}" for item in data if 'ip' in item and 'port' in item]
        return []