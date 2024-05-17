from typing import Any

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
            category = await self.uow.category.get(category_oid)
            if category:
                return category.to_schema()

            raise CategoryNotFoundError

    async def delete_category_by_id(self, category_oid: str) -> None:
        await self.get_category_by_id(category_oid)
        async with self.uow:
            await self.uow.category.delete(category_oid)
            await self.uow.commit()

    async def create_category(self, category_schema: CategoryInput) -> CategoryOutput:
        async with self.uow:
            params_search = {"title": category_schema.title}
            exist_category: CategoryOutput = await self.check_existing_category(params_search)
            if exist_category:
                raise CategoryAlreadyExistsError

            category_entity: DomainCategory = DomainCategory.to_entity(category_schema)
            await self.uow.category.add(category_entity)
            await self.uow.commit()
            return category_entity.to_schema()

    async def check_existing_category(self, params: dict[str, Any]) -> CategoryOutput:
        async with self.uow:
            exist_category = await self.uow.category.get_by_params(params)
            return exist_category.to_schema()


category_ad = CategoryAdService()
