import asyncio
import aiohttp
from bs4 import BeautifulSoup
import random

async def meme():
    try:
        random_meme = random.randint(1, 3)
        if random_meme == 1:
            random_site = random.randint(1, 2857)
            url = f"https://www.memify.ru/memes/{random_site}"
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    content = await response.text()
                    soup = BeautifulSoup(content, "html.parser")
                    items = soup.find_all("div", {"class": "infinite-item card"})
                    random_item = random.choice(items)
                    second_a = random_item.find_all("a")[1]
                    return f'{second_a.get("href")}'
        elif random_meme == 2:
            url = 'https://mem-baza.ru'
            random_site = random.randint(1, 117)
            async with aiohttp.ClientSession() as session:
                async with session.get(url + f"/page/{random_site}/") as response:
                    content = await response.text()
                    soup = BeautifulSoup(content, "html.parser")
                    items = soup.find_all('img', style='padding:0;border:0;')
                    random_item = random.choice(items)
                    print(random_item['src'])
                    return f"https://mem-baza.ru{random_item['src']}"
        elif random_meme == 3:
            random_site = random.randint(1, 22)
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://www.funomania.ru/mems/page/{random_site}/") as response:
                    content = await response.text()
                    soup = BeautifulSoup(content, "html.parser")
                    items = soup.find_all("article", {"class": "jo9"})
                    random_item = random.choice(items)
                    link = random_item.find("img")["src"]
                    print(link)
                    return f"https://www.funomania.ru{link}"
    except Exception as e:
    	news = await meme()
    	return news
