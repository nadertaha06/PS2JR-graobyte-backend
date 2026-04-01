from pymongo import MongoClient
from app.config import Config

client = MongoClient(Config.MONGO_URI)
db = client['graobyte']

usuarios = db['usuarios']
produtos = db['produtos']