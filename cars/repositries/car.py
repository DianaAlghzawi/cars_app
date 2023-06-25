from uuid import UUID
from sqlalchemy.engine import Connection
from sqlalchemy import select, exc, insert as sa_insert, update as sa_update, delete as sa_delete
from cars.infra.db.schema import cars
from cars.exception import ModelNotFoundException, ModelFoundException
from cars.data_models.car_schemas import Supported_filters, Car_patch, Car_data
from fastapi import Depends
from typing import Optional
from dataclasses import dataclass
from cars.infra.db.enumerations import CarBrand, ColorEnum
from datetime import datetime


@dataclass
class Car:
    id: UUID
    brand: CarBrand
    year: str
    price: float
    color: ColorEnum
    vin: str
    owner_id: Optional[UUID]
    created_at: datetime
    updated_at: datetime


def get_by_fillter(conn: Connection, car_filter: Supported_filters = Depends(Supported_filters)) -> list[Car]:
    query = select(cars)

    if car_filter.brand:
        query = query.filter(car_filter.brand == cars.c.brand)

    if car_filter.year:
        query = query.filter(cars.c.year.__ge__(car_filter.year))

    if car_filter.generation:
        decade_start = int(car_filter.generation[:3] + '0') - 1
        decade_end = decade_start + 9
        query = query.filter(cars.c.year.between(f'{decade_start}0', f'{decade_end}9'))

    if car_filter.min_price:
        query = query.filter(cars.c.price >= car_filter.min_price)

    if car_filter.max_price:
        query = query.filter(cars.c.price < car_filter.max_price)

    result = conn.execute(query).fetchall()
    return [Car(**car._asdict()) for car in result]


def get_by_id(conn: Connection, id: UUID) -> Car:
    if car := conn.execute(cars.select().where(cars.c.id == id)).fetchone():
        return Car(**car._asdict())
    raise ModelNotFoundException('Car', id)


def insert(conn: Connection, entered_data: Car_data = Depends(Car_data)) -> Optional[Car | None]:
    try:
        if car_info := conn.execute(sa_insert(cars).values(**entered_data.dict()).returning(cars)).fetchone():
            return Car(**car_info._asdict())

    except exc.SQLAlchemyError:
        raise ModelFoundException.already_found('Cars', entered_data.vin)
    return None


def delete(conn: Connection, id: UUID) -> None:
    if not conn.execute(sa_delete(cars).where(cars.c.id == id)).rowcount:
        raise ModelNotFoundException('Car', id)


def patch(conn: Connection, id: UUID, car: Car_patch = Depends(Car_patch)) -> Optional[Car | None]:
    try:
        if updated_car := ((get_by_id(conn, id).__dict__) | car.dict(exclude_none=True)):
            updated_car_info = conn.execute(sa_update(cars).where(cars.c.id == id).values(updated_car).returning(cars)).fetchone()
            return Car(**updated_car_info._asdict())
    except exc.SQLAlchemyError:
        raise ModelNotFoundException('Car', id)
    return None
