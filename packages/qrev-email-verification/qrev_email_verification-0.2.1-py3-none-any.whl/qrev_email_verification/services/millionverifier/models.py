from enum import IntEnum
from typing import Optional, Union

from pydantic import BaseModel, Field
from qrev_email_verification.models.models import InvalidEmailError as BaseEmailError

class ResultCodeEnum(IntEnum):
    # 1 : Ok,
    # 2: catch_all,
    # 3 : Unknown,
    # 4 : Error,
    # 5 : Disposable,
    # 6 : Invalid,

    OK = 1
    CATCH_ALL = 2
    UNKNOWN = 3
    ERROR = 4
    DISPOSABLE = 5
    INVALID = 6

    @classmethod
    def _missing_(cls, value):
        if isinstance(value, str):
            try:
                return cls[value.upper()]
            except KeyError:
                raise ValueError(f"Invalid string value: {value}")
        elif isinstance(value, ResultCodeEnum):
            return value
        else:
            raise ValueError(f"Invalid value: {value}")

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class EmailResponse(BaseModel):
    email: str
    quality: str
    result: str
    resultcode: ResultCodeEnum
    subresult: str
    free: bool
    role: bool
    didyoumean: str | None = None
    error: str
    livemode: bool
    executiontime: Optional[int] = Field(default=None)
    credits: Optional[int] = Field(default=None)
    service: str = "MillionVerifier"


class InvalidEmailError(BaseEmailError):
    pass