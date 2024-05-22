from typing import Annotated

from fastapi import APIRouter, status, Depends

from application.services.category_ad import get_category_ad_service, CategoryAdService
from application.services.user import UserService, get_user_service
from application.web.views.category_ad.schemas import CategoryOutput, CategoryInput

router = APIRouter(prefix="/category-advertisement",
                   tags=["CategoryAdvertisement"])


@router.get(path="/",
            summary="Получение категории объявления",
            status_code=status.HTTP_200_OK,
            response_model=CategoryOutput)
async def get_category_ad(category_service: Annotated[CategoryAdService, Depends(get_category_ad_service)],
                          category_oid: str) -> CategoryOutput:
    return await category_service.get_category_by_id(category_oid=category_oid)


@router.post(path="/",
             summary="Cоздание категории объявления",
             status_code=status.HTTP_201_CREATED,
             response_model=CategoryOutput)
async def add_category_ad(category_service: Annotated[CategoryAdService, Depends(get_category_ad_service)],
                          user_service: Annotated[UserService, Depends(get_user_service)],
                          category: CategoryInput) -> CategoryOutput:
    await user_service.check_role(role=("ADMIN",))
    return await category_service.create_category(category_schema=category)


@router.delete(path="/",
               summary="Удаление категории объявления",
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_category_ad(category_service: Annotated[CategoryAdService, Depends(get_category_ad_service)],
                             user_service: Annotated[UserService, Depends(get_user_service)],
                             category_oid: str) -> None:
    await user_service.check_role(role=("ADMIN",))
    return await category_service.delete_category_by_id(category_oid)
