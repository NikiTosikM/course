from fastapi import HTTPException, status
from sqlalchemy import Result, insert, select
from sqlalchemy.orm import selectinload

from src.models import Rooms
from src.repositories.base_repository import BaseRepository, DBModel
from src.repositories.db_expressions import (
    get_info_available_rooms,
)
from src.schemas.rooms import ResponceRoomHotelSchema, RoomHotelSchema


class RoomRepository(BaseRepository[Rooms]):
    model: DBModel = Rooms
    schema = ResponceRoomHotelSchema

    def __init__(self, session):
        super().__init__(session)

    async def get_filtered(
        self, *expressions, **filters
    ) -> list[ResponceRoomHotelSchema]:
        query = (
            select(self.model)
            .options(selectinload(Rooms.facilities))
            .filter(*expressions)
            .filter_by(**filters)
        )
        result: Result = await self.session.execute(query)
        return [self.schema.model_validate(model) for model in result.scalars().all()]

    async def add(self, data: RoomHotelSchema, **values) -> ResponceRoomHotelSchema:
        stmt = (
            insert(self.model)
            .values(**data.model_dump(), **values)
            .returning(self.model)
        )
        result: Result = await self.session.execute(stmt)

        return result.scalar_one()

    async def _get_available_rooms(
        self,
        date_from: str,
        date_to: str,
        hotel_id: int | None = None,
        room_id: int | None = None,
        **filters,
    ):
        # формируем запрос
        ids_free_rooms_sql_exper = get_info_available_rooms(
            date_from=date_from, date_to=date_to, hotel_id=hotel_id, room_id=room_id
        )
        query_free_rooms = (
            select(Rooms)
            .options(selectinload(Rooms.facilities))
            .filter(Rooms.id.in_(ids_free_rooms_sql_exper))
            .filter_by(**filters)
        )
        # получаем информацию про свободные комнаты
        result = await self.session.execute(query_free_rooms)
        rooms = [
            ResponceRoomHotelSchema.model_validate(room)
            for room in result.scalars().all()
        ]  # создаем схему комнаты с удобствами

        ids_count_available_rooms_sql_exper = get_info_available_rooms(
            date_from=date_from, date_to=date_to, hotel_id=hotel_id, only_ids=False
        )
        result = await self.session.execute(ids_count_available_rooms_sql_exper)
        id_count_available_room = {room[0]: room[1] for room in result.all()}
        for room in rooms:
            room.quantity = id_count_available_room[room.id]

        return rooms

    async def get_all_free_rooms(self, date_from: str, date_to: str, hotel_id: int):
        return await self._get_available_rooms(date_from, date_to, hotel_id)

        # print("вот запрос", query.compile(bind=async_engine, compile_kwargs={"literal_binds": True}))

    async def get_one_or_none(
        self,
        date_from: str,
        date_to: str,
        hotel_id: int | None = None,
        room_id: int | None = None,
        **filter_by,
    ):
        id_room: list[Rooms] = await self._get_available_rooms(
            date_from=date_from,
            date_to=date_to,
            hotel_id=hotel_id,
            room_id=room_id,
            **filter_by,
        )

        return id_room[0] if id_room else None
