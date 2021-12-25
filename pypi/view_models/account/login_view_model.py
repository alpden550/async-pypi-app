from typing import Optional

from starlette.requests import Request

from pypi.view_models.shared.view_model import BaseViewModel


class LoginViewModel(BaseViewModel):
    def __init__(self, request: Request):
        super().__init__(request)

        self.email: Optional[str] = None
        self.password: Optional[str] = None

    async def load(self):
        form = await self.request.form()
        self.email = form.get("email").lower().strip()
        self.password = form.get("password").strip()

        if not self.email:
            self.error = "You must specify the email."
        elif not self.password:
            self.error = "you must specify the password."
