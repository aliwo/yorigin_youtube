from dataclasses import asdict

from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorDatabase

from app.entities.collections.category.category_codes import CategoryCode
from app.entities.collections.category.category_document import CategoryDocument
from app.utils.mongo import db


class CategoryCollection:
    def __init__(self, db: AsyncIOMotorDatabase):
        self._collection = AsyncIOMotorCollection(db, "categories")

    async def set_index(self) -> None:
        await self._collection.create_index("code", unique=True)

    async def find_all(self) -> list[CategoryDocument]:
        return [CategoryDocument(**category) for category in await self._collection.find().to_list(length=None)]

    async def find_by_code(self, code: CategoryCode) -> CategoryDocument:
        found = await self._collection.find_one({"code": code})
        return CategoryDocument(**found)

    async def insert_one(
        self,
        code: CategoryCode,
        name: str,
        image_url: str,
        deep_link: str,
        priority: int,
    ) -> CategoryDocument:
        result = await self._collection.insert_one(
            {
                "code": code,
                "name": name,
                "image_url": image_url,
                "deep_link": deep_link,
                "priority": priority,
            }
        )
        return CategoryDocument(
            _id=result.inserted_id, code=code, name=name, image_url=image_url, deep_link=deep_link, priority=priority
        )

    async def upsert_one(self, category: CategoryDocument) -> None:
        to_update = asdict(category)
        del to_update["_id"]
        await self._collection.update_one(
            {"code": to_update.pop("code")},
            {"$set": to_update},
            upsert=True,
        )


category_collection = CategoryCollection(db)
