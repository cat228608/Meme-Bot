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
import get_joke
import get_fact
import get_game

bot = Bot(token="") #Тут токен
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
logging.basicConfig(level=logging.INFO)

async def anti_flood(*args, **kwargs):
    message = args[0]
    await message.answer("[Anti-spam] No no no mr. Fish!", show_alert=True)

async def delete_message(call: types.CallbackQuery):
    try:
        await bot.delete_message(call.message.chat.id, call.message.message_id)
    except Exception as e:
        print(e)

@dp.inline_handler()
async def process_inline_query(query: types.InlineQuery):
    fact_result = await get_fact.random_fact()
    fact_inline_result = types.InlineQueryResultArticle(
        id='fact',
        title='Случайный факт',
        description='Нажми на кнопку для получения случайного факта',
        input_message_content=types.InputTextMessageContent(
            message_text=fact_result
        ),
        reply_markup=types.InlineKeyboardMarkup()
            .add(
                types.InlineKeyboardButton(text='🔄 Обновить', callback_data='refresh_fact')
            )
            )    
    joke_result = await get_joke.get_random_anecdote()
    joke_inline_result = types.InlineQueryResultArticle(
        id='joke',
        title='Случайный анекдот',
        description='Нажми на кнопку для получения случайного анекдота',
        input_message_content=types.InputTextMessageContent(
            message_text=joke_result
        ),
        reply_markup=types.InlineKeyboardMarkup()
            .add(
                types.InlineKeyboardButton(text='🔄 Обновить', callback_data='refresh_joke')
            )
            )
    
    meme_result = await get_meme.meme()
    meme_inline_result = types.InlineQueryResultPhoto(
        id='meme',
        title='Случайный мем',
        description='Нажми на кнопку для получения смешной картинки',
        photo_url=meme_result,
        thumb_url=meme_result,
        caption='🔮Лови мем\n\nP.s Мемы вызванные инлайн методом не поддерживают удаления:(',
        reply_markup=types.InlineKeyboardMarkup()
            .add(types.InlineKeyboardButton(text='🔄 Обновить', callback_data='refresh'))
    )
    
    game_result = await get_game.game()
    game_inline_result = types.InlineQueryResultPhoto(
        id='game',
        title='Случайная coop игра',
        description='Нажми на кнопку для получения случайной coop игры',
        photo_url=game_result[3],
        thumb_url=game_result[3],
        caption=f'🎮Случайная Coop игра под названием {game_result[0]}\n\nОписание: {game_result[1]}',
        reply_markup=types.InlineKeyboardMarkup()
            .add(
            types.InlineKeyboardButton(text="🌐Страница игры", url=game_result[2]),
            types.InlineKeyboardButton(text='🔄 Обновить', callback_data='refresh_game'))
    )
    
    results = [meme_inline_result, game_inline_result, joke_inline_result, fact_inline_result]

    await bot.answer_inline_query(query.id, results)

@dp.callback_query_handler(text="refresh_joke")
@dp.throttled(anti_flood, rate=2)
async def refresh(call: types.CallbackQuery):
    try:
        result = await get_joke.get_random_anecdote()
        keyboard = types.InlineKeyboardMarkup()
        buttons = [
            types.InlineKeyboardButton(text="🔄 Обновить", callback_data="refresh_joke")]
        keyboard.add(*buttons)
        await call.bot.edit_message_text(text=result, inline_message_id=call.inline_message_id, reply_markup=keyboard)   
    except Exception as e:
        print(e)

@dp.callback_query_handler(text="refresh_fact")
@dp.throttled(anti_flood, rate=2)
async def refresh(call: types.CallbackQuery):
    try:
        result = await get_fact.random_fact()
        keyboard = types.InlineKeyboardMarkup()
        buttons = [
            types.InlineKeyboardButton(text="🔄 Обновить", callback_data="refresh_fact")]
        keyboard.add(*buttons)
        await call.bot.edit_message_text(text=result, inline_message_id=call.inline_message_id, reply_markup=keyboard)        
    except Exception as e:
        print(e)

@dp.callback_query_handler(text="refresh")
@dp.throttled(anti_flood, rate=2)
async def refresh(call: types.CallbackQuery):
    try:
        result = await get_meme.meme()
        keyboard = types.InlineKeyboardMarkup()
        buttons = [
            types.InlineKeyboardButton(text="🔄 Обновить", callback_data="refresh")]
        keyboard.add(*buttons)
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        await bot.edit_message_media(inline_message_id=call.inline_message_id, media=InputMediaPhoto(result))
        await bot.edit_message_caption(inline_message_id=call.inline_message_id, caption=f'⏱Мем был обновлен в: {current_time}', reply_markup=keyboard)
    except Exception as e:
        print(e)
        
@dp.callback_query_handler(text="refresh_game")
@dp.throttled(anti_flood, rate=2)
async def refresh(call: types.CallbackQuery):
    try:
        result = await get_game.game()
        keyboard = types.InlineKeyboardMarkup()
        buttons = [
        	types.InlineKeyboardButton(text="🌐Страница игры", url=result[2]),
            types.InlineKeyboardButton(text="🔄 Обновить", callback_data="refresh_game")]
        keyboard.add(*buttons)
        await bot.edit_message_media(inline_message_id=call.inline_message_id, media=InputMediaPhoto(result[3]))
        await bot.edit_message_caption(inline_message_id=call.inline_message_id, caption=f'🎮Случайная Coop игра под названием {result[0]}\n\nОписание: {result[1]}', reply_markup=keyboard)
    except Exception as e:
        print(e)

@dp.callback_query_handler(text="delete")
async def delete(call: types.CallbackQuery):
    await delete_message(call)

@dp.message_handler(commands="joke")
@dp.throttled(anti_flood,rate=2)
async def joke(message: types.Message):
    try:
        result = await get_joke.get_random_anecdote()
        keyboard = types.InlineKeyboardMarkup()
        buttons = [
            types.InlineKeyboardButton(text="🔄 Обновить", callback_data="update_joke"),
            types.InlineKeyboardButton(text="🗑 Удалить", callback_data="delete")
        ]
        keyboard.add(*buttons)
        await bot.send_message(
            message.chat.id,
            f"{result}",
            reply_markup=keyboard
        )
    except Exception as e:
        print(e)

@dp.message_handler(commands="fact")
@dp.throttled(anti_flood,rate=2)
async def joke(message: types.Message):
    try:
        result = await get_fact.random_fact()
        keyboard = types.InlineKeyboardMarkup()
        buttons = [
            types.InlineKeyboardButton(text="🔄 Обновить", callback_data="update_fact"),
            types.InlineKeyboardButton(text="🗑 Удалить", callback_data="delete")
        ]
        keyboard.add(*buttons)
        await bot.send_message(
            message.chat.id,
            f"{result}",
            reply_markup=keyboard
        )
    except Exception as e:
        print(e)

@dp.message_handler(commands="meme")
@dp.throttled(anti_flood,rate=2)
async def meme(message: types.Message):
    try:
        result = await get_meme.meme()
        keyboard = types.InlineKeyboardMarkup()
        buttons = [
            types.InlineKeyboardButton(text="🔄 Обновить", callback_data="update"),
            types.InlineKeyboardButton(text="🗑 Удалить", callback_data="delete")
        ]
        keyboard.add(*buttons)
        await bot.send_photo(
            message.chat.id,
            result,
            caption='🔮Лови мем',
            reply_markup=keyboard
        )
    except Exception as e:
        print(e)
        
@dp.message_handler(commands="coop")
@dp.throttled(anti_flood,rate=2)
async def meme(message: types.Message):
    try:
        result = await get_game.game()
        keyboard = types.InlineKeyboardMarkup()
        buttons = [
        	types.InlineKeyboardButton(text="🌐Страница игры", url=result[2]),
            types.InlineKeyboardButton(text="🔄 Обновить", callback_data="update_game"),
            types.InlineKeyboardButton(text="🗑 Удалить", callback_data="delete")
        ]
        keyboard.add(*buttons)
        await bot.send_photo(
            message.chat.id,
            result[3],
            caption=f'🎮Случайная Coop игра под названием {result[0]}\n\nОписание: {result[1]}',
            reply_markup=keyboard
        )
    except Exception as e:
        print(e)

@dp.callback_query_handler(text="update_joke")
@dp.throttled(anti_flood,rate=5)
async def update(call: types.CallbackQuery):
    try:
        result = await get_joke.get_random_anecdote()
        keyboard = types.InlineKeyboardMarkup()
        buttons = [
            types.InlineKeyboardButton(text="🔄 Обновить", callback_data="update_joke"),
            types.InlineKeyboardButton(text="🗑 Удалить", callback_data="delete")
        ]
        keyboard.add(*buttons)
        await call.message.edit_text(f"{result}", reply_markup=keyboard)
    except Exception as e:
        print(e)
        
@dp.callback_query_handler(text="update_fact")
@dp.throttled(anti_flood,rate=5)
async def update(call: types.CallbackQuery):
    try:
        result = await get_fact.random_fact()
        keyboard = types.InlineKeyboardMarkup()
        buttons = [
            types.InlineKeyboardButton(text="🔄 Обновить", callback_data="update_fact"),
            types.InlineKeyboardButton(text="🗑 Удалить", callback_data="delete")
        ]
        keyboard.add(*buttons)
        await call.message.edit_text(f"{result}", reply_markup=keyboard)
    except Exception as e:
        print(e)

@dp.callback_query_handler(text="update_game")
@dp.throttled(anti_flood,rate=5)
async def update(call: types.CallbackQuery):
    try:
        result = await get_game.game()
        keyboard = types.InlineKeyboardMarkup()
        buttons = [
        	types.InlineKeyboardButton(text="🌐Страница игры", url=result[2]),
            types.InlineKeyboardButton(text="🔄 Обновить", callback_data="update_game"),
            types.InlineKeyboardButton(text="🗑 Удалить", callback_data="delete")
        ]
        keyboard.add(*buttons)
        await call.message.edit_media(InputMediaPhoto(result[3]))
        await call.message.edit_caption(caption = f'🎮Случайная Coop игра под названием {result[0]}\n\nОписание: {result[1]}', reply_markup=keyboard)
    except Exception as e:
        print(e)

@dp.callback_query_handler(text="update")
@dp.throttled(anti_flood,rate=5)
async def update(call: types.CallbackQuery):
    try:
        result = await get_meme.meme()
        keyboard = types.InlineKeyboardMarkup()
        buttons = [
            types.InlineKeyboardButton(text="🔄 Обновить", callback_data="update"),
            types.InlineKeyboardButton(text="🗑 Удалить", callback_data="delete")
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
        print("Ошибка.\nОжидаем перезапуск 20 сек...")
        time.sleep(20)
