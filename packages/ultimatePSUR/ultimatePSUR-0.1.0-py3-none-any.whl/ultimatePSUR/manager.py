import threading
import time
import requests
from .scraper import ProxyScraper

class ProxyManager:
    def __init__(self, update_interval=1800):
        self.proxies = []
        self.update_interval = update_interval
        self.scraper = ProxyScraper()
        self._update_thread = threading.Thread(target=self._auto_update, daemon=True)
        self._update_thread.start()

    def _auto_update(self):
        while True:
            self.update_proxies()
            time.sleep(self.update_interval)

    def update_proxies(self):
        new_proxies = self.scraper.scrape()
        self.proxies = self._filter_working_proxies(new_proxies)

    def _filter_working_proxies(self, proxies):
        working_proxies = []
        for proxy in proxies:
            if self._check_proxy(proxy):
                working_proxies.append(proxy)
        return working_proxies

    def _check_proxy(self, proxy):
        try:
            response = requests.get('http://httpbin.org/ip', proxies={'http': proxy, 'https': proxy}, timeout=5)
            return response.status_code == 200
        except:
            return False

    def get_proxy(self):
        if not self.proxies:
            self.update_proxies()
        return self.proxies[0] if self.proxies else None