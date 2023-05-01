import dataclasses

from fastapi import APIRouter, Query
from fastapi.responses import ORJSONResponse

from app.entities.collections.category.category_codes import CategoryCode
from app.services.category_service import (
    get_distinct_home_categories,
    get_home_categories_one_by_one,
)

router = APIRouter(prefix="/v1/home_categories", tags=["Home Category"], redirect_slashes=False)


@dataclasses.dataclass
class CategoryResponse:
    categories: list[CategoryCode]


@router.get(
    "/one_by_one",
    description="카테고리 하나당 limit 1 짜리 count_documents 쿼리를 날려서 카테고리 목록을 구합니다.",
    response_class=ORJSONResponse,
)
async def one_by_one(
    longitude: float = Query(..., example=127.005926),
    latitude: float = Query(..., example=37.49006),
) -> CategoryResponse:
    return CategoryResponse(categories=await get_home_categories_one_by_one(longitude, latitude))


@router.get(
    "/distinct",
    description="distinct 쿼리를 날려서 카테고리 목록을 구합니다.",
    response_class=ORJSONResponse,
)
async def distinct(
    longitude: float = Query(..., example=127.005926),
    latitude: float = Query(..., example=37.49006),
) -> CategoryResponse:
    return CategoryResponse(categories=await get_distinct_home_categories(longitude, latitude))
