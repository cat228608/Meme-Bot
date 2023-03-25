from bs4 import BeautifulSoup
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InputMediaPhoto
from aiogram.utils.exceptions import Throttled
from aiogram.dispatcher import FSMContext
from datetime import datetime
import logging
import asyncio
import aiohttp
#import requests
#import requests_async as requests
import random

bot = Bot(token="") #Тут токен
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)

async def anti_flood(*args, **kwargs):
    message = args[0]
    await message.answer("Мем читай, а не спамь сука!", show_alert=True)

@dp.message_handler(commands="meme")
@dp.throttled(anti_flood,rate=2)
async def meme(message: types.Message):
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
                    keyboard = types.InlineKeyboardMarkup()
                    buttons = [
                        types.InlineKeyboardButton(text="🔄Обновить", callback_data="update")
                    ]
                    keyboard.add(*buttons)
                    await bot.send_photo(message.chat.id, second_a.get("href"), caption = f'☄️Лови мем.', reply_markup=keyboard)
        elif random_meme == 2:
            url = 'https://mem-baza.ru'
            random_site = random.randint(1, 117)
            async with aiohttp.ClientSession() as session:
                async with session.get(url + f"?page{random_site}") as response:
                    content = await response.text()
                    soup = BeautifulSoup(content, "html.parser")
                    items = soup.find_all('img', style='padding:0;border:0;')
                    random_item = random.choice(items)
                    keyboard = types.InlineKeyboardMarkup()
                    buttons = [
                        types.InlineKeyboardButton(text="🔄Обновить", callback_data="update")
                    ]
                    keyboard.add(*buttons)
                    await bot.send_photo(message.chat.id, f"https://mem-baza.ru{random_item['src']}", caption = f'☄️Эй! Лови мемасик!)', reply_markup=keyboard)
        elif random_meme == 3:
            random_site = random.randint(1, 22)
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://www.funomania.ru/mems/page/{random_site}/") as response:
                    content = await response.text()
                    soup = BeautifulSoup(content, "html.parser")
                    items = soup.find_all("article", {"class": "block story shortstory"})
                    random_item = random.choice(items)
                    link = random_item.find("img", {"class": "fr-dib"})["src"]
                    keyboard = types.InlineKeyboardMarkup()
                    buttons = [
                        types.InlineKeyboardButton(text="🔄Обновить", callback_data="update")
                    ]
                    keyboard.add(*buttons)
                    await bot.send_photo(message.chat.id, f"https://www.funomania.ru{link}", caption = f'☄️Эй! Лови мем с новой базы!)', reply_markup=keyboard)
    except Exception as e:
        print(e)
    
@dp.callback_query_handler(text="update")
@dp.throttled(anti_flood,rate=5)
async def update(call: types.CallbackQuery):
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
                    keyboard = types.InlineKeyboardMarkup()
                    buttons = [
                        types.InlineKeyboardButton(text="🔄Обновить", callback_data="update")
                    ]
                    keyboard.add(*buttons)
                    now = datetime.now()
                    current_time = now.strftime("%H:%M:%S")
                    await call.message.edit_media(InputMediaPhoto(second_a.get("href")))
                    await call.message.edit_caption(caption = f'⏱Мем был обновлен в: {current_time}', reply_markup=keyboard)
        elif random_meme == 2:
            url = 'https://mem-baza.ru'
            random_site = random.randint(1, 117)
            async with aiohttp.ClientSession() as session:
                async with session.get(url + f"?page{random_site}") as response:
                    content = await response.text()
                    soup = BeautifulSoup(content, "html.parser")
                    items = soup.find_all('img', style='padding:0;border:0;')
                    random_item = random.choice(items)
                    keyboard = types.InlineKeyboardMarkup()
                    buttons = [
                        types.InlineKeyboardButton(text="🔄Обновить", callback_data="update")
                    ]
                    keyboard.add(*buttons)
                    now = datetime.now()
                    current_time = now.strftime("%H:%M:%S")
                    await call.message.edit_media(InputMediaPhoto(f"https://mem-baza.ru{random_item['src']}"))
                    await call.message.edit_caption(caption = f'⏱Мем был обновлен в: {current_time}', reply_markup=keyboard)
        elif random_meme == 3:
            random_site = random.randint(1, 22)
            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://www.funomania.ru/mems/page/{random_site}/") as response:
                    content = await response.text()
                    soup = BeautifulSoup(content, "html.parser")
                    items = soup.find_all("article", {"class": "block story shortstory"})
                    random_item = random.choice(items)
                    link = random_item.find("img", {"class": "fr-dib"})["src"]
                    keyboard = types.InlineKeyboardMarkup()
                    buttons = [
                        types.InlineKeyboardButton(text="🔄Обновить", callback_data="update")
                    ]
                    keyboard.add(*buttons)
                    now = datetime.now()
                    current_time = now.strftime("%H:%M:%S")
                    await call.message.edit_media(InputMediaPhoto(f"https://www.funomania.ru{link}"))
                    await call.message.edit_caption(caption = f'⏱Мем был обновлен в: {current_time}', reply_markup=keyboard)
    except Exception as e:
        print(e)
    
    
while True:
    try:
        if __name__ == "__main__":
            executor.start_polling(dp, skip_updates=True)
        break
    except:
        print("Ошика.\nОжидаем перезапуск 20 сек...")
        time.sleep(20)