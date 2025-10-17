from typing import Generic, TypeVar

from fastapi import HTTPException, status
from sqlalchemy import Result, delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.mappers.base_mapper import DBModel, Schema

ValidateDatas = TypeVar("ValidateDatas", DBModel, None, list[DBModel])


class BaseRepository(Generic[DBModel]):
    model: DBModel
    schema: Schema
    
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session


    async def get_filtered(self, *expressions, **filters) -> list[Schema]:
        query = (
            select(self.model)
            .filter(*expressions)
            .filter_by(**filters)
        )
        result: Result = await self.session.execute(query)
        return [self.schema.model_validate(model) for model in result.scalars().all()]

    async def get_all(self) -> list[DBModel]:
        return await self.get_filtered()

    async def get_one_or_none(self, **filter_by) ->  DBModel | None:
        query = select(self.model).filter_by(**filter_by)
        result: Result = await self.session.execute(query)

        return result.scalar_one_or_none()

    async def add(self, data: Schema) -> Schema:
        stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        result: Result = await self.session.execute(stmt)
        model = result.scalar_one()
        
        return self.schema.model_validate(model)
    
    async def add_bulk(self, data: list[Schema]) -> Schema:
        stmt = insert(self.model).values([item.model_dump(exclude_unset=True) for item in data])
        await self.session.execute(stmt)

    async def update(
        self, data: Schema, exclude_unset: bool = False, **filter_by
    ) -> None:
        stmt = (
            update(self.model)
            .values(**data.model_dump(exclude_unset=exclude_unset))
            .filter_by(**filter_by)
            .returning(self.model)
        )
        await self.session.execute(stmt)


    async def delete(self, **filters) -> None:
        stmt = (
            delete(self.model)
            .filter_by(**filters)
            .returning(self.model)
        )
        await self.session.execute(stmt)

    async def specific_object(self, hotel_id: int):
        query = select(self.model).where(self.model.id==hotel_id)
        result = await self.session.execute(query)
        model = result.scalar_one_or_none()
        
        return self.schema.model_validate(model)
