import aiohttp
from bs4 import BeautifulSoup
import random
import asyncio

async def get_random_anecdote():
   headers = {
       'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.109 Safari/537.36 OPR/84.0.4316.52'
   }

   url = 'https://www.anekdot.ru/random/anekdot/'

   async with aiohttp.ClientSession() as session:
       async with session.get(url, headers=headers) as response:
           html = await response.text()

   soup = BeautifulSoup(html, 'html.parser')

   anecdotes = soup.find_all('div', class_="text")
   random_anecdote = random.choice(anecdotes)
   utf8_string = unicode_string.encode('utf-8')
   text_encode = u'{random_anecdote.text.strip()}'.encode('utf-8')
    
   return random_anecdote.text.strip()
