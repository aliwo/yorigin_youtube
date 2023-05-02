import asyncio

from app.entities.collections.category.category_codes import CategoryCode
from app.entities.collections.geo_json import GeoJsonPoint
from app.entities.collections.shop.shop_collection import shop_collection


async def get_home_categories_one_by_one(lng: float, lat: float) -> list[CategoryCode]:
    li = [
        shop_collection.exists_by_category_and_point_intersects(code, GeoJsonPoint(coordinates=[lng, lat]))
        for code in CategoryCode
    ]
    results = {code: exists for code, exists in zip(CategoryCode, await asyncio.gather(*li))}

    return [CategoryCode(code) for code, exists in results.items() if exists]


async def get_distinct_home_categories(lng: float, lat: float) -> list[CategoryCode]:
    cnt = await shop_collection._collection.count_documents({})
    result = await shop_collection.get_distinct_category_codes_by_point_intersects(GeoJsonPoint(coordinates=[lng, lat]))
    return result
