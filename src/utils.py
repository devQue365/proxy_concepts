import csv
import aiohttp
import asyncio


TIMEOUT = 10

ERROR = "\033[31m\033[1m"
SUCCESS = "\033[32m\033[1m"
DEFAULT = "\033[0m"

def extract_proxies(file_path: __file__):
    proxy_collection = []
    try:
        with open(file_path, newline='') as csv_file:
            # create reader object
            reader = csv.DictReader(csv_file)
            for row in reader:
                if all(k in ('Host', 'Port', 'User', 'Pass') for k in row):
                    # generate proxy record
                    proxy_record = {
                        'host': row['Host'].strip(),
                        'port': row['Port'].strip(),
                        'user': row['User'].strip(),
                        'pass': row['Pass'].strip()
                    }
                    # get the url -> https://username:password:host:port
                    proxy_url = f"http://{proxy_record['user']}:{proxy_record['pass']}@{proxy_record['host']}:{proxy_record['port']}"
                    proxy_collection.append(proxy_url)
        return proxy_collection
    except Exception as e:
        return {'error': str(e)}

# basic check to see the validity of proxies
async def validity_check(proxy):
    proxy_list = {
        'http': proxy,
        'https': proxy
    }
    async with aiohttp.ClientSession(timeout=TIMEOUT) as session:
        try:
            async with session.get("https://httpbin.org/ip", timeout=TIMEOUT, proxy=proxy_list) as res:
                text = await res.text
                print(f"{SUCCESS}Proxy_response status : {res.status}{DEFAULT}")
        except Exception as e:
            print(f"{ERROR}Exception = {str(e)}{DEFAULT}")
        

# make concurrent requests to url
async def make_request(session: aiohttp.ClientSession, url, proxy) -> dict | None:
    try:
        async with session.get(url, proxy = proxy, timeout = TIMEOUT) as response:
            return await response.text()
    except Exception as e:
        print(f"{ERROR}Exception = {str(e)}{DEFAULT}")
        return None
    