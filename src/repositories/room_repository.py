from repositories.base_repository import BaseRepository
from sqlalchemy import insert, Result, select

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
        
    async def get_rooms_by_hotel(self, hotel_id) -> list[ResponceRoomHotelSchema]:
        query = select(self.model).where(self.model.hotel_id==hotel_id)
        result: Result = await self.session.execute(query)
        models = result.scalars().all()
        
        return [self.schema.model_validate(model) for model in models]
    