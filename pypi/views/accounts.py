from fastapi import APIRouter
from starlette.requests import Request

from pypi.models.account import AccountViewModel, LoginViewModel, RegisterViewModel

router = APIRouter()


@router.get("/account")
def account(request: Request):
    """."""
    account_model = AccountViewModel(request)
    return account_model.to_dict()


@router.get("/account/register")
def register(request: Request):
    """."""
    register_model = RegisterViewModel(request)
    return register_model.to_dict()


@router.get("/account/login")
def login(request: Request):
    """."""
    login_model = LoginViewModel(request)
    return login_model.to_dict()


@router.get("/account/logout")
def logout(request: Request):
    """."""
    return {}
