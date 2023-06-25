from pydantic import BaseModel, validator
from cars.infra.db.enumerations import Gender, StatesEnum
from typing import Optional
from cars.exception import ValidatorException
from datetime import date
import re


class Owner_data(BaseModel):
    first_name: str
    middle_name: Optional[str]
    last_name: str
    state: StatesEnum
    zip: str
    gender: Gender
    national_number: str
    birthdate: date

    @validator('first_name')
    def validate_firs_name(cls, first_name):
        pattern = '^[A-Za-z ]+$'
        if first_name and (len(first_name) < 3 or (not re.match(pattern, first_name))):
            raise ValidatorException.invalid_validator('Owner', 'first name', first_name)
        return first_name

    @validator('last_name')
    def validate_last_name(cls, last_name):
        pattern = '^[A-Za-z ]+$'
        if last_name and (len(last_name) < 3 or (not re.match(pattern, last_name))):
            raise ValidatorException.invalid_validator('last', 'last name', last_name)
        return last_name.capitalize()

    @validator('middle_name')
    def validate_middle_name(cls, middle_name):
        pattern = '^[A-Za-z ]+$'
        if middle_name:
            if (len(middle_name) < 3 or (not re.match(pattern, middle_name))):
                raise ValidatorException.invalid_validator('Owner', 'middle name', middle_name)
            return middle_name.capitalize()

    @validator('zip')
    def validate_zip(cls, zip_code):
        if not zip_code.isdigit() or len(zip_code) != 5:
            raise ValidatorException.invalid_validator('Owner', 'ZIP', zip_code)
        return zip_code

    @validator('national_number')
    def validate_national_number(cls, national_number):
        if not national_number.isdigit() or len(national_number) != 10:
            raise ValidatorException.invalid_validator('Owner', 'national number', national_number)
        return national_number

    @validator('birthdate')
    def validate_birthdate(cls, birthdate):
        try:
            date.strftime(birthdate, '%yyyy-%mm-%dd')
        except ValueError:
            raise ValueError('Invalid birthdate. The birthdate must be in the format YYYY-MM-DD.')
        if birthdate > date.today():
            raise ValueError('Invalid birthdate. The birthdate cannot be in the future.')

        return birthdate

    @validator('state', 'gender')
    def validate_enum(cls, str_enum):
        return str_enum.capitalize()


class Supported_filters(BaseModel):
    cars_count: Optional[int]
    state: Optional[StatesEnum]
    zip: Optional[str]
    gender: Optional[Gender]
    age: Optional[int]

    @validator('zip')
    def validate_zip(cls, zip_code):
        if zip_code:
            if not zip_code.isdigit() or len(zip_code) != 5:
                raise ValidatorException.invalid_validator('Owner', 'ZIP', zip_code)
            return zip_code

    @validator('age')
    def validate_age(cls, value):
        if value:
            if (value == 0) or (value < 18):
                raise ValidatorException.invalid_validator('Owner', 'age', value)
            return value

    @validator('cars_count')
    def validate_cars_count(cls, value):
        if value:
            if (value == 0) or (value < 1):
                raise ValidatorException.invalid_validator('Owner', 'cars count', value)
            return value


class Owner_patch(BaseModel):
    first_name: Optional[str]
    middle_name: Optional[str]
    last_name: Optional[str]
    state: Optional[StatesEnum]
    zip: Optional[str]
    gender: Optional[Gender]
    national_number: Optional[str]
    birthdate: Optional[date]

    @validator('first_name')
    def validate_firs_name(cls, first_name):
        pattern = '^[A-Za-z ]+$'
        if first_name and (len(first_name) < 3 or (not re.match(pattern, first_name))):
            raise ValidatorException.invalid_validator('Owner', 'first name', first_name)
        return first_name

    @validator('last_name')
    def validate_last_name(cls, last_name):
        pattern = '^[A-Za-z ]+$'
        if last_name:
            if len(last_name) < 3 or (not re.match(pattern, last_name)):
                raise ValidatorException.invalid_validator('last', 'last name', last_name)
            last_name = last_name.capitalize()
        return last_name

    @validator('middle_name')
    def validate_middle_name(cls, middle_name):
        pattern = '^[A-Za-z ]+$'
        if middle_name:
            middle_name = middle_name.capitalize()
            if (len(middle_name) < 3 or (not re.match(pattern, middle_name))):
                raise ValidatorException.invalid_validator('Owner', 'middle name', middle_name)
        return middle_name

    @validator('zip')
    def validate_zip(cls, zip_code):
        if zip_code and (not zip_code.isdigit() or len(zip_code) != 5):
            raise ValidatorException.invalid_validator('Owner', 'ZIP', zip)
        return zip_code

    @validator('national_number')
    def validate_national_number(cls, national_number):
        if national_number and (not national_number.isdigit() or len(national_number) != 10):
            raise ValidatorException.invalid_validator('Owner', 'national number', national_number)
        return national_number

    @validator('birthdate')
    def validate_birthdate(cls, birthdate):
        try:
            if birthdate:
                date.strftime(birthdate, '%yyyy-%mm-%dd')
        except ValueError:
            raise ValueError('Invalid birthdate. The birthdate must be in the format YYYY-MM-DD.')

        if birthdate and birthdate > date.today():
            raise ValueError('Invalid birthdate. The birthdate cannot be in the future.')

        return birthdate

    @validator('state', 'gender')
    def validate_enum(cls, str_enum):
        if str_enum:
            return str_enum.capitalize()
        return str_enum
