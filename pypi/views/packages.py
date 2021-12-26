from fastapi import APIRouter
from fastapi_chameleon import template
from starlette.requests import Request

from pypi.view_models.packages import DetailPackageViewModel

router = APIRouter()


@router.get("/{package_name}")
@template("packages/details.pt")
async def detail(package_name: str, request: Request):
    detail_model = DetailPackageViewModel(package_name, request)
    await detail_model.load()
    return detail_model.to_dict()
