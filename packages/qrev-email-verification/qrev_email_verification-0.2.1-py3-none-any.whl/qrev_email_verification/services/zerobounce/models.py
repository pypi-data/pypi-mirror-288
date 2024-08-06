from datetime import datetime
from enum import StrEnum
from typing import Optional

from pydantic import BaseModel, Field, field_serializer

from qrev_email_verification.models.models import InvalidEmailError as BaseEmailError


class ResultStatusEnum(StrEnum):
    """
    https://www.zerobounce.net/docs/email-validation-api-quickstart/#status_codes__v2__
    """
    VALID = "valid"
    INVALID = "invalid"
    CATCH_ALL = "catch-all"
    SPAMTRAP = "spamtrap"
    ABUSE = "abuse"
    DO_NOT_MAIL = "do_not_mail"
    UNKNOWN = "unknown"

    def __str__(self):
        return self.value

    def __repr__(self):
        return self.value

    def __eq__(self, o) -> bool:
        if isinstance(o, str):
            return self.value == o.lower()
        return super().__eq__(o)

    def __hash__(self) -> int:
        return hash(self.value)


class EmailResponse(BaseModel):
    email: Optional[str] = None
    account: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    did_you_mean: Optional[str] = None
    domain: Optional[str] = None
    domain_age_days: Optional[int] = None
    firstname: Optional[str] = None
    free_email: Optional[bool] = None
    gender: Optional[str] = None
    lastname: Optional[str] = None
    mx_found: Optional[bool] = None
    mx_record: Optional[str] = None
    processed_at: Optional[datetime] = None
    region: Optional[str] = None
    smtp_provider: Optional[str] = None
    status: Optional[str] = None
    sub_status: Optional[str] = None
    verified: Optional[bool] = None
    zipcode: Optional[str] = None
    resultcode: Optional[int] = None
    error: Optional[str] = None
    service: str = "ZeroBounce"


class InvalidEmailError(BaseEmailError):
    pass