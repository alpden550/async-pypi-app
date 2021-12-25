import datetime

import sqlalchemy as sa
import sqlalchemy.orm as orm

from pypi.data.base_model import BaseSQLAlchemy


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
    license: str = sa.Column(sa.String, index=True)

    user_id: int = sa.Column(sa.ForeignKey("users.id"))
    user = orm.relationship("User", backref="packages")

    maintainers = sa.Column(sa.ARRAY(sa.String))

    def __repr__(self):
        return f"<Package {self.id}>"
