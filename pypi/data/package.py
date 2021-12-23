import datetime

import sqlalchemy as sa
import sqlalchemy.orm as orm

from pypi.data.base_model import BaseSQLAlchemy
from pypi.data.release import Release


class Package(BaseSQLAlchemy):
    __tablename__ = "packages"

    id: str = sa.Column(sa.String, primary_key=True, unique=True)
    created_at: datetime.datetime = sa.Column(sa.DateTime, default=datetime.datetime.now(), primary_key=True)
    updated_at: datetime.datetime = sa.Column(sa.DateTime, default=datetime.datetime.now(), primary_key=True)
    summary: str = sa.Column(sa.String, nullable=False)
    description: str = sa.Column(sa.String, nullable=False)

    home_page: str = sa.Column(sa.String)
    docs_url: str = sa.Column(sa.String)
    package_url: str = sa.Column(sa.String)

    author_name: str = sa.Column(sa.String)
    author_email: str = sa.Column(sa.String, index=True)

    license: str = sa.Column(sa.String, index=True)

    releases: list[Release] = orm.relationship(
        "Release",
        order_by=[
            Release.major_ver.desc(),
            Release.minor_ver.desc(),
            Release.build_ver.desc(),
        ],
        back_populates="package",
    )

    def __repr__(self):
        return f"<Package {self.id}>"
