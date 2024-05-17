from fastapi import APIRouter, status

from application.services.category_ad import category_ad
from application.web.views.category_ad.schemas import CategoryOutput, CategoryInput

router = APIRouter(prefix="/CategoryAdvertisement",
                   tags=["CategoryAdvertisement"])


@router.get(path="/",
            summary="Получение категории объявления",
            status_code=status.HTTP_200_OK,
            response_model=CategoryOutput)
async def get_category_ad(category_oid: str) -> CategoryOutput:
    return await category_ad.get_category_by_id(category_oid=category_oid)


@router.post(path="/",
             summary="Cоздание категории объявления",
             status_code=status.HTTP_201_CREATED,
             response_model=CategoryOutput)
async def add_category_ad(category: CategoryInput) -> CategoryOutput:
    return await category_ad.create_category(category_schema=category)


@router.delete(path="/",
               summary="Удаление категории объявления",
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_category_ad(category_oid: str) -> None:
    return await category_ad.delete_category_by_id(category_oid)
