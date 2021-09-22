import os

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
    await bot.send_message(chat_id=message.from_user.id, text=messages.get('start'), reply_markup=kb.start)
    await message.answer(messages.get('welcome'), reply_markup=kb.welcome)
    await shutdown(dp)


@dp.callback_query_handler(lambda c: c.data == 'welcome')
async def welcome_question_ask(callback_query: types.CallbackQuery):
    await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id,
                                text=messages['question'], reply_markup=kb.question)


@dp.callback_query_handler(lambda c: c.data == 'where')
async def fair_schema(callback_query: types.CallbackQuery):
    image = types.InputFile('images', 'where.jpg')
    await bot.send_photo(chat_id=callback_query.from_user.id, photo=image)


@dp.callback_query_handler(lambda c: c.data == 'master_class')
async def master_class(callback_query: types.CallbackQuery):
    text = 'Успей подать заявку на первые встречи со Студенческими организациями ДВФУ!'
    back_kb = types.InlineKeyboardMarkup()
    back_kb.add(types.InlineKeyboardButton('Ссылка на регистрацию', url='https://vk.com/away.php?to=https%3A%2F'
                                                                        '%2Fdocs.google.com%2Fforms%2Fd%2Fe'
                                                                        '%2F1FAIpQLSe41SL3EJsROLWtco7K2ACsX339S'
                                                                        'yIKn2mIiLE_0Yjch81lFQ%2Fviewform&cc_key='))
    image = types.InputFile('images', filename='schedule.jpg')
    await bot.send_photo(chat_id=callback_query.from_user.id, photo=image, reply_markup=back_kb)


@dp.callback_query_handler(lambda c: c.data in ('wrong', 'right'))
async def get_question_answer(callback_query: types.CallbackQuery):
    data = callback_query.data
    await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id,
                                text=messages[data], reply_markup=kb.direction_list)


@dp.callback_query_handler(lambda c: ' '.join(c.data.split('_')) in organizations.keys())
async def organizations_list(callback_query: types.CallbackQuery):
    text = organizations.get(' '.join(callback_query.data.split('_')))[-1].get('name')
    text += '\n\n' + organizations.get(' '.join(callback_query.data.split('_')))[-1].get('description')
    await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id,
                                text=text, reply_markup=kb.organization_list[' '.join(callback_query.data.split('_'))])


@dp.callback_query_handler(lambda c: 'back' in c.data or 'return' in c.data)
async def go_back(callback_query: types.CallbackQuery):
    if callback_query.data == 'return':
        await bot.edit_message_text(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id,
                                    text=messages.get('start'), reply_markup=kb.start)
        await bot.edit_message_media(chat_id=callback_query.from_user.id, message_id=callback_query.message.message_id,
                                     media=None)
    if callback_query.data != 'back':
        data = callback_query.data.replace('back_', '')
        text = organizations.get(' '.join(data.split('_')))[-1].get('description')
        keyboard = kb.organization_list.get(' '.join(data.split('_')))
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
