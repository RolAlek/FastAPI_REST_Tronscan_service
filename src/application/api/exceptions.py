from typing import Protocol

from pydantic import BaseModel


class APIErrorSchema(BaseModel):
    code: str
    message: str


class BaseHTTPErrorProtocol(Protocol):
    status_code: int
    error_schema: APIErrorSchema
    code: str


class BaseHTTPError(BaseHTTPErrorProtocol, Exception):
    pass


def get_responses(*errors: tuple[BaseHTTPError]) -> dict:
    result = {}
    for error in errors:
        if error.status_code not in result:
            result[error.status_code] = {
                "content": {
                    "application/json": {
                        "examples": {error.code: {"value": error.error_schema}}
                    }
                }
            }
        else:
            result[error.status_code]["content"]["application/json"]["examples"][
                error.code
            ] = {"value": error.error_schema}
    return result
