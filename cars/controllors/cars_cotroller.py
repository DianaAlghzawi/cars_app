from fastapi import APIRouter, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from cars.infra.db.engine import engine
from cars.repositries import car
from uuid import UUID
from cars.data_models.car_schemas import Supported_filters, Car_patch, Car_data


cars_router = APIRouter(
    prefix='/cars',
    tags=['Cars']
)


@cars_router.get('/')
def get_by_fillter(car_filter: Supported_filters = Depends(Supported_filters)) -> JSONResponse:
    with engine.connect() as conn:
        return JSONResponse(content=jsonable_encoder(car.get_by_fillter(conn, car_filter))
                            , status_code=status.HTTP_200_OK)


@cars_router.get('/{id}')
async def get_by_id(id: UUID) -> JSONResponse:
    with engine.connect() as conn:
        return JSONResponse(content=jsonable_encoder(car.get_by_id(conn, id)), status_code=status.HTTP_200_OK)


@cars_router.post('/')
async def insert(car_data: Car_data = Depends(Car_data)) -> JSONResponse:
    with engine.begin() as conn:
        car_info = car.insert(conn, car_data)
        return JSONResponse(content=jsonable_encoder(car_info), status_code=status.HTTP_201_CREATED)


@cars_router.delete('/{id}')
async def delete(id: UUID) -> JSONResponse:
    with engine.begin() as conn:
        car.delete(conn, id)
        return JSONResponse(content=jsonable_encoder({'Messsage': 'Owner had been deleted successfully'}),
                            status_code=status.HTTP_204_NO_CONTENT)


@cars_router.patch('/')
async def patch(id: UUID, patch_car: Car_patch = Depends(Car_patch)) -> JSONResponse:
    with engine.begin() as conn:
        return JSONResponse(content=jsonable_encoder(car.patch(conn, id, patch_car)), status_code=status.HTTP_200_OK)
