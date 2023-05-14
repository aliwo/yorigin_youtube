from app.entities.collections.category.category_codes import CategoryCode
from app.entities.collections.category.category_collection import category_collection
from app.entities.collections.geo_json import GeoJsonPolygon
from app.entities.collections.shop.shop_collection import shop_collection
from app.entities.collections.shop.shop_document import ShopDeliveryAreaDocument
from app.services.category_service import get_home_categories_one_by_one


async def test_one_by_one() -> None:
    # given
    await category_collection.insert_one(CategoryCode.CHICKEN, "치킨", "test_url", "test_link", 10)
    await category_collection.insert_one(CategoryCode.BURGER, "버거", "test_url", "test_link", 10)
    await category_collection.insert_one(CategoryCode.PIZZA, "피자", "test_url", "test_link", 10)

    await shop_collection.insert_one(
        "치킨집",
        [CategoryCode.CHICKEN],
        [ShopDeliveryAreaDocument(poly=GeoJsonPolygon(coordinates=[[[0, 0], [0, 10], [10, 10], [10, 0], [0, 0]]]))],
    )

    # when
    categories = await get_home_categories_one_by_one(5, 5)

    # then
    assert CategoryCode.CHICKEN.value in categories
    assert CategoryCode.BURGER.value not in categories
