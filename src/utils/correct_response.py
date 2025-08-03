from enum import Enum


class CorrectResponse(Enum):
    OK = 200
    CREATED = 201

    @classmethod
    def is_correct(cls, status_code: str | int | float | dict[str, str | float | int]) -> bool:
        if not isinstance(status_code, int):
            raise TypeError("Argument 'status_code' must be an integer")
        return status_code in {item.value for item in cls}
