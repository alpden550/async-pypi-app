from typing import Optional

from starlette.requests import Request

from pypi.data.models.package import Package
from pypi.data.models.release import Release
from pypi.services import package_service
from pypi.view_models.shared.view_model import BaseViewModel


class DetailPackageViewModel(BaseViewModel):
    def __init__(self, package_name: str, request: Request):
        super().__init__(request)

        self.package_name = package_name
        self.package: Optional[Package] = None
        self.latest_release: Optional[Release] = None
        self.latest_version = "0.0.0"
        self.is_latest = True
        self.maintainers = []

    async def load(self):
        self.package = await package_service.get_package(self.package_name)
        self.latest_release = await package_service.get_latest_package_release(self.package_name)
        if not self.package or not self.latest_release:
            return

        release = self.latest_release
        self.latest_version = f"{release.major_ver}.{release.minor_ver}.{release.build_ver}"
        self.maintainers = self.package.maintainers
