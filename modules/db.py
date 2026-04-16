from motor.motor_asyncio import AsyncIOMotorClient
from config import MONGO_URL

mongo = AsyncIOMotorClient(MONGO_URL)
db = mongo.userbot

users = db.users
ranks = db.ranks
warns = db.warns
groups = db.groups
