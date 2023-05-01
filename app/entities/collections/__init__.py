from app.entities.collections.category.category_collection import category_collection
from app.entities.collections.shop.shop_collection import shop_collection


async def set_indexes() -> None:
    await category_collection.set_index()
    await shop_collection.set_index()
