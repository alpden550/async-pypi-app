from starlette.requests import Request

from pypi.data.user import User
from pypi.models.shared.view_model import BaseViewModel


class AccountViewModel(BaseViewModel):
    def __init__(self, request: Request):
        super().__init__(request)
        self.user = User("Denis", "alpden@me.com", "password")
