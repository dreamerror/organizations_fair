import json


with open('organizations.json', 'r', encoding='utf-8') as orgs:
    organizations = json.loads('\n'.join(orgs.readlines()))

with open('messages.json', 'r', encoding='utf-8') as msgs:
    messages = json.loads('\n'.join(msgs.readlines()))
