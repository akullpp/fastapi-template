from fastapi import Request

from app import utilities
from app.response import JsonResponse


class CustomError(Exception):
    def __init__(
        self,
        code: int,
        key: str,
        message: str | None = None,
        details: dict | None = None,
    ):
        self.code = code
        self.key = key
        self.message = message
        self.details = details

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        return f"{class_name}(code={self.code!r}, key={self.key!r})"

    def json(self) -> JsonResponse:
        code = self.code
        content = {
            "key": self.key,
        }
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Expose-Headers": "*",
            "Access-Control-Allow-Credentials": "true",
        }
        utilities.add_all(
            content,
            [
                ("message", self.message),
                ("details", self.details),
            ],
        )
        return JsonResponse(content, code, headers)


async def custom_exception_handler(_: Request, exception: Exception) -> JsonResponse:
    if isinstance(exception, CustomError):
        return exception.json()

    content = {
        "key": "UNSPECIFIED",
    }
    utilities.add(content, ("message", str(exception)))

    return JsonResponse(
        status_code=500,
        content=content,
    )
