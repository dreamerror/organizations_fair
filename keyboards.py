from aiogram import types

from text import organizations


welcome = types.InlineKeyboardMarkup()
welcome.add(types.InlineKeyboardButton('Конечно!', callback_data='welcome'))
welcome.add(types.InlineKeyboardButton('Да, давай!', callback_data='welcome'))

question = types.InlineKeyboardMarkup()
question.add(types.InlineKeyboardButton('10', callback_data='wrong'))
question.add(types.InlineKeyboardButton('28', callback_data='wrong'))
question.add(types.InlineKeyboardButton('30', callback_data='wrong'))
question.add(types.InlineKeyboardButton('Больше 50', callback_data='right'))

direction_list = types.InlineKeyboardMarkup()
direction_list.add(types.InlineKeyboardButton('Студенческое самоуправление', callback_data='self_management'))
direction_list.add(types.InlineKeyboardButton('Наука', callback_data='science'))
direction_list.add(types.InlineKeyboardButton('Киберспорт и программирование', callback_data='IT_and_cybersport'))
direction_list.add(types.InlineKeyboardButton('Просвещение', callback_data='enlightenment'))
direction_list.add(types.InlineKeyboardButton('Творчество', callback_data='art'))
direction_list.add(types.InlineKeyboardButton('Спорт и туризм', callback_data='sports_and_tourism'))
direction_list.add(types.InlineKeyboardButton('Личные качества', callback_data='personal_qualities'))
direction_list.add(types.InlineKeyboardButton('Медиа сообщества', callback_data='media'))
direction_list.add(types.InlineKeyboardButton('Игры', callback_data='games'))
direction_list.add(types.InlineKeyboardButton('Международное развитие', callback_data='international'))
direction_list.add(types.InlineKeyboardButton('Волонтёрское движение', callback_data='volunteer'))
direction_list.add(types.InlineKeyboardButton('Другое', callback_data='other'))

organization_list = dict()
all_orgs = dict()
for direction in direction_list['inline_keyboard']:
    kb = types.InlineKeyboardMarkup()
    key = ' '.join(direction[0]['callback_data'].split('_'))
    for org in organizations.get(key):
        index = organizations.get(key).index(org)
        all_orgs[index] = key
        if org.get('url'):
            kb.add(types.InlineKeyboardButton(org.get('name'), callback_data=f'{"_".join(key.split(" "))}_{index}'))
    organization_list[key] = kb