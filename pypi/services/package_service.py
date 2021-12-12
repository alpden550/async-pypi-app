from datetime import datetime
from typing import Optional

from pypi.data.package import Package
from pypi.data.release import Release


def count_packages() -> int:
    return 0


def count_releases() -> int:
    return 0


def fetch_latest_releases(limit: int = 5) -> list:
    return [
        {"id": "fastapi", "summary": "Async web framework"},
        {"id": "uvicorn", "summary": "ASI server"},
    ][:limit]


def get_package(package_name: str) -> Optional[Package]:
    return Package(
        package_name=package_name,
        summary="This is the summary",
        description="Full detail here",
        home_page="www.google.com",
        package_license="MIT",
        author_name="Sebastian",
    )


def get_latest_package_release(package_name: str) -> Optional[Release]:
    return Release("1.2.3", datetime.now())
