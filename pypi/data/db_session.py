from typing import Optional, Callable

import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session

from pypi.data.base_model import BaseSQLAlchemy

__factory: Optional[Callable[[], Session]] = None


def global_init(db_file: str):
    global __factory

    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("You must specify the database.")

    engine = sa.create_engine(db_file, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    import pypi.data.__all_models  # noqa

    BaseSQLAlchemy.metadata.create_all(engine)


def create_session() -> Session:
    global __factory

    if not __factory:
        raise Exception("You must call global_init() before using this method.")

    session: Session = __factory()
    session.expire_on_commit = False

    return session
