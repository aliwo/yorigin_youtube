import asyncio
import os

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from shapely import union_all
from shapely.geometry import mapping, shape

from app.entities.collections.category.category_codes import CategoryCode
from app.entities.collections.category_area.category_area_collection import (
    category_area_collection,
)
from app.entities.collections.geo_json import GeoJsonPolygon

DATABASE_NAME = os.environ.get("MONGO_DATABASE", "ddang")

client = AsyncIOMotorClient()
db = client[DATABASE_NAME]
shop_collection = AsyncIOMotorCollection(db, "shops")


async def insert_category_area(category_code: CategoryCode) -> None:
    to_union = []
    async for shop in shop_collection.find({"category_codes": category_code}):
        for area in shop["delivery_areas"]:
            to_union.append(shape(area["poly"]))

    multi_polygon = union_all(to_union)

    await category_area_collection.insert_one(category_code, poly=GeoJsonPolygon(**mapping(multi_polygon)))


async def loop_all_categories_and_insert_category_area() -> None:
    for category_code in CategoryCode:
        await insert_category_area(category_code)
        print(category_code, "inserted")


asyncio.run(loop_all_categories_and_insert_category_area())
