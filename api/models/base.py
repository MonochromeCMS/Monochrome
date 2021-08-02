import uuid
from typing import Any

from sqlalchemy import func, Column, Integer, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import as_declarative, declared_attr

from ..exceptions import UnprocessableEntityHTTPException, NotFoundHTTPException


@as_declarative()
class Base:
    id: Any
    __name__: str
    version = Column(Integer, default=0)

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

    async def save(self, db_session: AsyncSession):
        """
        :param db_session:
        :return:
        """
        try:
            self.version = self.version + 1 if self.version else 1
            db_session.add(self)
            return await db_session.commit()
        except SQLAlchemyError as ex:
            raise UnprocessableEntityHTTPException(repr(ex))

    async def delete(self, db_session: AsyncSession):
        """
        :param db_session:
        :return:
        """
        try:
            await db_session.delete(self)
            await db_session.commit()
            return True
        except SQLAlchemyError as ex:
            raise UnprocessableEntityHTTPException(repr(ex))

    async def update(self, db_session: AsyncSession, **kwargs):
        """
        :param db_session:
        :param kwargs:
        :return:
        """
        for k, v in kwargs.items():
            setattr(self, k, v)
        await self.save(db_session)

    @classmethod
    async def find(cls, db_session: AsyncSession, _id: uuid.UUID):
        stmt = select(cls).where(cls.id == _id)
        result = await db_session.execute(stmt)
        instance = result.scalars().first()
        if instance is None:
            raise NotFoundHTTPException()
        else:
            return instance

    @classmethod
    async def find_rel(cls, db_session: AsyncSession, _id: uuid.UUID, relationship):
        stmt = select(cls).where(cls.id == _id).options(joinedload(relationship))
        result = await db_session.execute(stmt)
        instance = result.scalars().first()
        if instance is None:
            raise NotFoundHTTPException()
        else:
            return instance

    @staticmethod
    async def pagination(db_session, stmt, limit, offset):
        count_stmt = stmt.with_only_columns(func.count())
        count_result = await db_session.execute(count_stmt)
        page_stmt = stmt.offset(offset).limit(limit)
        page_result = await db_session.execute(page_stmt)
        return count_result.scalars().first(), page_result.scalars().all()
