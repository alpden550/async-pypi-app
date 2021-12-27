import fastapi.responses
from fastapi import APIRouter, Depends
from fastapi_chameleon import template
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.requests import Request

from pypi.data.db_session import get_session
from pypi.infrastructure import cookie_auth
from pypi.services import user_service
from pypi.view_models.account import AccountViewModel, LoginViewModel, RegisterViewModel

router = APIRouter()


@router.get("/", include_in_schema=False)
@template("account/index.pt")
async def account(request: Request, session: AsyncSession = Depends(get_session)):
    account_model = AccountViewModel(request)
    await account_model.load(session=session)
    return account_model.to_dict()


@router.get("/register", include_in_schema=False)
@template("account/register.pt")
def get_register(request: Request):
    register_model = RegisterViewModel(request)
    return register_model.to_dict()


@router.post("/register", include_in_schema=False)
@template("account/register.pt")
async def post_register(request: Request, session: AsyncSession = Depends(get_session)):
    register_model = RegisterViewModel(request)
    await register_model.load(session=session)

    if register_model.error:
        return register_model.to_dict()

    user_account = await user_service.create_account(
        session=session,
        name=register_model.name,
        email=register_model.email,
        password=register_model.password,
    )
    response = fastapi.responses.RedirectResponse(url="/account", status_code=status.HTTP_302_FOUND)
    cookie_auth.set_auth(response, user_account.id)
    return response


@router.get("/login", include_in_schema=False)
@template("account/login.pt")
def get_login(request: Request):
    login_model = LoginViewModel(request)
    return login_model.to_dict()


@router.post("/login", include_in_schema=False)
@template("account/login.pt")
async def post_login(request: Request, session: AsyncSession = Depends(get_session)):
    login_model = LoginViewModel(request)
    await login_model.load()

    if login_model.error:
        return login_model.to_dict()

    user = await user_service.login_user(session=session, email=login_model.email, password=login_model.password)
    if not user:
        login_model.error = "The account does not exist or the password is wrong."
        return login_model.to_dict()

    response = fastapi.responses.RedirectResponse(url="/account", status_code=status.HTTP_302_FOUND)
    cookie_auth.set_auth(response, user.id)
    return response


@router.get("/logout", include_in_schema=False)
def logout():
    response = fastapi.responses.RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    cookie_auth.logout(response)
    return response
