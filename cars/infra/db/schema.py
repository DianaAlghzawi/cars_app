from sqlalchemy import Table, String, DateTime, Float, Column, text, ForeignKey, UniqueConstraint, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import UUID
import sqlalchemy as sa
from datetime import datetime
from cars.infra.db.engine import metadata

new_uuid = text('uuid_generate_v4()')
now = datetime.utcnow()
default_now = dict(default=now, server_default=sa.func.now())


owner = Table(
    'owner',
    metadata,
    Column('id', UUID(as_uuid=True), nullable=False, server_default=new_uuid),
    Column('first_name', String, nullable=False),
    Column('middle_name', String),
    Column('last_name', String, nullable=False),
    Column('national_number', String, nullable=False),
    Column('state', String, nullable=False),
    Column('zip', String, nullable=False),
    Column('gender', String, nullable=False),
    Column('birthdate', DateTime, nullable=False),
    Column('created_at', DateTime, nullable=False, default=now, server_default=sa.func.now()),
    Column('updated_at', DateTime, nullable=True, onupdate=now, default=now, server_default=sa.func.now()),
    PrimaryKeyConstraint("id", name="owner_pk"),
    UniqueConstraint('national_number', name='national_number'),
)

cars = Table(
    'cars',
    metadata,
    Column('id', UUID(as_uuid=True), nullable=False, server_default=new_uuid),
    Column('owner_id', UUID(as_uuid=True), ForeignKey('owner.id')),
    Column('brand', String, nullable=False),
    Column('year', String, nullable=False),
    Column('price', Float, nullable=False),
    Column('color', String, nullable=False),
    Column('vin', String, nullable=False),
    Column('created_at', DateTime, nullable=False, default=now, server_default=sa.func.now()),
    Column('updated_at', DateTime, nullable=True, onupdate=now, default=now, server_default=sa.func.now()),
    PrimaryKeyConstraint("id", name="car_pk"),
    UniqueConstraint('vin', name='vin_key'),
)
