from fastapi import APIRouter
from fastapi_chameleon import template
from starlette.requests import Request

from pypi.models.home import IndexViewModel

router = APIRouter()


@router.get("/")
@template("home/index.pt")
def index(request: Request):
    """Main index pypi page."""
    model = IndexViewModel(request)
    return model.to_dict()
