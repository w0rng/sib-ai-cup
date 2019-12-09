from hashlib import sha256
from random import randint
from db import TEAMS, BOTS, FOOD
from time import sleep

import json

# Генерация токена
def get_token(team_name: str, password: str) -> str:
    team_name = team_name.lower()
    pass_and_salt = password + team_name[::-2]
    token = sha256(str.encode(pass_and_salt)).hexdigest()[:16]

    if TEAMS.count_documents({'name': team_name}) == 0:
        __registration_team(team_name, token)
        __registration_bot(team_name)
        return token
    elif TEAMS.count_documents({'name': team_name, 'token': token}) == 1:
        return token
    else:
        return 'Error'


def get_BOTS(private_api: bool = False) -> str:
    result = []
    for bot in BOTS.find():
        result.append({
            'score': bot['score'],
            'coordinate': bot['coordinate']
        })
        if private_api:
            result[-1].update({'name': bot['name']})
            result[-1].update({'color': bot['color']})
    return json.dumps(result)


def add_food():
    while 1:
        print("add food")
        sleep(5)


def bot_move(token: str, x: int, y: int) -> None:
    if abs(x) > 40 or abs(y) > 40:
        return 'Ошибка! Слишком большое расстояние.'

    team_name = __get_team_name(token)
    if (team_name):
        return 'Ошибка! Не верный токен'

    bot = BOTS.find_one({'name': team_name})

    new_x = (bot['coordinate']['x'] + x) % 1920
    new_y = (bot['coordinate']['y'] + y) % 1080

    
    BOTS.update_one({'name': team_name}, {'$set': {
        "coordinate" : {
            'x': new_x,
            'y': new_y
        }}})
    return 'good'

def get_coordinate(token: str) -> None:
    team_name = __get_team_name(token)
    if (team_name):
        return 'Ошибка! Не верный токен'

    bot = BOTS.find_one({'name': team_name})
    return json.dumps({
        'x': bot['coordinate']['x'],
        'y': bot['coordinate']['y']
    })


def __get_team_name(token: str) -> str:
    team = TEAMS.find_one({'token': token})
    return team.get('name')

def __registration_team(team_name: str, token: str) -> None:
    TEAMS.insert_one({
        'name': team_name,
        'token': token
    })

def __registration_bot(team_name: str) -> None:
    BOTS.insert_one({
        'name': team_name,
        'score': 0,
        'color': {
            'r': randint(0, 200),
            'g': randint(0, 200),
            'b': randint(0, 200)
        },
        'coordinate': {
            'x': randint(0, 1920),
            'y': randint(0, 1080)
        }

    })