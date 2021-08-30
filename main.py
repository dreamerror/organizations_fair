import os
import json

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import keyboards as kb

TOKEN = os.getenv('TOKEN')
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    await message.answer('Список организаций', reply_markup=kb.test_keyboards[0])
    await shutdown(dp)


@dp.callback_query_handler(lambda c: 'next' in c.data)
async def next_page(callback_query: types.CallbackQuery):
    index = int(callback_query.data.split('_')[-1])
    await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id,
                                text=callback_query.message.text, reply_markup=kb.test_keyboards[index + 1])
    await shutdown(dp)


@dp.callback_query_handler(lambda c: 'back' in c.data)
async def prev_page(callback_query: types.CallbackQuery):
    if len(callback_query.data.split('_')) == 1:
        await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id,
                                    text='Список организаций', reply_markup=kb.test_keyboards[0])
    else:
        index = int(callback_query.data.split('_')[-1])
        await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id,
                                    text=callback_query.message.text, reply_markup=kb.test_keyboards[index - 1])
    await shutdown(dp)


@dp.callback_query_handler(lambda c: ' '.join(c.data.split('_')[:-1]) in kb.organizations.keys())
async def show_organisation(callback_query: types.CallbackQuery):
    index = int(callback_query.data.split('_')[-1])
    org = kb.organizations.get(' '.join(callback_query.data.split('_')[:-1]))[index]
    new_kb = types.InlineKeyboardMarkup()
    new_kb.add(types.InlineKeyboardButton('Страница организации', callback_data='org', url=org.get('url')))
    new_kb.add(types.InlineKeyboardButton('Назад', callback_data='back'))
    new_text = f'{org.get("name")}'
    if org.get('description'):
        new_text += f'\n\n{org.get("description")}'
    await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id,
                                text=new_text, reply_markup=new_kb)
    await shutdown(dp)


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


if __name__ == '__main__':
    executor.start_polling(dp, on_shutdown=shutdown)
