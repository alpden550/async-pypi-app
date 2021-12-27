from fastapi import APIRouter, Depends
from fastapi_chameleon import template
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from pypi.data.db_session import get_session
from pypi.view_models.packages import DetailPackageViewModel

router = APIRouter()


@router.get("/{package_name}")
@template("packages/details.pt")
async def detail(package_name: str, request: Request, session: AsyncSession = Depends(get_session)):
    detail_model = DetailPackageViewModel(package_name, request)
    await detail_model.load(session=session)
    return detail_model.to_dict()
