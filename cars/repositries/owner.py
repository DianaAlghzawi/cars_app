from uuid import UUID
from datetime import date, datetime
from sqlalchemy.engine import Connection
from sqlalchemy import extract, func, select, exc, insert as sa_insert, update as sa_update, delete as sa_delete
from cars.infra.db.schema import owner
from typing import Optional
from cars.exception import ModelFoundException, ModelNotFoundException
from cars.data_models.owner_schemas import Supported_filters, Owner_patch, Owner_data
from fastapi import Depends
from cars.infra.db.schema import cars
from cars.repositries.car import Car
from cars.infra.db.enumerations import StatesEnum, Gender
from dataclasses import dataclass


@dataclass
class Owner:
    id: UUID
    first_name: str
    middle_name: Optional[str]
    last_name: str
    state: StatesEnum
    zip: str
    gender: Gender
    national_number: str
    birthdate: date
    created_at: datetime
    updated_at: datetime


def get_by_id(conn: Connection, id: UUID) -> Owner:
    if owner_info := conn.execute(select(owner).where(owner.c.id == id)).fetchone():
        return Owner(**owner_info._asdict())
    raise ModelNotFoundException('Owner', id)


def get_by_fillter(conn: Connection, owner_filter: Supported_filters = Depends(Supported_filters)) -> list[Owner]:
    query = select(owner)

    if owner_filter.cars_count:
        owners_filterd_with_cars_count = conn.execute(select(cars.c.owner_id).
                                                      group_by(cars.c.owner_id).
                                                      having(func.count() >= owner_filter.cars_count)).fetchall()
        owner_ids = list(map(lambda x: x[0], owners_filterd_with_cars_count))
        query = query.where(owner.c.id.in_(owner_ids))

    if owner_filter.age:
        query = query.filter(extract('year', date.today()) - extract('year', owner.c.birthdate) == owner_filter.age)

    if owner_filter.zip:
        query = query.filter(owner.c.zip == owner_filter.zip)

    if owner_filter.state:
        query = query.filter(owner.c.state == owner_filter.state)

    if owner_filter.gender:
        query = query.filter(owner.c.gender == owner_filter.gender)

    result = conn.execute(query).fetchall()
    return [Owner(**car._asdict()) for car in result]


def get_owner_cars_by_id(conn: Connection, id: UUID) -> list[Car]:
    try:
        owner_cars = conn.execute(select(cars).where(cars.c.owner_id == id)).fetchall()
        return [Car(**car._asdict()) for car in owner_cars]
    except exc.SQLAlchemyError:
        raise ModelNotFoundException('Owner', id)


def insert(conn: Connection, owner_data: Owner_data = Depends(Owner_data)) -> Optional[Owner | None]:
    try:
        if owner_info := conn.execute(sa_insert(owner).values(**owner_data.dict()).returning(owner)).fetchone():
            return Owner(**owner_info._asdict())
    except exc.SQLAlchemyError:
        raise ModelFoundException.already_found('Owner', owner_data.national_number)
    return None


def delete(conn: Connection, id: UUID) -> None:
    if not conn.execute(sa_delete(owner).where(owner.c.id == id)).rowcount:
        raise ModelNotFoundException('Owner', id)


def delete_owner_car_by_id(conn: Connection, owner_id: UUID, car_id: UUID) -> None:
    if owner_cars_count := conn.execute(select(cars.c.owner_id).where(cars.c.owner_id == owner_id)).rowcount:
        if not conn.execute(sa_delete(cars).where((cars.c.owner_id == owner_id) & (cars.c.id == car_id))).rowcount:
            raise ModelNotFoundException('Car', car_id)
        if owner_cars_count == 1:
            conn.execute(sa_delete(owner).where(owner.c.id == owner_id))
        return None
    raise ModelNotFoundException('Owner', owner_id)


def patch(conn: Connection, id: UUID, owner_patch: Owner_patch = Depends(Owner_patch)) -> Owner:
    if updated_owner := (get_by_id(conn, id).__dict__) | owner_patch.dict(exclude_none=True):
        updated_owner_info = conn.execute(sa_update(owner).where(owner.c.id == id).values(updated_owner)
                                          .returning(owner)).fetchone()
        return Owner(**updated_owner_info._asdict())
    raise ModelNotFoundException('Owner', id)
