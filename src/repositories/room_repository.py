from repositories.base_repository import BaseRepository, Model
from sqlalchemy import insert, Result, select
from sqlalchemy.orm import selectinload

from src.models import Rooms
from schemas.rooms import RoomHotelSchema, ResponceRoomHotelSchema
from repositories.db_expressions import (
    get_info_available_rooms,
)


class RoomRepository(BaseRepository[Rooms]):
    model: Model = Rooms
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
        ids_free_rooms_sql_exper = get_info_available_rooms(
            date_from=date_from, date_to=date_to, hotel_id=hotel_id
        )
        query_free_rooms = (
            select(Rooms)
            .options(selectinload(Rooms.facilities))
            .filter(Rooms.id.in_(ids_free_rooms_sql_exper))
            .filter_by(hotel_id=hotel_id)
        )
        result = await self.session.execute(
            query_free_rooms
        )  # получили информацию про свободные комнаты
        free_room = [
            ResponceRoomHotelSchema.model_validate(room)
            for room in result.scalars().all()
        ]

        ids_count_available_rooms_sql_exper = get_info_available_rooms(
            date_from=date_from, date_to=date_to, hotel_id=hotel_id, only_ids=False
        )
        result = await self.session.execute(ids_count_available_rooms_sql_exper)
        id_count_available_room = {room[0]: room[1] for room in result.all()}
        for room in free_room:
            room.quantity = id_count_available_room[room.id]

        return free_room
        
    async def get_one_or_none(self, **filter_by):
        query = (
            select(Rooms)
            .options(selectinload(Rooms.facilities))
            .filter_by(**filter_by)
        )
        result = await self.session.execute(query)
        return [
            ResponceRoomHotelSchema.model_validate(room)
            for room in result.scalars().all()
        ]
