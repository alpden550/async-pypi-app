from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from pypi.services import user_service
from pypi.view_models.shared.view_model import BaseViewModel


class RegisterViewModel(BaseViewModel):
    def __init__(self, request: Request):
        super().__init__(request)

        self.name: Optional[str] = None
        self.email: Optional[str] = None
        self.password: Optional[str] = None

    async def load(self, session: AsyncSession):
        form = await self.request.form()
        self.name = form.get("name")
        self.email = form.get("email")
        self.password = form.get("password")

        if not self.name or not self.name.strip():
            self.error = "Your name is required."
        elif not self.email or not self.email.strip():
            self.error = "Your email is required."
        elif not self.password or len(self.password) < 5:
            self.error = "Your password is required and must be at 5 characters."
        elif await user_service.get_user_by_email(session=session, email=self.email):
            self.error = "This email already exists. Could log in instead?"
