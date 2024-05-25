from typing import Any, Optional

from application.domain.entities.category_ad import Category as DomainCategory
from application.exceptions.domain import CategoryNotFoundError, CategoryAlreadyExistsError
from application.infrastructure.unit_of_work_manager import get_unit_of_work
from application.repos.uow.unit_of_work import AbstractUnitOfWork


class CategoryAdService:

    uow: AbstractUnitOfWork

    def __init__(self, uow=None):
        self.uow = uow if uow else get_unit_of_work()

    async def get_category_by_id(self, category_oid: str) -> DomainCategory:
        async with self.uow:
            category: DomainCategory | None = await self.uow.category.get(category_oid)
            if category:
                return category

            raise CategoryNotFoundError

    async def delete_category_by_id(self, category_oid: str) -> None:
        await self.get_category_by_id(category_oid)
        async with self.uow:
            await self.uow.category.delete(category_oid)
            await self.uow.commit()

    async def create_category(self, category: DomainCategory) -> DomainCategory:
        async with self.uow:
            params_search = {"title": category.title}
            exist_category: Optional[DomainCategory] = await self.check_existing_category(params_search)
            if exist_category:
                raise CategoryAlreadyExistsError

            await self.uow.category.add(category)
            await self.uow.commit()
            return category

    async def check_existing_category(self, params: dict[str, Any]) -> Optional[DomainCategory]:
        async with self.uow:
            exist_category: DomainCategory | None = await self.uow.category.get_by_params(params)
            if exist_category:
                return exist_category


def get_category_ad_service() -> CategoryAdService:
    return CategoryAdService()
