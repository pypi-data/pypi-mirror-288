from dataclasses import dataclass, field
from logging import getLogger
from typing import Any

import requests
from pydantic_settings import BaseSettings, SettingsConfigDict

from qrev_email_verification import APIResponse
from qrev_email_verification.email_verifying_service import EmailVerifyingService
from qrev_email_verification.services.zerobounce.models import (
    EmailResponse,
    InvalidEmailError,
    ResultStatusEnum,
)

log = getLogger(__name__)


class ZeroBounceSettings(BaseSettings):
    api_key: str = ""
    model_config = SettingsConfigDict(env_prefix="ZEROBOUNCE_")
    valid_statuses: set[ResultStatusEnum] = field(
        default_factory=lambda: set([ResultStatusEnum.VALID, ResultStatusEnum.CATCH_ALL])
    )
    api_url: str = "https://api.zerobounce.net/v2/validate"


@dataclass
class ZeroBounceService(EmailVerifyingService):
    """ZeroBounce Email Verification Service"""

    settings: ZeroBounceSettings = field(default_factory=ZeroBounceSettings)
    name: str = "ZeroBounce"

    def _get(self, url: str, params: dict[str, Any], **kwargs) -> APIResponse:
        if not self.settings.api_key:
            raise ValueError("API Key is required for ZeroBounce service")
        r = requests.get(url, params=params, **kwargs)
        return APIResponse.from_response(r, "ZeroBounce")

    def _get_email_response(self, email: str, **kwargs) -> EmailResponse:

        if not self.settings.api_key:
            raise ValueError("API Key is required for ZeroBounce service")
        params = {"api_key": self.settings.api_key, "email": email, "ip_address": ""}

        response: APIResponse = self._get(self.settings.api_url, params=params)
        if not response.status_code == 200:
            raise Exception(f"Unable to verify email {email}: {response.text}")

        result = response.get_json()
        assert result and isinstance(result, dict)
        result.pop("credits", None)
        er = EmailResponse(**result)
        return er

    def verify_email(self, email: str, **kwargs) -> EmailResponse:
        r = self._get_email_response(email, **kwargs)
        if r.status not in self.settings.valid_statuses:
            raise InvalidEmailError(r, f"Email {email} is not valid")
        return r
