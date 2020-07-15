import json

USERS_FILENAME = './app/users.json'

with open(USERS_FILENAME) as file:
    users = json.load(file)
