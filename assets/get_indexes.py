import asyncio

from motor.motor_asyncio import AsyncIOMotorCollection

from app.utils.mongo import db

shop_collection = AsyncIOMotorCollection(db, "shops")
category_area_collection = AsyncIOMotorCollection(db, "category_areas")


async def get_indexes() -> None:
    print("shop_collection")
    for son in await shop_collection.list_indexes().to_list(length=None):
        print(son)
    print("category_areas_collection")
    for son in await category_area_collection.list_indexes().to_list(length=None):
        print(son)


asyncio.run(get_indexes())
