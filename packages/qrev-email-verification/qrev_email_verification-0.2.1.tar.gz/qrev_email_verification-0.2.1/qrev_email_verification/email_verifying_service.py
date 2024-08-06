from dataclasses import dataclass
from typing import Any, TypeVar, cast

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

T = TypeVar("T", bound=BaseSettings)


@dataclass
class EmailVerifyingService:
    def verify_email(self, email: str, **kwargs) -> BaseModel:
        raise NotImplementedError

    def verify_email_json(self, email: str, **kwargs) -> dict[str, Any]:
        raise NotImplementedError

    @classmethod
    def _create_settings_class(cls, base_class: type[T], env_prefix: str) -> type[T]:
        class DynamicSettings(base_class):  # type: ignore
            model_config = SettingsConfigDict(env_prefix=env_prefix)

        return DynamicSettings  # type: ignore

    @classmethod
    def create_settings(cls, settings_type: type[T], env_prefix: str, *args, **kwargs) -> T:
        DynamicSettings = cls._create_settings_class(settings_type, env_prefix)
        return DynamicSettings(*args, **kwargs)
