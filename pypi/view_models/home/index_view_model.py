from starlette.requests import Request

from pypi.view_models.shared import BaseViewModel
from pypi.services import package_service, user_service


class IndexViewModel(BaseViewModel):
    def __init__(self, request: Request):
        super().__init__(request)

        self.package_count: int = package_service.count_packages()
        self.release_count: int = package_service.count_releases()
        self.user_count: int = user_service.user_count()
        self.packages: list[dict[str, str]] = package_service.fetch_latest_releases(limit=5)
