from typing import Dict, Tuple, Any, Type, Optional, List
from sqlalchemy.engine import Dialect
import sqlalchemy as sa
from enum import Enum


class EnumNameValues(Enum):
    """
    Override Enum's auto values generation to make them being Enum's names instead of members.
    """
    @staticmethod
    def _generate_next_value_(name: str, start: int, count: int, last_values: List[Any]) -> str:
        return name


class StrEnumNameValues(str, EnumNameValues):
    pass


class StrEnum(sa.types.TypeDecorator[Enum]):
    """SQLAlchemy TypeDecorator so that we can store enums as strings in the database.
    By default, SQLAalchemy will store `.name` in the database, but we override this logic to
    allow us to reduce the use of casting to `EnumType(value)`, and reduce the use of the
    `.value` property when using the field elsewhere.
    """
    impl = sa.String

    cache_ok = True

    def __init__(self, enumtype: Type[Enum], args: Tuple[Any], *kwargs: Dict[str, Any]) -> None:
        super().__init__(*args, **kwargs)
        self._enumtype = enumtype

    # Alembic requires that `__repr__` return a constructor for this type that can be passed into
    # `eval()`.  The default implementation for `__repr__` does not do this well for custom types.
    def __repr__(self) -> str:
        return f'StrEnum({self._enumtype.__name__})'

    def process_bind_param(self, value: Optional[Enum], dialect: Dialect) -> Optional[str]:
        return value.value if value is not None else None

    def process_result_value(self, value: Optional[str], dialect: Dialect) -> Optional[Enum]:
        return self._enumtype(value) if value is not None else None


class Gender(StrEnumNameValues):
    Male: str = 'Male'
    Female: str = 'Female'


class CarBrand(StrEnumNameValues):
    TOYOTA : str = 'Toyota'
    KIA : str = 'Kia'
    HONDA : str = 'Honda'
    FORD : str = 'Ford'
    NISSAN : str = 'Nissan'
    MERCEDES_BENZ : str = 'Mercedes-Benz'
    AUDI : str = 'Audi'
    MAZDA : str = 'Mazda'


class ColorEnum(StrEnumNameValues):
    BLACK : str = "Black"
    WHITE : str = "White"
    SILVER : str = "Silver"
    GRAY : str = "Gray"
    RED : str = "Red"
    BLUE : str = "Blue"
    GREEN : str = "Green"
    YELLOW : str = "Yellow"
    ORANGE : str = "Orange"
    BROWN : str = "Brown"
    PURPLE : str = "Purple"
    GOLD : str = "Gold"
    BRONZE : str = "Bronze"
    PINK : str = "Pink"


class StatesEnum(StrEnumNameValues):
    Amman = "Amman"
    Aqaba = "Aqaba"
    Balqa = "Balqa"
    Irbid = "Irbid"
    Jerash = "Jerash"
    Karak = "Karak"
    Maan = "Ma'an"
    Madaba = "Madaba"
    Mafraq = "Mafraq"
    Tafilah = "Tafilah"
    Zarqa = "Zarqa"
    Ajloun = "Ajloun"
