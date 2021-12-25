from fastapi import APIRouter
from fastapi_chameleon import template
from starlette.requests import Request

from pypi.view_models.home import IndexViewModel

router = APIRouter()


@router.get("/")
@template("home/index.pt")
def index(request: Request):
    model = IndexViewModel(request)
    return model.to_dict()
