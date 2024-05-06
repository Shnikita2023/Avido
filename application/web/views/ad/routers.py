from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from application.exceptions.base import ApplicationException
from application.services.ad import advertisement_service
from application.web.views.ad.schemas import AdvertisementOutput, AdvertisementInput, AdvertisementInputUpdate

router = APIRouter(prefix="/Advertisement",
                   tags=["Advertisement"])


@router.get(path="/",
            summary="Получение объявления",
            status_code=status.HTTP_200_OK,
            response_model=AdvertisementOutput)
async def get_advertisement(advertisement_oid: UUID) -> AdvertisementOutput:
    try:
        return await advertisement_service.get_advertisement_by_id(advertisement_oid=advertisement_oid)

    except ApplicationException as ex:
        raise HTTPException(status_code=400, detail=ex.message)


@router.post(path="/",
             summary="Cоздание объявления",
             status_code=status.HTTP_201_CREATED,
             response_model=AdvertisementOutput)
async def add_advertisement(advertisement: AdvertisementInput) -> AdvertisementOutput:
    try:
        return await advertisement_service.create_advertisement(data=advertisement)

    except ApplicationException as ex:
        raise HTTPException(status_code=400, detail=ex.message)


@router.patch(path="/",
              summary="Редактирование объявления",
              status_code=status.HTTP_200_OK,
              response_model=AdvertisementOutput)
async def update_advertisement(advertisement_oid: UUID,
                               new_advertisement: AdvertisementInputUpdate) -> AdvertisementOutput:
    try:
        return await advertisement_service.update_partial_advertisement_by_id(advertisement_oid, new_advertisement)

    except ApplicationException as ex:
        raise HTTPException(status_code=400, detail=ex.message)


@router.delete(path="/",
               summary="Cнятие объявления",
               status_code=status.HTTP_204_NO_CONTENT)
async def delete_advertisement(advertisement_oid: UUID) -> None:
    try:
        return await advertisement_service.delete_advertisement_by_id(advertisement_oid)

    except ApplicationException as ex:
        raise HTTPException(status_code=400, detail=ex.message)
