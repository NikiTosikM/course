from repositories.base_repository import BaseRepository
from sqlalchemy import insert, Result

from models.rooms import Rooms
from schemas.rooms import RoomHotelSchema, ResponceRoomHotelSchema


class RoomRepository(BaseRepository[Rooms]):
    def __init__(self, session, model, schema = None):
        super().__init__(session, model, schema)
        
    async def add(self, data: RoomHotelSchema, **values) -> ResponceRoomHotelSchema:
        stmt = insert(self.model).values(**data.model_dump(), **values).returning(self.model)
        result: Result = await self.session.execute(stmt)
        model = result.scalar_one()
        return self.schema.model_validate(model)
        
    