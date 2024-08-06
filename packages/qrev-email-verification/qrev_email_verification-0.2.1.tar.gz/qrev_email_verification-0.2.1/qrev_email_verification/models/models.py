from typing import Any, Optional, Union

import requests
from pydantic import BaseModel, Field


class InvalidEmailError(Exception):
    def __init__(self, email_response: Any, message: str):
        self.email_response = email_response
        self.save_var = email_response
        super().__init__(message)


class APIResponse(BaseModel):
    status_code: int
    text: str = ""
    json_content: Union[dict, list, None] = None
    headers: dict = Field(default_factory=dict)

    @classmethod
    def from_response(cls, response: requests.Response, service: Optional[str] = None):
        try:
            json_content = response.json()
            if service:
                json_content["service"] = service
        except ValueError:
            json_content = None

        return cls(
            status_code=response.status_code,
            text=response.text,
            json_content=json_content,
            headers=dict(response.headers),
        )

    def get_json(self) -> Union[dict, list, None]:
        return self.json_content

