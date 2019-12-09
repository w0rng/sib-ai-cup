import requests
from time import sleep
from random import randint

TOKEN = '19d148725126211c'
URL = 'http://127.0.0.1:5000/'

while 1:
    x, y = randint(-40, 40), randint(-40, 40)
    requests.post(URL + 'move', data={'token': TOKEN, 'x': x, 'y': y})
    sleep(0.1)
