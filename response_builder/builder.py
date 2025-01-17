from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Any, Dict


class HttpResponse(JSONResponse):
    def __init__(self, status: str, status_code: int, message: str, data: Any, custom_header: str = "CustomHeaderValue",
                 **kwargs):
        content = {
            "status": status,
            "status_code": status_code,
            "message": message,
            "data": data
        }

        content = jsonable_encoder(content)

        headers = kwargs.get("headers", {})
        headers["X-Custom-Header"] = custom_header

        super().__init__(content=content, headers=headers, **kwargs)


class HttpErrorResponse(JSONResponse):
    def __init__(self, status: str, status_code: int, message: str, data: Any, custom_header: str = "CustomHeaderValue",
                 **kwargs):
        content = {
            "status": status,
            "status_code": status_code,
            "message": message,
            "data": data
        }

        content = jsonable_encoder(content)

        headers = kwargs.get("headers", {})
        headers["X-Custom-Header"] = custom_header

        super().__init__(content=content, headers=headers, **kwargs)

