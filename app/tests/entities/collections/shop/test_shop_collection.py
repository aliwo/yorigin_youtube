import asyncio

from app.entities.collections.category.category_codes import CategoryCode
from app.entities.collections.geo_json import GeoJsonPoint, GeoJsonPolygon
from app.entities.collections.shop.shop_collection import shop_collection
from app.entities.collections.shop.shop_document import ShopDeliveryAreaDoc


async def test_shop_point_intersects() -> None:
    # Given
    await asyncio.gather(
        shop_collection.insert_one(
            "치킨집",
            [CategoryCode.CHICKEN],
            [
                ShopDeliveryAreaDoc(
                    poly=GeoJsonPolygon(coordinates=[[[0, 0], [0, 10], [10, 10], [10, 0], [0, 0]]]),
                )
            ],
        ),
        shop_collection.insert_one(
            "피자집",
            [CategoryCode.PIZZA],
            [
                ShopDeliveryAreaDoc(
                    poly=GeoJsonPolygon(coordinates=[[[0, 0], [0, 2], [2, 2], [2, 0], [0, 0]]]),
                )
            ],
        ),
    )

    # When
    result = await shop_collection.point_intersects(GeoJsonPoint(coordinates=[5, 5]))

    # Then
    assert len(result) == 1
    assert result[0].name == "치킨집"


async def test_shop_point_intersects_when_it_has_multiple_delivery_area() -> None:
    # Given
    await asyncio.gather(
        shop_collection.insert_one(
            "치킨집",
            [CategoryCode.CHICKEN],
            [
                ShopDeliveryAreaDoc(
                    poly=GeoJsonPolygon(coordinates=[[[0, 0], [0, 10], [10, 10], [10, 0], [0, 0]]]),
                ),
                ShopDeliveryAreaDoc(
                    poly=GeoJsonPolygon(coordinates=[[[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]]]),
                ),
            ],
        ),
        shop_collection.insert_one(
            "피자집",
            [CategoryCode.PIZZA],
            [
                ShopDeliveryAreaDoc(
                    poly=GeoJsonPolygon(coordinates=[[[0, 0], [0, 2], [2, 2], [2, 0], [0, 0]]]),
                ),
            ],
        ),
    )

    # When
    result = await shop_collection.point_intersects(GeoJsonPoint(coordinates=[5, 5]))

    # Then
    assert len(result) == 1
    assert result[0].name == "치킨집"


async def test_shop_exists_by_category_and_point_intersects_when_it_has_multiple_delivery_area() -> None:
    # Given
    await asyncio.gather(
        shop_collection.insert_one(
            "치킨집",
            [CategoryCode.CHICKEN],
            [
                ShopDeliveryAreaDoc(
                    poly=GeoJsonPolygon(coordinates=[[[0, 0], [0, 10], [10, 10], [10, 0], [0, 0]]]),
                ),
                ShopDeliveryAreaDoc(
                    poly=GeoJsonPolygon(coordinates=[[[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]]]),
                ),
            ],
        ),
        shop_collection.insert_one(
            "피자집",
            [CategoryCode.PIZZA],
            [
                ShopDeliveryAreaDoc(
                    poly=GeoJsonPolygon(coordinates=[[[0, 0], [0, 2], [2, 2], [2, 0], [0, 0]]]),
                ),
            ],
        ),
    )

    # When
    found = await shop_collection.exists_by_category_and_point_intersects(
        CategoryCode.CHICKEN, GeoJsonPoint(coordinates=[5, 5])
    )
    not_found = await shop_collection.exists_by_category_and_point_intersects(
        CategoryCode.PIZZA, GeoJsonPoint(coordinates=[5, 5])
    )

    # Then
    assert found is True
    assert not_found is False


async def test_shop_get_distinct_category_codes_by_point_intersects() -> None:
    # Given
    await asyncio.gather(
        shop_collection.insert_one(
            "치킨집",
            [CategoryCode.CHICKEN],
            [
                ShopDeliveryAreaDoc(
                    poly=GeoJsonPolygon(coordinates=[[[0, 0], [0, 10], [10, 10], [10, 0], [0, 0]]]),
                ),
                ShopDeliveryAreaDoc(
                    poly=GeoJsonPolygon(coordinates=[[[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]]]),
                ),
            ],
        ),
        shop_collection.insert_one(
            "치킨집2",
            [CategoryCode.CHICKEN],
            [
                ShopDeliveryAreaDoc(
                    poly=GeoJsonPolygon(coordinates=[[[0, 0], [0, 9], [9, 9], [9, 0], [0, 0]]]),
                ),
                ShopDeliveryAreaDoc(
                    poly=GeoJsonPolygon(coordinates=[[[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]]]),
                ),
            ],
        ),
        shop_collection.insert_one(
            "피자집",
            [CategoryCode.PIZZA],
            [
                ShopDeliveryAreaDoc(
                    poly=GeoJsonPolygon(coordinates=[[[0, 0], [0, 2], [2, 2], [2, 0], [0, 0]]]),
                ),
            ],
        ),
        shop_collection.insert_one(
            "버거집",
            [CategoryCode.BURGER],
            [
                ShopDeliveryAreaDoc(
                    poly=GeoJsonPolygon(coordinates=[[[0, 0], [0, 9], [9, 9], [9, 0], [0, 0]]]),
                ),
            ],
        ),
    )

    # When
    result_codes = await shop_collection.get_distinct_category_codes_by_point_intersects(
        GeoJsonPoint(coordinates=[5, 5])
    )

    # Then
    assert all(code in result_codes for code in [CategoryCode.CHICKEN, CategoryCode.BURGER])


async def test_shop_get_get_category_codes_by_facet() -> None:
    # Given
    await asyncio.gather(
        shop_collection.insert_one(
            "치킨집",
            [CategoryCode.CHICKEN],
            [
                ShopDeliveryAreaDoc(
                    poly=GeoJsonPolygon(coordinates=[[[0, 0], [0, 10], [10, 10], [10, 0], [0, 0]]]),
                ),
                ShopDeliveryAreaDoc(
                    poly=GeoJsonPolygon(coordinates=[[[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]]]),
                ),
            ],
        ),
        shop_collection.insert_one(
            "치킨집2",
            [CategoryCode.CHICKEN],
            [
                ShopDeliveryAreaDoc(
                    poly=GeoJsonPolygon(coordinates=[[[0, 0], [0, 9], [9, 9], [9, 0], [0, 0]]]),
                ),
                ShopDeliveryAreaDoc(
                    poly=GeoJsonPolygon(coordinates=[[[0, 0], [0, 1], [1, 1], [1, 0], [0, 0]]]),
                ),
            ],
        ),
        shop_collection.insert_one(
            "피자집",
            [CategoryCode.PIZZA],
            [
                ShopDeliveryAreaDoc(
                    poly=GeoJsonPolygon(coordinates=[[[0, 0], [0, 2], [2, 2], [2, 0], [0, 0]]]),
                ),
            ],
        ),
        shop_collection.insert_one(
            "버거집",
            [CategoryCode.BURGER],
            [
                ShopDeliveryAreaDoc(
                    poly=GeoJsonPolygon(coordinates=[[[0, 0], [0, 9], [9, 9], [9, 0], [0, 0]]]),
                ),
            ],
        ),
    )

    # When
    result_codes = await shop_collection.get_category_codes_by_facet(GeoJsonPoint(coordinates=[5, 5]))

    # Then
    assert all(code in result_codes for code in [CategoryCode.CHICKEN, CategoryCode.BURGER])
