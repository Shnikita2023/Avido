from typing import Any, Optional

from application.domain.entities.category_ad import Category as DomainCategory
from application.exceptions.domain import CategoryNotFoundError, CategoryAlreadyExistsError
from application.infrastructure.unit_of_work_manager import get_unit_of_work
from application.repos.uow.unit_of_work import AbstractUnitOfWork
from application.web.views.category_ad.schemas import CategoryOutput, CategoryInput


class CategoryAdService:

    uow: AbstractUnitOfWork

    def __init__(self, uow=None):
        self.uow = uow if uow else get_unit_of_work()

    async def get_category_by_id(self, category_oid: str) -> CategoryOutput:
        async with self.uow:
            category: DomainCategory | None = await self.uow.category.get(category_oid)
            if category:
                return CategoryOutput.to_schema(category)

            raise CategoryNotFoundError

    async def delete_category_by_id(self, category_oid: str) -> None:
        await self.get_category_by_id(category_oid)
        async with self.uow:
            await self.uow.category.delete(category_oid)
            await self.uow.commit()

    async def create_category(self, category_schema: CategoryInput) -> CategoryOutput:
        async with self.uow:
            params_search = {"title": category_schema.title}
            exist_category: Optional[CategoryOutput] = await self.check_existing_category(params_search)
            if exist_category:
                raise CategoryAlreadyExistsError

            category: DomainCategory = category_schema.to_domain()
            await self.uow.category.add(category)
            await self.uow.commit()
            return CategoryOutput.to_schema(category)

    async def check_existing_category(self, params: dict[str, Any]) -> Optional[CategoryOutput]:
        async with self.uow:
            exist_category: DomainCategory | None = await self.uow.category.get_by_params(params)
            if exist_category:
                return CategoryOutput.to_schema(exist_category)


def get_category_ad_service() -> CategoryAdService:
    return CategoryAdService()
