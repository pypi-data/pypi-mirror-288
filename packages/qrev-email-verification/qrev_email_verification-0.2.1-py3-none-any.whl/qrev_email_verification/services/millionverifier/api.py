from dataclasses import dataclass, field
from typing import Any, Optional, Type, TypeVar, cast

import requests
from pydantic_settings import BaseSettings, SettingsConfigDict

from qrev_email_verification import APIResponse
from qrev_email_verification.email_verifying_service import EmailVerifyingService
from qrev_email_verification.services.millionverifier.models import (
    EmailResponse,
    InvalidEmailError,
    ResultCodeEnum,
)


class MillionVerifierSettings(BaseSettings):
    api_key: str = ""
    valid_includes: set[ResultCodeEnum] = field(
        default_factory=lambda: set([ResultCodeEnum.OK, ResultCodeEnum.CATCH_ALL])
    )
    url: str = "https://api.millionverifier.com/api/v3/"

    model_config = SettingsConfigDict(env_prefix="MILLIONVERIFIER_")


T = TypeVar("T", bound=BaseSettings)


@dataclass
class MillionVerifierService(EmailVerifyingService):
    """
    Response Example:
    {
    "email": "bademail@gmal.com",
    "quality": "good",
    "result": "invalid",
    "resultcode": 6,
    "subresult": "unknown",
    "free": false,
    "role": false,
    "didyoumean": "bademail@gmail.com",
    "credits": 3454,
    "executiontime": 2,
    "error": "",
    "livemode": true
    }

    resultcode:
    1 : Ok,
    2: catch_all,
    3 : Unknown,
    4 : Error,
    5 : Disposable,
    6 : Invalid,
    """

    settings: MillionVerifierSettings = field(default_factory=MillionVerifierSettings)

    name: str = "MillionVerifier"

    def _get(self, url: str, params: dict[str, Any], **kwargs) -> APIResponse:
        if not self.settings.api_key:
            raise ValueError("API Key is required for MillionVerifier service")
        r = requests.get(url, params=params, **kwargs)
        return APIResponse.from_response(r, "MillionVerifier")

    def _get_email_response(self, email: str, **kwargs) -> EmailResponse:
        params = {"api": self.settings.api_key, "email": email, "timeout": 10}
        response: APIResponse = self._get(self.settings.url, params=params)

        if response.status_code == 200:
            result = response.get_json()
            assert result and isinstance(result, dict)
            result.pop("credits", None)
            er = EmailResponse(**result)
            return er
        else:
            # return {"error": "Unable to verify email", "status_code": response.status_code}
            raise Exception(f"Unable to verify email {email}: {response.text}")

    def verify_email(self, email: str, **kwargs) -> EmailResponse:
        er = self._get_email_response(email, **kwargs)
        if er.error == "error" or not er.resultcode in self.settings.valid_includes:
            raise InvalidEmailError(er, f"Email {email} is not valid")
        return er
