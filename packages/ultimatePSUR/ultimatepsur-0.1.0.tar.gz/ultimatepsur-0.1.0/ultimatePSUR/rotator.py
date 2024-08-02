import random
from .manager import ProxyManager

class ProxyRotator:
    def __init__(self, update_interval=1800):
        self.manager = ProxyManager(update_interval)

    def get_proxy(self):
        proxies = self.manager.proxies
        return random.choice(proxies) if proxies else None

    def rotate_proxy(self, current_proxy):
        proxies = self.manager.proxies
        if not proxies:
            return None
        current_index = proxies.index(current_proxy) if current_proxy in proxies else -1
        next_index = (current_index + 1) % len(proxies)
        return proxies[next_index]

    def use_proxy(self, url, max_retries=3):
        for _ in range(max_retries):
            proxy = self.get_proxy()
            if not proxy:
                return None
            try:
                response = requests.get(url, proxies={'http': proxy, 'https': proxy}, timeout=10)
                if response.status_code == 200:
                    return response
            except:
                self.manager.proxies.remove(proxy)
        return None