from pymongo import MongoClient


DATA_BASE = MongoClient('localhost', 27017).sibHack
TEAMS = DATA_BASE.Teams
BOTS = DATA_BASE.Bots
FOOD = DATA_BASE.Food

