from typing import Optional

import sqlalchemy as sa
from sqlalchemy import func
from sqlalchemy.engine import ChunkedIteratorResult
from sqlalchemy.ext.asyncio import AsyncSession

from pypi.data import db_session
from pypi.data.models.package import Package
from pypi.data.models.release import Release


async def count_packages() -> int:
    session: AsyncSession
    async with db_session.create_async_session() as session:
        result: ChunkedIteratorResult = await session.execute(sa.select(func.count(Package.id)))
        return result.scalar()


async def count_releases() -> int:
    session: AsyncSession
    async with db_session.create_async_session() as session:
        result: ChunkedIteratorResult = await session.execute(sa.select(func.count(Release.id)))
        return result.scalar()


async def fetch_latest_releases(limit: int = 5) -> list[Package]:
    session: AsyncSession
    async with db_session.create_async_session() as session:
        query = sa.select(Release).order_by(Release.created_at.desc()).limit(limit)  # noqa
        result: ChunkedIteratorResult = await session.execute(query)
        releases = result.scalars()

    return [release.package for release in releases]


async def get_package(package_name: str) -> Optional[Package]:
    session: AsyncSession
    async with db_session.create_async_session() as session:
        query = sa.select(Package).filter_by(id=package_name)
        result: ChunkedIteratorResult = await session.execute(query)
        return result.scalar_one_or_none()


async def get_latest_package_release(package_name: str) -> Optional[Release]:
    session: AsyncSession
    async with db_session.create_async_session() as session:
        query = sa.select(Release).filter_by(package_id=package_name).order_by(Release.created_at.desc())  # noqa
        result: ChunkedIteratorResult = await session.execute(query)
        return result.scalar()
