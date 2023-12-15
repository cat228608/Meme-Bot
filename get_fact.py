import aiohttp
import asyncio
import json

cookies = {
    '__ddg1_': 'thEe0tNs9L2YM7ixEmld',
    'PHPSESSID': '9f556dddcb09a7c5c447fb83cd362241',
    'uid': '244ff0ef4e060fedbd1c13c33b657bd2',
    'fid': '473419598',
    'tid': '350893939',
    '_ym_uid': '1701720130983093318',
    '_ym_d': '1701720130',
    '_ym_isad': '2',
    '_ym_visorc': 'b',
}

headers = {
    'authority': 'randstuff.ru',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'origin': 'https://randstuff.ru',
    'referer': 'https://randstuff.ru/fact/',
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120"',
    'sec-ch-ua-mobile': '?1',
    'sec-ch-ua-platform': '"Android"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}

async def random_fact():
    async with aiohttp.ClientSession(cookies=cookies, headers=headers) as session:
        async with session.post('https://randstuff.ru/fact/generate/') as response:
            json_string = await response.text()
            data = json.loads(json_string)
            fact = data['fact']['text']
            return fact
