from repositories.base_repository import BaseRepository, Model
from sqlalchemy import insert, Result

from models import Rooms
from schemas.rooms import RoomHotelSchema, ResponceRoomHotelSchema
from repositories.db_expressions import getting_available_rooms


class RoomRepository(BaseRepository[Rooms]):
    model = Rooms
    schema = ResponceRoomHotelSchema

    def __init__(self, session):
        super().__init__(session)

    async def add(self, data: RoomHotelSchema, **values) -> ResponceRoomHotelSchema:
        stmt = (
            insert(self.model)
            .values(**data.model_dump(), **values)
            .returning(self.model)
        )
        result: Result = await self.session.execute(stmt)

        return result.scalar_one()

    async def get_all(self, date_from: str, date_to: str, hotel_id: int):
        ids_and_count_free_rooms_sql_exper = getting_available_rooms(
            date_from=date_from,
            date_to=date_to,
            hotel_id=hotel_id
        )
        result: Result = await self.session.execute(ids_and_count_free_rooms_sql_exper )
        
        id_numbers_available_seats: dict[int, int] = {room[0]: room[1] for room in result.all()}  # ключ - id_room, value - count available_seats
        free_room_models: list[Model] = await self.get_filtered(
            Rooms.id.in_(id_numbers_available_seats), hotel_id=hotel_id
        )
        
        for room in free_room_models:
            room.quantity =  id_numbers_available_seats[room.id]
            
        return free_room_models

        # print("вот запрос", query.compile(bind=async_engine, compile_kwargs={"literal_binds": True}))