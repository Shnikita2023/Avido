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
    category = await category_service.get_category_by_id(category_oid=category_oid)
    return CategoryOutput.to_schema(category)


@router.post(path="/",
             summary="Cоздание категории объявления",
             status_code=status.HTTP_201_CREATED,
             response_model=CategoryOutput)
async def add_category_ad(category_service: Annotated[CategoryAdService, Depends(get_category_ad_service)],
                          user_service: Annotated[UserService, Depends(get_user_service)],
                          category_schema: CategoryInput) -> CategoryOutput:
    # user_service.check_user_role_allowed(role=("ADMIN",))
    category = await category_service.create_category(category=category_schema.to_domain())
    return CategoryOutput.to_schema(category)


@router.delete(path="/",
               summary="Удаление категории объявления",
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_category_ad(category_service: Annotated[CategoryAdService, Depends(get_category_ad_service)],
                             user_service: Annotated[UserService, Depends(get_user_service)],
                             category_oid: str) -> None:
    user_service.check_user_role_allowed(role=("ADMIN",))
    return await category_service.delete_category_by_id(category_oid)
