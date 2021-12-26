from typing import Optional

import sqlalchemy as sa
from passlib.handlers.sha2_crypt import sha512_crypt as crypto
from sqlalchemy import func
from sqlalchemy.engine import ChunkedIteratorResult
from sqlalchemy.ext.asyncio import AsyncSession

from pypi.data import db_session
from pypi.data.models.user import User


async def user_count() -> int:
    session: AsyncSession
    async with db_session.create_async_session() as session:
        result: ChunkedIteratorResult = await session.execute(sa.select(func.count(User.id)))
        return result.scalar()


async def create_account(name: str, email: str, password: str) -> User:
    session: AsyncSession
    async with db_session.create_async_session() as session:
        user = User(name=name, email=email, hash_password=crypto.hash(password, rounds=172_434))
        session.add(user)
        await session.commit()
    return user


async def login_user(email: str, password: str) -> Optional[User]:
    session: AsyncSession
    async with db_session.create_async_session() as session:
        query = sa.select(User).filter_by(email=email)
        result: ChunkedIteratorResult = await session.execute(query)
        user = result.scalar_one_or_none()

        if not user or not crypto.verify(password, user.hash_password):
            return None
        return user


async def get_user_by_id(user_id: int) -> Optional[User]:
    session: AsyncSession
    async with db_session.create_async_session() as session:
        query = sa.select(User).filter_by(id=user_id)
        result: ChunkedIteratorResult = await session.execute(query)
        return result.scalar_one_or_none()


async def get_user_by_email(email: str) -> Optional[User]:
    session: AsyncSession
    async with db_session.create_async_session() as session:
        query = sa.select(User).filter_by(email=email)
        result: ChunkedIteratorResult = await session.execute(query)
        return result.scalar_one_or_none()
