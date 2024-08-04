from typing import Generic, Optional, Protocol, TypeVar

from pydantic import BaseModel

R = TypeVar("R")
E = TypeVar("E", bound=BaseModel)


class Response(Protocol, Generic[R, E]):
    result: Optional[R]
    errors: Optional[E]


class ResponseError(Exception):
    def __init__(self, message: str, error_codes: list[str]):
        self.message = message
        self.error_codes = error_codes


def return_or_raise(response: Response[R, E]) -> R:
    """This method takes a response object from the Fanpoints API and returns
    the result if it exists, otherwise it raises the returned errors."""
    if response.result is not None:
        return response.result

    if response.errors is None:
        raise Exception("Unknown error occurred.")

    error_codes = []
    for code in response.errors.model_fields.keys():
        if getattr(response.errors, code) is not None:
            error_codes.append(code)

    if not error_codes:
        raise Exception("Unknown error occurred.")

    raise ResponseError(f"The following errors occurred: {error_codes}.", error_codes)
