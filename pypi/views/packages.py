from fastapi import APIRouter
from fastapi_chameleon import template
from starlette.requests import Request

from pypi.models.packages import DetailPackageViewModel

router = APIRouter()


@router.get("/{package_name}")
@template("packages/details.pt")
def detail(package_name: str, request: Request):
    detail_model = DetailPackageViewModel(package_name, request)
    return detail_model.to_dict()
