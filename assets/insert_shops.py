import asyncio
import json
import os

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection

DATABASE_NAME = os.environ.get("MONGO_DATABASE", "ddang")

client = AsyncIOMotorClient()
db = client[DATABASE_NAME]
shop_collection = AsyncIOMotorCollection(db, "shops")


async def insert_all() -> None:
    """
    프로젝트 root 에서 실행하세요
    :return:
    """
    for filename in os.listdir("assets/shops"):
        if not os.path.isfile(f"assets/shops/{filename}"):
            continue
        with open(f"assets/shops/{filename}") as f:
            data = json.load(f)
            await shop_collection.insert_many(data)
            print(f"{filename} inserted")

    for filename in os.listdir("assets/shops/majesta"):
        if not os.path.isfile(f"assets/shops/majesta/{filename}"):
            continue
        with open(f"assets/shops/majesta/{filename}") as f:
            data = json.load(f)
            await shop_collection.insert_many(data)
            print(f"{filename} inserted")


asyncio.run(insert_all())
