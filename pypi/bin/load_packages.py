import json
import pathlib
from typing import Generator, Optional, Any

from dateutil.parser import parse
from sqlalchemy.orm import Session

from pypi.config import get_settings
from pypi.data.db_session import create_session, global_init
from pypi.data.helpers import get_or_create
from pypi.data.models.package import Package
from pypi.data.models.release import Release
from pypi.data.models.user import User
from pypi.infrastructure.helpers import try_int


def fetch_packages_files() -> Generator[pathlib.Path, None, None]:
    return pathlib.Path("pypi/bin/pypi-top-100").rglob("*.json")


def add_user(session: Session, name: str, email: Optional[str]) -> User:
    user = get_or_create(session, User, name=name.strip())
    if email.strip():
        email_user = session.query(User).filter_by(email=email).first()
        if email_user:
            email_user.name = name
            session.add(email_user)
        else:
            user.email = email
        session.add(user)
        session.commit()

    return user


def add_package(session: Session, package_id: str, params: dict[str, Any]) -> Package:
    package = get_or_create(session, Package, id=package_id)
    package.summary = params.get("summary") or ""
    package.description = params.get("description") or ""
    package.home_page = params.get("home_page")
    package.docs_url = params.get("docs_url")
    package.package_url = params.get("package_url")
    package.license = params.get("license")
    package.user = params.get("user")
    package.maintainers = [params.get("maintainers")] if params.get("maintainers") else []

    session.add(package)
    session.commit()
    return package


def add_release(session: Session, package: Package, params: dict[str, Any]) -> None:
    major_ver, minor_ver, build_ver = make_version_num(params.get("version"))
    release = Release(
        package=package,
        major_ver=major_ver,
        minor_ver=minor_ver,
        build_ver=build_ver,
        comment=params.get("comment"),
        url=params.get("url"),
        size=params.get("size"),
        created_at=params.get("created_at"),
    )

    session.add(release)
    session.commit()


def make_version_num(version_text: str) -> tuple[int, int, int]:
    major, minor, build = 0, 0, 0
    if version_text:
        version_text = version_text.split("b")[0]
        parts = version_text.split(".")
        if len(parts) == 1:
            major = try_int(parts[0])
        elif len(parts) == 2:
            major = try_int(parts[0])
            minor = try_int(parts[1])
        elif len(parts) == 3:
            major = try_int(parts[0])
            minor = try_int(parts[1])
            build = try_int(parts[2])

        return major, minor, build


def fetch_licenses(classifiers: list[str]) -> str:
    licenses = [classifier.split(":")[-1].strip() for classifier in classifiers if "License" in classifier]
    return ", ".join(licenses)


def main():
    global_init(get_settings().database_url)
    session: Session = create_session()

    packages_files = fetch_packages_files()
    for package_file in packages_files:
        package_json = json.loads(package_file.read_text())
        package_info = package_json["info"]

        user = add_user(session=session, name=package_info.get("author"), email=package_info.get("author_email"))
        package = add_package(
            session=session,
            package_id=package_info["name"],
            params={
                "summary": package_info.get("summary") if package_info.get("summary") else "",
                "description": package_info.get("description") if package_info.get("description") else "",
                "home_page": package_info.get("home_page"),
                "docs_url": package_info.get("docs_url"),
                "package_url": package_info.get("package_url"),
                "license": fetch_licenses(package_info["classifiers"]),
                "user": user,
                "maintainers": package_info.get("maintainer"),
            },
        )

        for version, release_data in package_json["releases"].items():
            release = release_data[-1] if release_data else None
            if release is None:
                continue

            add_release(
                session=session,
                package=package,
                params={
                    "version": version,
                    "comment": release.get("comment_text"),
                    "url": release.get("url"),
                    "size": release.get("size", 0),
                    "created_at": parse(release.get("upload_time")),
                },
            )

        print(package)

    session.close()


if __name__ == "__main__":
    main()
