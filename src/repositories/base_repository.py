from typing import TypeVar, Generic

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, Result, insert, update, delete
from pydantic import BaseModel

from core.db.base_model import Base


Model = TypeVar("Model", bound=Base)
Schema = TypeVar("Schema", bound=BaseModel)

ValidateDatas = TypeVar("ValidateDatas", Model, None, list[Model])


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
    
    async def update(self, data: Schema, **filter_by) -> None:
        stmt = (
            update(self.model)
            .where(self.model.id==filter_by["id"])
            .values(**data.model_dump())
            .returning(self.model)
        )
        result = await self.session.execute(stmt)
        model: Model = result.scalars().all()
        self.validate_input_data(obj_model=model)
        
    async def delete(self, **filter_by) -> None:
        stmt = (
            delete(self.model)
            .where(self.model.id==filter_by["id"])
            .returning(self.model)
        )
        result = await self.session.execute(stmt)
        model: Model = result.scalars().all()
        self.validate_input_data(obj_model=model)
        
    def validate_input_data(self, obj_model: ValidateDatas):
        print(obj_model, flush=True)
        if not obj_model or len(obj_model) > 1:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail={
                    "message": "The method should return only one object of this model"
                }
            )