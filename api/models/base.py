from typing import Any

from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import as_declarative, declared_attr

from ..exceptions import UnprocessableEntityHTTPException


@as_declarative()
class Base:
    id: Any
    __name__: str

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

    @staticmethod
    async def pagination(db_session, stmt, limit, offset):
        count_stmt = stmt.with_only_columns(func.count())
        count_result = await db_session.execute(count_stmt)
        page_stmt = stmt.offset(offset).limit(limit)
        page_result = await db_session.execute(page_stmt)
        return count_result.scalars().first(), page_result.scalars().all()
