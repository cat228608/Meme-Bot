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
    except Exception as e:
        print(e)
    
@dp.callback_query_handler(text="update")
@dp.throttled(anti_flood,rate=5)
async def update(call: types.CallbackQuery):
    try:
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