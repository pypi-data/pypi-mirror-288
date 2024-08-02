import requests
from bs4 import BeautifulSoup
import re
from concurrent.futures import ThreadPoolExecutor, as_completed

class ProxyScraper:
    def __init__(self):
        self.urls = [
            "https://free-proxy-list.net/",
            "https://advanced.name/freeproxy",
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt",
            "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt"
        ]

    def scrape(self):
        with ThreadPoolExecutor(max_workers=10) as executor:
            future_to_url = {executor.submit(self._process_url, url): url for url in self.urls}
            proxy_lists = []
            for future in as_completed(future_to_url):
                try:
                    proxy_lists.append(future.result())
                except Exception as e:
                    print(f"Error processing URL: {e}")
        return self._filter_and_combine_proxies(proxy_lists)

    def _process_url(self, url):
        if "free-proxy-list" in url:
            return self._scrape_free_proxy_list(url)
        elif "advanced.name" in url:
            return self._scrape_advanced_name_proxies(url)
        else:
            return self._download_raw_proxies(url)

    def _scrape_free_proxy_list(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        proxies = []
        for row in soup.select('table.table tbody tr'):
            cols = row.find_all('td')
            if len(cols) >= 2:
                ip = cols[0].text.strip()
                port = cols[1].text.strip()
                proxies.append(f"{ip}:{port}")
        return proxies

    def _scrape_advanced_name_proxies(self, url):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        proxies = []
        for row in soup.select('table#table_proxies tbody tr'):
            ip = row.get('data-ip')
            port = row.get('data-port')
            if ip and port:
                proxies.append(f"{ip}:{port}")
        return proxies

    def _download_raw_proxies(self, url):
        response = requests.get(url)
        return [line.strip() for line in response.text.splitlines() if line.strip()]

    def _is_valid_proxy(self, proxy):
        pattern = r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{1,5}$'
        return bool(re.match(pattern, proxy))

    def _filter_and_combine_proxies(self, proxy_lists):
        unique_proxies = set()
        for proxies in proxy_lists:
            for proxy in proxies:
                if self._is_valid_proxy(proxy):
                    unique_proxies.add(proxy)
        return sorted(list(unique_proxies))