from typing import Any, Optional

from starlette.requests import Request

from pypi.infrastructure import cookie_auth


class BaseViewModel:
    def __init__(self, request: Request):
        self.request: Request = request
        self.error: Optional[str] = None
        self.user_id: Optional[id] = None
        self.is_logged_in = cookie_auth.get_user_id_from_cookie(self.request)

    def to_dict(self) -> dict[str, Any]:
        return self.__dict__
