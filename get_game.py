from bs4 import BeautifulSoup
import aiohttp
import asyncio

async def game():
	try:
		url = f"https://freetp.org"
		async with aiohttp.ClientSession() as session:
			async with session.get(url) as response:
				content = await response.text()
				soup = BeautifulSoup(content, 'html.parser')
				dle_content = soup.find('div', {'class': 'example3'})
				name = dle_content.find('h7').get_text().split('играть')[0]
				desc = dle_content.find('a', {'rel': 'nofollow'})['title'] + "..."
				url = dle_content.find('a', {'rel': 'nofollow'})['href']
				src = dle_content.find('img')['src']
				if "freetp.org" in src:
					src = src.split('freetp.org')[1]
				return [name, desc, url, 'freetp.org' + src]
	except:
		return game()
