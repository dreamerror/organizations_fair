import os
import pytz
from datetime import datetime, tzinfo

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import keyboards as kb
from text import organizations, messages

TOKEN = os.getenv('TOKEN')
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['start'])
async def start_message(message: types.Message):
    now = pytz.utc.localize(datetime.now())
    if now <= datetime(2021, 9, 23, 18, 0, 0, 0, tzinfo=pytz.timezone('Asia/Vladivostok')):
        await bot.send_message(message.from_user.id, text='23 сентября с 15:00 до 18:00 на '
                                                          'спортивных площадках кампуса '
                                                          'двфу пройдёт ярмарка студенческих организаций. '
                                                          'Мы приглашаем тебя! До встречи!')
    await message.answer(messages.get('welcome'), reply_markup=kb.welcome)
    await shutdown(dp)


@dp.callback_query_handler(lambda c: c.data == 'welcome')
async def welcome_question_ask(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id,
                                text=messages['question'], reply_markup=kb.question)


@dp.callback_query_handler(lambda c: c.data in ('wrong', 'right'))
async def get_question_answer(callback_query: types.CallbackQuery):
    data = callback_query.data
    await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id,
                                text=messages[data], reply_markup=kb.direction_list)


@dp.callback_query_handler(lambda c: ' '.join(c.data.split('_')) in organizations.keys())
async def organizations_list(callback_query: types.CallbackQuery):
    keyboard = kb.organization_list[' '.join(callback_query.data.split('_'))]
    text = organizations.get(' '.join(callback_query.data.split('_')))[-1].get('name')
    text += '\n\n' + organizations.get(' '.join(callback_query.data.split('_')))[-1].get('description')
    await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id,
                                text=text, reply_markup=kb.organization_list[' '.join(callback_query.data.split('_'))])


@dp.callback_query_handler(lambda c: 'back' in c.data)
async def go_back(callback_query: types.CallbackQuery):
    if callback_query.data != 'back':
        data = callback_query.data.replace('back_', '')
        text = organizations.get(' '.join(data.split('_')))[-1].get('description')
        keyboard = kb.organization_list.get(text)
        await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id,
                                    text=text, reply_markup=keyboard)
    else:
        await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id,
                                    text='Список направлений', reply_markup=kb.direction_list)


@dp.callback_query_handler(lambda c: ' '.join(c.data.split('_')[:-1]) in organizations.keys())
async def show_organisation(callback_query: types.CallbackQuery):
    index = int(callback_query.data.split('_')[-1])
    org = kb.organizations.get(' '.join(callback_query.data.split('_')[:-1]))[index]
    direction = '_'.join(callback_query.data.split('_')[:-1])
    new_kb = types.InlineKeyboardMarkup()
    new_kb.add(types.InlineKeyboardButton('Страница организации', callback_data='org', url=org.get('url')))
    new_kb.add(types.InlineKeyboardButton('Назад', callback_data=f'back_{direction}'))
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
