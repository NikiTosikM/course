from typing import Generic, TypeVar

from fastapi import HTTPException, status
from sqlalchemy import Result, delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from repositories.mappers.base_mapper import DBModel, Schema, BaseDataMapper

ValidateDatas = TypeVar("ValidateDatas", DBModel, None, list[DBModel])


class BaseRepository(Generic[DBModel]):
    model: type[DBModel]
    mapper: type[BaseDataMapper]
    
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.session = session


    async def get_filtered(self, *expressions, **filters) -> list[DBModel]:
        query = (
            select(self.model)
            .filter(*expressions)
            .filter_by(**filters)
        )
        result: Result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(model) for model in result.scalars().all()]

    async def get_all(self) -> list[DBModel]:
        return await self.get_filtered()

    async def get_one_or_none(self, **filter_by) ->  DBModel | None:
        query = select(self.model).filter_by(**filter_by)
        result: Result = await self.session.execute(query)

        return result.scalar_one_or_none()

    async def add(self, data: Schema) -> Schema:
        stmt = insert(self.model).values(**self.mapper.map_to_dict(data)).returning(self.model)
        result: Result = await self.session.execute(stmt)
        
        return result.scalar_one()
    
    async def add_bulk(self, data: list[Schema]) -> Schema:
        stmt = insert(self.model).values([self.mapper.map_to_dict(item) for item in data])
        await self.session.execute(stmt)

    async def update(
        self, data: Schema, exclude_unset: bool = False, **filter_by
    ) -> None:
        stmt = (
            update(self.model)
            .values(**self.mapper.map_to_dict(data=data, exclude_unset=exclude_unset))
            .filter_by(**filter_by)
            .returning(self.model)
        )
        result = await self.session.execute(stmt)
        model = result.scalars().all()
        self.validate_input_data(obj_model=model)

    async def delete(self, **filters) -> None:
        stmt = (
            delete(self.model)
            .filter_by(**filters)
            .returning(self.model)
        )
        result = await self.session.execute(stmt)
        model = result.scalars().all()
        self.validate_input_data(obj_model=model)

    def validate_input_data(self, obj_model: ValidateDatas):
        if not obj_model or len(obj_model) > 1:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail={
                    "message": "The method should return only one object of this model"
                },
            )

    async def specific_object(self, hotel_id: int):
        query = select(self.model).where(self.model.id==hotel_id)
        result = await self.session.execute(query)
        
        return result.scalar_one_or_none()
