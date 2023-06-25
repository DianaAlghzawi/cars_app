from datetime import date
from typing import Optional
from cars.infra.db.enumerations import CarBrand, ColorEnum
from pydantic import validator
from datetime import datetime
from cars.exception import ValidatorException
from pydantic import BaseModel
from uuid import UUID
import re


class Car_data(BaseModel):
    brand: CarBrand
    year: str
    price: float
    color: ColorEnum
    vin: str
    owner_id: Optional[UUID]

    @validator('vin')
    def validate_vin(cls, vin):
        pattern = r'^[A-Za-z0-9]{17}$'
        if not re.match(pattern, vin):
            raise ValidatorException.invalid_validator('Car', 'VIN must be a 17-character alphanumeric', vin)
        return vin

    @validator('price')
    def validate_price(cls, price):
        if price <= 0:
            raise ValidatorException.invalid_validator('Car', 'price', price)
        return price

    @validator('year')
    def validate_year(cls, year):
        try:
            year = datetime.strptime(year, '%Y').year
            if year > date.today().year:
                raise ValueError('Invalid year. Year cannot be in the future.')
            return str(year)
        except ValueError:
            raise ValueError('Invalid value for year or generation.')


class Supported_filters(BaseModel):
    brand: Optional[CarBrand]
    generation: Optional[str]
    year: Optional[str]
    min_price: Optional[float]
    max_price: Optional[float]

    @validator('max_price', 'min_price')
    def validate_prices_range(cls, value, field):
        if value and value <= 0:
            raise ValueError(f'Invalid {field}. {field} must be greater than zero.')
        return value

    @validator('year', 'generation')
    def validate_year(cls, year):
        if not year:
            return year
        try:
            if year := datetime.strptime(year, '%Y').year:
                return str(year)
        except ValueError:
            raise ValidatorException.invalid_validator('Car', 'year', year)


class Car_patch(BaseModel):
    brand: Optional[CarBrand]
    year: Optional[str]
    price: Optional[float]
    color: Optional[ColorEnum]
    vin: Optional[str]
    owner_id: Optional[UUID]

    @validator('vin')
    def validate_vin(cls, vin):
        pattern = r'^[A-Za-z0-9]{17}$'
        if vin and (not re.match(pattern, vin)):
            raise ValidatorException.invalid_validator('Car', 'VIN must be a 17-character alphanumeric', vin)
        return vin

    @validator('price')
    def validate_price(cls, price):
        if price and price <= 0:
            raise ValidatorException.invalid_validator('Car', 'price', price)
        return price

    @validator('year')
    def validate_year(cls, year):
        if not year:
            return year
        try:
            if year:
                year = datetime.strptime(year, '%Y').year
                if year > date.today().year:
                    raise ValueError('Invalid year. Year cannot be in the future.')
                return str(year)
        except ValueError:
            raise ValueError('Invalid value for year or generation.')
