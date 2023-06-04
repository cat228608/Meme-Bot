from bs4 import BeautifulSoup
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InputMediaPhoto, InlineQueryResultPhoto, InputTextMessageContent, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.exceptions import Throttled
from aiogram.dispatcher import FSMContext
from datetime import datetime
import logging
import asyncio
import aiohttp
import random
import get_meme

bot = Bot(token="") #Тут токен
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)

async def anti_flood(*args, **kwargs):
    message = args[0]
    await message.answer("Мем читай, а не спамь!", show_alert=True)

@dp.inline_handler()
async def process_inline_query(query: types.InlineQuery):
    result = await get_meme.meme()
    results = [
        types.InlineQueryResultPhoto(
            id='meme',
            photo_url=result,
            thumb_url=result,
            caption='🔮Лови мем',
            reply_markup=types.InlineKeyboardMarkup()
                .add(types.InlineKeyboardButton(text='🔄Обновить', callback_data='refresh'))
        )
    ]
    await bot.answer_inline_query(query.id, results)

@dp.callback_query_handler(text="refresh")
@dp.throttled(anti_flood, rate=2)
async def refresh(call: types.CallbackQuery):
    try:
        result = await get_meme.meme()
        keyboard = types.InlineKeyboardMarkup()
        buttons = [
            types.InlineKeyboardButton(text="🔄Обновить", callback_data="refresh")
        ]
        keyboard.add(*buttons)
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        await bot.edit_message_media(inline_message_id=call.inline_message_id, media=InputMediaPhoto(result))
        await bot.edit_message_caption(inline_message_id=call.inline_message_id, caption=f'⏱Мем был обновлен в: {current_time}', reply_markup=keyboard)
    except Exception as e:
        print(e)

@dp.message_handler(commands="meme")
@dp.throttled(anti_flood,rate=2)
async def meme(message: types.Message):
    try:
        result = await get_meme.meme()
        keyboard = types.InlineKeyboardMarkup()
        buttons = [
            types.InlineKeyboardButton(text="🔄Обновить", callback_data="update")
            ]
        keyboard.add(*buttons)
        await bot.send_photo(message.chat.id, result, caption = f'☄️Эй! Лови мем!', reply_markup=keyboard)
    except Exception as e:
        print(e)
    
@dp.callback_query_handler(text="update")
@dp.throttled(anti_flood,rate=5)
async def update(call: types.CallbackQuery): #Аня, я тебя люблю сильнее жизни!
    try:
        result = await get_meme.meme()
        keyboard = types.InlineKeyboardMarkup()
        buttons = [
            types.InlineKeyboardButton(text="🔄Обновить", callback_data="update")
        ]
        keyboard.add(*buttons)
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        await call.message.edit_media(InputMediaPhoto(result))
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