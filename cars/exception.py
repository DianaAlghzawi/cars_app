from uuid import UUID


class ModelNotFoundException(Exception):
    def __init__(self, name: str, id: UUID):
        self.content = f'Model: {name} with id:{id} not found'


class ModelFoundException(Exception):
    def __init__(self, message):
        self.message = message

    @classmethod
    def already_found(cls, name: str, vin: str):
        content = f"Model: {name} with {vin} already found"
        return cls(content)


class ValidatorException(Exception):
    def __init__(self, message):
        self.message = message

    @classmethod
    def invalid_validator(cls, name: str, exception: str, value: str):
        content = f"Model: {name} with {exception}: {value} is invalid"
        return cls(content)

    @classmethod
    def invalid_list_validator(cls, name: str, exception: str, list_values: list):
        content = f"Model: {name} Invalid. Allowed {exception} are: {', '.join(list_values)}"
        return cls(content)
