from dataclasses import dataclass, field
from functools import wraps
from typing import Any, Type

from pydantic_settings import BaseSettings, SettingsConfigDict
from qrev_cache import Var, mongo_cache

from .api import MillionVerifierService, MillionVerifierSettings
from .models import EmailResponse


class MongoSettings(MillionVerifierSettings):
    cache_only: bool = False
    flat_data: bool = True

    model_config = SettingsConfigDict(env_prefix="MILLIONVERIFIER_")


@dataclass
class MillionVerifierMongoService(MillionVerifierService):
    data_type: Type[EmailResponse] = EmailResponse
    query: dict[str, Any] = field(
        default_factory=lambda: {
            "email": Var("email"),
            "service": "MillionVerifier",
        }
    )
    settings: MongoSettings = field(default_factory=MongoSettings)  # type: ignore

    def _get_email_response(self, email: str, **kwargs) -> EmailResponse:
        @wraps(self._get_email_response)
        @mongo_cache(
            env_prefix=self.settings.model_config.get("env_prefix"),
            query=self.query,
            flat_data=self.settings.flat_data,
            data_type=self.data_type,
            cache_only=self.settings.cache_only,
        )
        def wrapped(email: str, **kwargs) -> EmailResponse:
            return MillionVerifierService._get_email_response(self, email, **kwargs)

        return wrapped(email, **kwargs)
