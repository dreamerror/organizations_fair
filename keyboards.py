import json

from aiogram import types


with open('organizations.json', 'r', encoding='utf-8') as orgs:
    organizations = json.loads('\n'.join(orgs.readlines()))
