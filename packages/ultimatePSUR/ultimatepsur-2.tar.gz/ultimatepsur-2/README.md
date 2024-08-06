# UltimatePSUR: Ultimate Proxy Scraper, Updater, and Rotator

UltimatePSUR is a powerful and flexible Python library for scraping, updating, and rotating proxies. It's designed to seamlessly integrate with your web scraping and automation projects.

## Features

- Asynchronous proxy scraping from multiple sources
- Support for custom proxy APIs (e.g., ProxyScrape, Geonode)
- Automatic proxy validation and filtering
- Easy proxy rotation
- Simple integration with aiohttp
- Configurable proxy sources
- Proxy caching and persistence

## Installation

Install UltimatePSUR using pip:
pip install ultimatePSUR

## Quick Start

Here's a simple example of how to use UltimatePSUR:

```python
import asyncio
from ultimatePSUR import ProxyRotator

async def main():
    rotator = ProxyRotator()
    
    # Update proxies
    await rotator.manager.update_proxies()
    
    # Get a random proxy
    proxy = await rotator.get_proxy()
    print(f"Random proxy: {proxy}")
    
    # Use a proxy to make a request
    response = await rotator.use_proxy("https://api.ipify.org")
    if response:
        print(f"Your IP: {await response.text()}")
    else:
        print("Failed to make a request using proxies")

asyncio.run(main())
Advanced Usage
Custom Configuration
Create a config.json file to customize proxy sources and APIs:
json{
    "proxy_sources": [
        "https://free-proxy-list.net/",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt"
    ],
    "custom_apis": {
        "proxyscrape": {
            "url": "https://api.proxyscrape.com/v2/",
            "params": {
                "request": "getproxies",
                "protocol": "http",
                "timeout": "10000",
                "country": "all"
            }
        },
        "geonode": {
            "url": "https://proxylist.geonode.com/api/proxy-list",
            "params": {
                "limit": "500",
                "page": "1",
                "sort_by": "lastChecked",
                "sort_type": "desc"
            },
            "format": "json",
            "json_path": ["data"]
        }
    }
}
Then initialize the ProxyRotator with the config file:
pythonrotator = ProxyRotator(config_file="path/to/your/config.json")
Using Proxies in Web Scraping
pythonimport aiohttp
import asyncio
from ultimatePSUR import ProxyRotator

async def scrape_website(url, rotator):
    for _ in range(3):  # Try up to 3 times
        proxy = await rotator.get_proxy()
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url, proxy=f"http://{proxy}", timeout=10) as response:
                    if response.status == 200:
                        return await response.text()
        except:
            continue
    return None

async def main():
    rotator = ProxyRotator()
    await rotator.manager.update_proxies()

    urls = [
        "https://example.com",
        "https://example.org",
        "https://example.net"
    ]
    
    tasks = [scrape_website(url, rotator) for url in urls]
    results = await asyncio.gather(*tasks)
    
    for url, result in zip(urls, results):
        if result:
            print(f"Successfully scraped {url}")
        else:
            print(f"Failed to scrape {url}")

asyncio.run(main())
Posting Proxies to a Service
pythonimport aiohttp
import asyncio
from ultimatePSUR import ProxyRotator

async def post_proxies(proxies, api_url, api_key):
    async with aiohttp.ClientSession() as session:
        headers = {"Authorization": f"Bearer {api_key}"}
        data = {"proxies": proxies}
        async with session.post(api_url, json=data, headers=headers) as response:
            return await response.json()

async def main():
    rotator = ProxyRotator()
    await rotator.manager.update_proxies()

    api_url = "https://your-proxy-service.com/api/proxies"
    api_key = "your-api-key"

    result = await post_proxies(rotator.manager.proxies, api_url, api_key)
    print(f"Posted {len(rotator.manager.proxies)} proxies. Response: {result}")

asyncio.run(main())
Saving and Loading Proxies
python# Save proxies to a file
await rotator.manager.update_proxies()
rotator.manager.save_proxies("my_proxies.txt")

# Load proxies from a file
loaded_manager = await ProxyManager.load_proxies("my_proxies.txt")
Contributing
Contributions are welcome! Please feel free to submit a Pull Request.
License
This project is licensed under the MIT License - see the LICENSE file for details.
------------------------
## Bonus Examples
# Example 1: Scraping proxies and using them with rotation
```python
import asyncio
import aiohttp
from ultimatePSUR import ProxyManager, ProxyRotator

async def make_request(url, proxy):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, proxy=f"http://{proxy}", timeout=10) as response:
                return await response.text()
    except:
        return None

async def main():
    # Initialize and update the proxy manager
    manager = ProxyManager()
    await manager.update_proxies()
    
    # Save proxies to the default file (proxies.txt)
    manager.save_proxies()
    
    # Create a rotator
    rotator = ProxyRotator()
    
    # Make multiple requests using different proxies
    target_url = "http://httpbin.org/ip"
    for _ in range(5):
        proxy = await rotator.get_proxy()
        result = await make_request(target_url, proxy)
        if result:
            print(f"Request successful using proxy {proxy}")
            print(f"Response: {result}")
        else:
            print(f"Request failed using proxy {proxy}")

asyncio.run(main())
----------------------------------------

# Example 2: Using a custom proxy file and making requests without rotation
```python
import asyncio
import aiohttp
from ultimatePSUR import ProxyManager

async def make_request(url, proxy):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, proxy=f"http://{proxy}", timeout=10) as response:
                return await response.text()
    except:
        return None

async def main():
    # Load proxies from a custom file
    manager = await ProxyManager.load_proxies("my_custom_proxies.txt")
    
    # Make requests using each proxy without rotation
    target_url = "http://httpbin.org/ip"
    for proxy in manager.proxies:
        result = await make_request(target_url, proxy)
        if result:
            print(f"Request successful using proxy {proxy}")
            print(f"Response: {result}")
        else:
            print(f"Request failed using proxy {proxy}")

asyncio.run(main())
-----------------------------------
# Example 3: Scraping from custom Geonode and ProxyScrape APIs and rotating for a specific website
First, update your config.json to include the custom API sources:
jsonCopy{
    "custom_apis": {
        "geonode": {
            "url": "https://proxylist.geonode.com/api/proxy-list",
            "params": {
                "limit": "500",
                "page": "1",
                "sort_by": "lastChecked",
                "sort_type": "desc"
            },
            "format": "json",
            "json_path": ["data"]
        },
        "proxyscrape": {
            "url": "https://api.proxyscrape.com/v2/",
            "params": {
                "request": "getproxies",
                "protocol": "http",
                "timeout": "10000",
                "country": "all"
            }
        }
    }
}
Now, here's the example code:
```python
import asyncio
import aiohttp
from ultimatePSUR import ProxyManager, ProxyRotator

async def make_request(url, proxy):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, proxy=f"http://{proxy}", timeout=10) as response:
                return await response.text()
    except:
        return None

async def main():
    # Initialize and update the proxy manager with custom config
    manager = ProxyManager("config.json")
    await manager.update_proxies()
    
    # Save proxies to the default file (proxies.txt)
    manager.save_proxies()
    
    # Create a rotator
    rotator = ProxyRotator("config.json")
    
    # Make multiple requests to a specific website using different proxies
    target_url = "https://example.com"
    for _ in range(10):
        proxy = await rotator.get_proxy()
        result = await make_request(target_url, proxy)
        if result:
            print(f"Request to {target_url} successful using proxy {proxy}")
        else:
            print(f"Request to {target_url} failed using proxy {proxy}")
        
        # Print the current proxy
        print(f"Current proxy: {proxy}")

asyncio.run(main())

These updates make the library more flexible and capable of handling custom API sources like ProxyScrape and Geonode. The README now includes examples for various use cases, including web scraping with proxies and posting proxies to a service.

To use custom API sources:

1. Add the API details to the `custom_apis` section in your `config.json` file.
2. The library will automatically scrape from these sources along with the default ones.