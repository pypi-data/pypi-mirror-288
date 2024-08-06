import os
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any, Optional

from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from qrev_email_verification.email_verifying_service import EmailVerifyingService
from qrev_email_verification.models.models import InvalidEmailError
from qrev_email_verification.services.millionverifier.api import MillionVerifierSettings
from qrev_email_verification.services.millionverifier.mongo_api import (
    MillionVerifierMongoService,
)
from qrev_email_verification.services.millionverifier.mongo_api import (
    MongoSettings as MVMongoSettings,
)
from qrev_email_verification.services.zerobounce.api import ZeroBounceSettings
from qrev_email_verification.services.zerobounce.mongo_api import (
    MongoSettings as ZBMongoSettings,
)
from qrev_email_verification.services.zerobounce.mongo_api import ZeroBounceMongoService


class EmailVerificationSettings(BaseSettings):
    uri: str = ""
    db: str = "verification"
    collection: str = "email"
    millionverifier: str = ""
    zerobounce: str = ""
    services_env_prefix: dict[str, str] = Field(default_factory=dict)

    model_config = SettingsConfigDict(env_prefix="MONGO_EMAIL_VERIFICATION_")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._set_service_prefix("millionverifier")
        self._set_service_prefix("zerobounce")

    def _set_service_prefix(self, service_name):
        service_value = getattr(self, service_name, None)
        if service_value:
            prefix = service_value if service_value.endswith("_") else f"{service_value}_"
            self.services_env_prefix[service_name] = prefix


@dataclass
class EmailVerification:
    settings: EmailVerificationSettings = field(default_factory=EmailVerificationSettings)
    services: dict[str, EmailVerifyingService] = field(default_factory=dict)

    def __post_init__(self):
        for service_name, env_prefix in self.settings.services_env_prefix.items():
            service_name = service_name.lower()
            if service_name == "millionverifier":
                ms = MillionVerifierMongoService.create_settings(
                    MVMongoSettings, env_prefix=env_prefix
                )
                self.services[service_name] = MillionVerifierMongoService(settings=ms)
            elif service_name.lower() == "zerobounce":
                ms = ZeroBounceMongoService.create_settings(ZBMongoSettings, env_prefix=env_prefix)
                self.services[service_name] = ZeroBounceMongoService(settings=ms)

    def get_email_responses(
        self, email: str, service_name: Optional[str] = None, include_invalids: bool = False
    ) -> dict[str, BaseModel]:
        results = {}
        services = (
            self.services if not service_name else {service_name: self.services[service_name]}
        )
        for service_name, service in services.items():
            ## verify_email will throw an InvalidEmailError if the email is invalid
            ## or doesn't meet the validation criteria
            try:
                r = service.verify_email(email)
                results[service_name] = r
            except InvalidEmailError as e:
                if not include_invalids:
                    raise e
                results[service_name] = e.email_response
                # results.append(e.email_response)

        else:
            return results

    def check_email_verification(
        self,
        email: str,
        service_name: Optional[str] = None,
    ) -> bool:
        ## TODO : Add in logical expressions with logex
        services = (
            self.services if not service_name else {service_name: self.services[service_name]}
        )
        for service_name, service in services.items():
            ## verify_email will throw an InvalidEmailError if the email is invalid
            ## or doesn't meet the validation criteria
            service.verify_email(email)
        else:
            return True
