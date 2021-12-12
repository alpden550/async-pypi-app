from typing import Any, Optional

from starlette.requests import Request


class BaseViewModel:
    def __init__(self, request: Request):
        self.request: Request = request
        self.error: Optional[str] = None
        self.user_id: Optional[id] = None
        self.is_logged_in = False

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__
