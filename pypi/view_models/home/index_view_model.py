from sqlalchemy.ext.asyncio import AsyncSession
from starlette.requests import Request

from pypi.services import package_service, user_service
from pypi.view_models.shared import BaseViewModel


class IndexViewModel(BaseViewModel):
    def __init__(self, request: Request):
        super().__init__(request)

        self.package_count: int = 0
        self.release_count: int = 0
        self.user_count: int = 0
        self.packages: list[dict[str, str]] = []

    async def load(self, session: AsyncSession):
        self.package_count: int = await package_service.count_packages(session=session)
        self.release_count: int = await package_service.count_releases(session=session)
        self.user_count: int = await user_service.user_count(session=session)
        self.packages: list[dict[str, str]] = await package_service.fetch_latest_releases(session=session, limit=5)
