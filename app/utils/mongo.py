import os

from motor.motor_asyncio import AsyncIOMotorClient

DATABASE_NAME = os.environ.get("MONGO_DATABASE", "ddang")

client = AsyncIOMotorClient()
db = client[DATABASE_NAME]
