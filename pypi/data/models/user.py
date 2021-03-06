import datetime

import sqlalchemy as sa

from pypi.data.models.base_model import BaseSQLAlchemy


class User(BaseSQLAlchemy):
    __tablename__ = "users"

    id: int = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name: str = sa.Column(sa.String, index=True)
    username: str = sa.Column(sa.String, nullable=True)
    email: str = sa.Column(sa.String, index=True, unique=True, nullable=True)
    hash_password: str = sa.Column(sa.String)
    created_at: datetime.datetime = sa.Column(sa.DateTime, default=datetime.datetime.now, index=True)
    last_login_at: datetime.datetime = sa.Column(sa.DateTime, default=datetime.datetime.now, index=True)
    profile_image_url: str = sa.Column(sa.String)

    def __repr__(self):
        return f"User {self.name} – {self.email}"
