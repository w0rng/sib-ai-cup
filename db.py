from pymongo import MongoClient


data_base = MongoClient('localhost', 27017).sibHack
teams = data_base.Teams
bots = data_base.Bots


