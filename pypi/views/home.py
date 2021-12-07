from fastapi import APIRouter
from fastapi_chameleon import template

router = APIRouter()


@router.get("/")
@template("home/index.pt")
def index():
    """Main index pypi page."""
    return {"user_name": "YEP"}


@router.get("/about")
def about():
    """About pypi page."""
    return {}
