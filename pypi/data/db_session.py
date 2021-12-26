from typing import Optional, Callable

import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession
from sqlalchemy.orm import Session

from pypi.config import get_settings
from pypi.data.models.base_model import BaseSQLAlchemy

__factory: Optional[Callable[[], Session]] = None
__async_engine: Optional[AsyncEngine] = None
engine: Engine = sa.create_engine(get_settings().database_url, pool_pre_ping=True, echo=False)


def global_init(db_file: str):
    global __factory, __async_engine

    if __factory:
        return

    if not db_file or not db_file.strip():
        raise Exception("You must specify the database.")

    __factory = orm.sessionmaker(bind=engine)
    __async_engine = create_async_engine(get_settings().async_database_url, echo=False)

    import pypi.data.models.__all_models  # noqa

    BaseSQLAlchemy.metadata.create_all(engine)


def create_session() -> Session:
    global __factory

    if not __factory:
        raise Exception("You must call global_init() before using this method.")

    session: Session = __factory()
    session.expire_on_commit = False

    return session


def create_async_session() -> AsyncSession:
    global __async_engine

    if not __async_engine:
        raise Exception("You must call global_init() before using this method.")

    session: AsyncSession = AsyncSession(__async_engine)
    session.sync_session.expire_on_commit = False

    return session
