from aiogram import types

from text import organizations


test_keyboards = list()
for key in organizations.keys():
    kb = types.InlineKeyboardMarkup()
    for org in organizations.get(key):
        index = organizations.get(key).index(org)
        kb.add(types.InlineKeyboardButton(org.get('name'), callback_data=f'{"_".join(key.split(" "))}_{index}'))
    test_keyboards.append(kb)

for i in range(len(test_keyboards)):
    if i != len(test_keyboards)-1:
        test_keyboards[i].add(types.InlineKeyboardButton('Далее', callback_data=f'next_{i}'))
    if i != 0:
        test_keyboards[i].add(types.InlineKeyboardButton('Назад', callback_data=f'back_{i}'))
