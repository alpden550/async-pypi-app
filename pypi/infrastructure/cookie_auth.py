from typing import Optional

from starlette.requests import Request
from starlette.responses import Response

from pypi.infrastructure.helpers import __hash_text, try_int

auth_cookie_name = "pypi_account"


def set_auth(response: Response, user_id: int) -> None:
    hash_value = __hash_text(str(user_id))
    value = f"{user_id}:{hash_value}"
    response.set_cookie(auth_cookie_name, value, secure=False, httponly=True)


def get_user_id_from_cookie(request: Request) -> Optional[int]:
    if auth_cookie_name not in request.cookies:
        return None

    value = request.cookies[auth_cookie_name]
    value_parts = value.split(":")

    if len(value_parts) != 2:
        return None

    user_id, hash_value = value_parts
    hash_value_check = __hash_text(user_id)
    if hash_value != hash_value_check:
        return None

    return try_int(user_id)


def logout(response: Response) -> None:
    response.delete_cookie(auth_cookie_name)
