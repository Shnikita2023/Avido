from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from application.services.category_ad import CategoryAdService
from application.exceptions.base import ApplicationException
from application.web.views.category_ad.schemas import CategoryOutput, CategoryInput

router = APIRouter(prefix="/CategoryAdvertisement",
                   tags=["CategoryAdvertisement"])


@router.get(path="/",
            summary="Получение категории объявления",
            status_code=status.HTTP_200_OK,
            response_model=CategoryOutput)
async def get_category_ad(category_oid: UUID) -> CategoryOutput:
    try:
        return await CategoryAdService().get_category_by_id(category_oid=category_oid)

    except ApplicationException as ex:
        raise HTTPException(status_code=400, detail=ex.message)


@router.post(path="/",
             summary="Cоздание категории объявления",
             status_code=status.HTTP_201_CREATED,
             response_model=CategoryOutput)
async def add_category_ad(category_ad: CategoryInput) -> CategoryOutput:
    return await CategoryAdService().create_category(data=category_ad)


@router.delete(path="/",
               summary="Удаление категории объявления",
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_category_ad(category_oid: UUID) -> None:
    try:
        return await CategoryAdService().delete_category_by_id(category_oid)

    except ApplicationException as ex:
        raise HTTPException(status_code=400, detail=ex.message)
