from typing import Any

from pydantic import BaseModel


class Response(BaseModel):
    success: bool = True
    message: Any = None
    data: Any
    error_code: int = 0
