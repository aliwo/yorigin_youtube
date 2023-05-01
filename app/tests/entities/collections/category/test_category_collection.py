import pytest
from pymongo.errors import DuplicateKeyError

from app.entities.collections.category.category_codes import CategoryCode
from app.entities.collections.category.category_collection import category_collection


async def test_create_chicken_category() -> None:
    # Given
    await category_collection.insert_one(
        code=CategoryCode.CHICKEN, name="치킨", image_url="test_url", deep_link="test_link", priority=10
    )

    # When
    chicken = await category_collection.find_by_code(CategoryCode.CHICKEN)

    # Then
    assert chicken.code == "chicken"
    assert chicken.name == "치킨"


async def test_category_code_should_be_unique() -> None:
    # Given
    await category_collection.insert_one(
        code=CategoryCode.CHICKEN, name="치킨", image_url="test_url", deep_link="test_link", priority=10
    )

    # Expect
    with pytest.raises(DuplicateKeyError):
        await category_collection.insert_one(
            code=CategoryCode.CHICKEN, name="치킨2", image_url="test_url", deep_link="test_link", priority=10
        )
