from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Any, Dict


class HttpResponse(JSONResponse):
    def __init__(self, status: str, status_code: int, message: str, data: Any, custom_header: str = "CustomHeaderValue",
                 **kwargs):
        # Format the response content as a dictionary containing status, status_code, message, and data
        content = {
            "status": status,
            "status_code": status_code,
            "message": message,
            "data": data
        }

        content = jsonable_encoder(content)

        headers = kwargs.get("headers", {})
        headers["X-Custom-Header"] = custom_header

        # Call the parent class constructor
        super().__init__(content=content, headers=headers, **kwargs)


class HttpErrorResponse(JSONResponse):
    def __init__(self, status: str, status_code: int, message: str, data: Any, custom_header: str = "CustomHeaderValue",
                 **kwargs):
        # Format the response content as a dictionary containing status, status_code, message, and data
        content = {
            "status": status,
            "status_code": status_code,
            "message": message,
            "data": data
        }

        # Optionally modify the content (ensure it's JSON serializable)
        content = jsonable_encoder(content)

        # Add custom headers if needed
        headers = kwargs.get("headers", {})
        headers["X-Custom-Header"] = custom_header

        # Call the parent class constructor
        super().__init__(content=content, headers=headers, **kwargs)

