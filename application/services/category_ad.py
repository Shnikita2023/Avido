from uuid import UUID

from application.domain.category_ad.category_ad import Category as DomainCategory
from application.exceptions.domain import CategoryNotFoundError, CategoryAlreadyExistsError
from application.infrastructure.unit_of_work_manager import get_unit_of_work
from application.services.uof.unit_of_work import AbstractUnitOfWork
from application.web.views.category_ad.schemas import CategoryOutput, CategoryInput


class CategoryAdService:

    uow: AbstractUnitOfWork

    def __init__(self, uow=None):
        self.uow = uow if uow else get_unit_of_work()

    async def get_category_by_id(self, category_oid: UUID) -> CategoryOutput:
        async with self.uow:
            category_ad = await self.uow.category.get(category_oid)
            if category_ad:
                return category_ad

            raise CategoryNotFoundError

    async def delete_category_by_id(self, category_oid: UUID) -> None:
        await self.get_category_by_id(category_oid)
        async with self.uow:
            await self.uow.category.delete(category_oid)
            await self.uow.commit()

    async def create_category(self, data: CategoryInput) -> CategoryOutput:
        async with self.uow:
            await self._check_existing_category(title=data.title)
            category_entity: DomainCategory = DomainCategory.to_entity(data)
            await self.uow.category.add(category_entity)
            await self.uow.commit()
            return category_entity

    async def _check_existing_category(self, title: str) -> None:
        params = {"title": title}
        fields = ("title",)
        category = await self.uow.category.get_by_params(params, fields)
        if category:
            raise CategoryAlreadyExistsError


category_ad = CategoryAdService()
