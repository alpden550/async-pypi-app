from starlette.requests import Request

from pypi.view_models.shared.view_model import BaseViewModel
from pypi.services import package_service


class DetailPackageViewModel(BaseViewModel):
    def __init__(self, package_name: str, request: Request):
        super().__init__(request)

        self.package_name = package_name
        self.package = package_service.get_package(package_name)
        self.latest_release = package_service.get_latest_package_release(package_name)
        self.latest_version = "0.0.0"
        self.is_latest = True
        self.maintainers = []

        if not self.package or not self.latest_release:
            return

        self.latest_version = self.latest_release.version
        self.maintainers = self.package.maintainers
