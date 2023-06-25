from fastapi import APIRouter, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from cars.infra.db.engine import engine
from cars.repositries import owner
from uuid import UUID
from typing import Optional
from cars.data_models.owner_schemas import Supported_filters, Owner_patch, Owner_data

owner_router = APIRouter(
    prefix='/owners',
    tags=['Owners']
)


@owner_router.get('/')
async def get_by_filter(owner_filter: Optional[Supported_filters] = Depends(Supported_filters)) -> JSONResponse:
    with engine.connect() as conn:
        owner_info = owner.get_by_fillter(conn, owner_filter)
        return JSONResponse(content=jsonable_encoder(owner_info), status_code=status.HTTP_200_OK)


@owner_router.get('/{id}')
async def get_by_id(id: UUID) -> JSONResponse:
    with engine.connect() as conn:
        owner_info = owner.get_by_id(conn, id)
        return JSONResponse(content=jsonable_encoder(owner_info), status_code=status.HTTP_200_OK)


@owner_router.get('/{id}/cars')
async def get_owner_cars_by_id(id: UUID) -> JSONResponse:
    with engine.connect() as conn:
        owner_cars = owner.get_owner_cars_by_id(conn, id)
        return JSONResponse(content=jsonable_encoder(owner_cars), status_code=status.HTTP_200_OK)


@owner_router.post('/')
async def insert(owner_data: Owner_data = Depends(Owner_data)) -> JSONResponse:
    with engine.connect() as conn:
        owner_info = owner.insert(conn, owner_data)
        return JSONResponse(content=jsonable_encoder(owner_info), status_code=status.HTTP_201_CREATED)


@owner_router.delete('/{id}')
async def delete(id: UUID) -> JSONResponse:
    with engine.begin() as conn:
        owner.delete(conn, id)
        return JSONResponse(content=jsonable_encoder({'Messsage': 'Owner had been deleted successfully'}),
                            status_code=status.HTTP_204_NO_CONTENT)


@owner_router.delete('/{owner_id}/cars/{car_id}')
async def delete_owner_car_by_id(owner_id: UUID, car_id: UUID) -> JSONResponse:
    with engine.begin() as conn:
        owner.delete_owner_car_by_id(conn, owner_id, car_id)
        return JSONResponse(content=jsonable_encoder({'Messsage': 'Owner had been deleted successfully'}),
                            status_code=status.HTTP_204_NO_CONTENT)


@owner_router.patch('/')
async def patch(id: UUID, owner_patch: Owner_patch = Depends(Owner_patch)) -> JSONResponse:
    with engine.begin() as conn:
        patched_owner = owner.patch(conn, id, owner_patch)
        return JSONResponse(content=jsonable_encoder(patched_owner), status_code=status.HTTP_200_OK)
