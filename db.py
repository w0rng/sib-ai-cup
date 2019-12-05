from pymongo import MongoClient
from bot import Bot


client = MongoClient('localhost', 27017)
data_base = client.sibHack
bots = data_base.Bots


def register(name: str):
    if bots.count_documents({'name': name}) == 0:
        bot = Bot(name)
        bots.insert_one(bot.dict_())
        return f'Good!\nToken is {bot.token}'
    else:
        return 'Error'


def get_bots():
    result = ''
    for bot in bots.find():
        result.join({
            'name': bot["name"],
            'coords': bot["coords"],
            'color': bot["color"]
        })
    return result
