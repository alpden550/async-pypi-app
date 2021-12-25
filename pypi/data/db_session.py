from typing import Optional, Callable

import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session

from pypi.config import get_settings
from pypi.data.models.base_model import BaseSQLAlchemy

__factory: Optional[Callable[[], Session]] = None
engine = sa.create_engine(get_settings().database_url, pool_pre_ping=True, echo=False)


def global_init(db_file: str):
    global __factory

    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("You must specify the database.")

    __factory = orm.sessionmaker(bind=engine)

    import pypi.data.models.__all_models  # noqa

    BaseSQLAlchemy.metadata.create_all(engine)


def create_session() -> Session:
    global __factory

    if not __factory:
        raise Exception("You must call global_init() before using this method.")

    session: Session = __factory()
    session.expire_on_commit = False

    return session
