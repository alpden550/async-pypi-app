from fastapi import APIRouter, Depends
from fastapi_chameleon import template
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from pypi.data.db_session import get_session
from pypi.view_models.home import IndexViewModel

router = APIRouter()


@router.get("/", include_in_schema=False)
@template("home/index.pt")
async def index(request: Request, session: AsyncSession = Depends(get_session)):
    model = IndexViewModel(request)
    await model.load(session=session)
    return model.to_dict()
