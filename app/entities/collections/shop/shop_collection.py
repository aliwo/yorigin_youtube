from dataclasses import asdict
from typing import Any

import pymongo
from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorDatabase

from app.entities.collections.category.category_codes import CategoryCode
from app.entities.collections.geo_json import GeoJsonPoint
from app.entities.collections.shop.shop_document import (
    ShopDeliveryAreaDocument,
    ShopDocument,
)
from app.utils.mongo import db


class ShopCollection:
    def __init__(self, db: AsyncIOMotorDatabase):
        self._collection = AsyncIOMotorCollection(db, "shops")

    async def set_index(self) -> None:
        await self._collection.create_index(
            [
                ("delivery_areas.poly", pymongo.GEOSPHERE),
                ("category_codes", pymongo.ASCENDING),
            ]
        )
        await self._collection.create_index([("delivery_areas.poly", pymongo.GEOSPHERE)])

    async def point_intersects(self, point: GeoJsonPoint) -> list[ShopDocument]:
        return [
            self._parse(result)
            for result in await self._collection.find(
                {"delivery_areas": {"$elemMatch": {"poly": {"$geoIntersects": {"$geometry": asdict(point)}}}}}
            ).to_list(length=None)
        ]

    async def exists_by_category_and_point_intersects(self, category_code: CategoryCode, point: GeoJsonPoint) -> bool:
        cnt = await self._collection.count_documents(
            {
                "category_codes": category_code,
                "delivery_areas": {"$elemMatch": {"poly": {"$geoIntersects": {"$geometry": asdict(point)}}}},
            },
            limit=1,
        )
        return bool(cnt)

    async def get_distinct_category_codes_by_point_intersects(self, point: GeoJsonPoint) -> list[CategoryCode]:
        return [
            CategoryCode(category_code)
            for category_code in await self._collection.distinct(
                "category_codes",
                {"delivery_areas": {"$elemMatch": {"poly": {"$geoIntersects": {"$geometry": asdict(point)}}}}},
            )
        ]

    async def insert_one(
        self, name: str, category_codes: list[CategoryCode], delivery_areas: list[ShopDeliveryAreaDocument]
    ) -> ShopDocument:
        result = await self._collection.insert_one(
            {
                "name": name,
                "category_codes": category_codes,
                "delivery_areas": [asdict(delivery_area) for delivery_area in delivery_areas],
            }
        )
        return ShopDocument(
            _id=result.inserted_id,
            name=name,
            category_codes=category_codes,
            delivery_areas=delivery_areas,
        )

    def _parse(self, result: dict[Any, Any]) -> ShopDocument:
        delivery_areas = [ShopDeliveryAreaDocument(**delivery_area) for delivery_area in result.pop("delivery_areas")]
        return ShopDocument(
            delivery_areas=delivery_areas,
            **result,
        )


shop_collection = ShopCollection(db)
