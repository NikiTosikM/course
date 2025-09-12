from typing import TypeVar, Generic

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result, insert
from pydantic import BaseModel

from core.db.base_model import Base


Model = TypeVar("Model", bound=Base)
Schema = TypeVar("Schema", bound=BaseModel)


class BaseRepository(Generic[Model]):
    def __init__(
        self,
        session: AsyncSession,
        model: type[Model],
        schema: type[Schema] | None = None,
    ):
        self.session = session
        self.model = model
        self.schema = schema

    async def get_all(self) -> list[Model]:
        query = select(self.model)
        result: Result = await self.session.execute(query)

        return result.scalars().all()

    async def get_one_or_none(self, **filter_by) -> Model:
        query = select(self.model).filter_by(**filter_by)
        result: Result = await self.session.execute(query)

        return result.scalar_one_or_none()

    async def add(self, data: Schema) -> Model:
        stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        result: Result = await self.session.execute(stmt)
        
        return result.scalar_one()
