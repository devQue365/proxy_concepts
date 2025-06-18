from utils import *
from itertools import cycle
import random
import sys
# Concurrent request logic
async def make_concurrent_requests(url_list, proxy_pool, max_concurrent = 100):
    sem = asyncio.Semaphore(max_concurrent)
    proxy_cycle = cycle(proxy_pool)
    async with aiohttp.ClientSession() as session:
        async def sem_make_request(url):
            # get the next proxy
            proxy = next(proxy_cycle)
            async with sem:
                return await make_request(session, url, proxy)
        tasks = [sem_make_request(url) for url in url_list]
        # get the results
        results = await asyncio.gather(*tasks)
        return results

if __name__ == '__main__':
    url_list = ['https://www.google.com/', 'https://www.google.com/search?q=glassdoor']
    # proxies (csv) file path
    FILE__PATH = 'src/proxies.csv'
    proxy_pool = extract_proxies(FILE__PATH)
    if (not proxy_pool):
        print(f"{ERROR}Proxies not found !{DEFAULT}")
        sys.exit(1)
    response_json = asyncio.run((make_concurrent_requests(url_list, proxy_pool)))
    if(response_json):
        print(response_json)
