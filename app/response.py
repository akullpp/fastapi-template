from typing import Any

from fastapi.responses import JSONResponse


class JsonResponse(JSONResponse):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.headers["Access-Control-Allow-Origin"] = "*"
        self.headers["Access-Control-Expose-Headers"] = "*"
        self.headers["Access-Control-Allow-Credentials"] = "true"
