from hashlib import sha256
from random import randint
from db import teams, bots
import json

# Генерация токена
def get_token(team_name: str, password: str) -> str:
    team_name = team_name.lower()
    pass_and_salt = password + team_name[::-2]
    token = sha256(str.encode(pass_and_salt)).hexdigest()[:16]

    if teams.count_documents({'name': team_name}) == 0:
        __registration_team(team_name, token)
        __registration_bot(team_name)
        return token
    elif teams.count_documents({'name': team_name, 'token': token}) == 1:
        return token
    else:
        return 'Error'


def get_bots(private_api: bool = False) -> str:
    result = []
    for bot in bots.find():
        result.append({
            'score': bot['score'],
            'coordinate': bot['coordinate']
        })
        if private_api:
            result[-1].update({'name': bot['name']})
            result[-1].update({'color': bot['color']})
    return json.dumps(result)


def bot_move(token: str, x: int, y: int) -> None:
    team = teams.find_one({'token': token})
    if team is None:
        return 'Error! Не верный токен.'

    bot = bots.find_one({'name': team['name']})
    if abs(x) > 40 or abs(y) > 40:
        return 'Error! Слишком большое расстояние.'

    new_x = (bot['coordinate']['x'] + x) % 1920
    new_y = (bot['coordinate']['y'] + y) % 1080

    
    bots.update_one({'name': team['name']}, {'$set': {
        "coordinate" : {
            'x': new_x,
            'y': new_y
        }}})
    return 'good'

def get_coordinate(token: str) -> None:
    team = teams.find_one({'token': token})
    if team is None:
        return 'Error! Не верный токен.'

    bot = bots.find_one({'name': team['name']})
    return json.dumps({
        'x': bot['coordinate']['x'],
        'y': bot['coordinate']['y']
    })


def __registration_team(team_name: str, token: str) -> None:
    teams.insert_one({
        'name': team_name,
        'token': token
    })

def __registration_bot(team_name: str) -> None:
    bots.insert_one({
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