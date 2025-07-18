from enum import Enum


class CorrectResponse(Enum):
    OK = 200
    CREATED = 201

    @classmethod
    def is_correct(cls, status_code: int) -> bool:
        return status_code in {item.value for item in cls}
