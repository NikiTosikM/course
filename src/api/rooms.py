from fastapi import APIRouter

from schemas.rooms import (
    RoomHotelSchema,
    ResponceRoomHotelSchema,
    UpdateRoomHotelSchema,
    RoomHotelPartialUpdateSchema,
)
from core.db.base_model import async_session_maker
from repositories.room_repository import RoomRepository
from models.rooms import Rooms


router = APIRouter(prefix="/hotels", tags=["Rooms"])


@router.get("/{hotel_id}")
async def get_all_rooms(hotel_id: int):
    async with async_session_maker() as session:
        rooms: list[ResponceRoomHotelSchema] = await RoomRepository(
            session=session, model=Rooms, schema=ResponceRoomHotelSchema
        ).get_rooms_by_hotel(hotel_id=hotel_id)

    return rooms


@router.get("/hotels/{hotel_id}/rooms/{room_id}")
async def get_room(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        room: Rooms | None = await RoomRepository(session=session, model=Rooms).get_one_or_none(
            hotel_id=hotel_id, id=room_id
        )
        
    return room
    


@router.post("/{hotel_id}")
async def create_room(hotel_id: int, room: RoomHotelSchema):
    async with async_session_maker() as session:
        room_data: ResponceRoomHotelSchema = await RoomRepository(
            session=session, model=Rooms, schema=RoomHotelSchema
        ).add(data=room, hotel_id=hotel_id)
        await session.commit()

    return room_data


@router.put("/{hotel_id}/rooms/{room_id}")
async def update_room(
    hotel_id: int, room_id: int, update_data_room: UpdateRoomHotelSchema
):
    async with async_session_maker() as session:
        await RoomRepository(
            session=session, model=Rooms, schema=UpdateRoomHotelSchema
        ).update(data=update_data_room, hotel_id=hotel_id, id=room_id)
        await session.commit()

    return {"status": "ok"}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def change_room(
    hotel_id: int, room_id: int, update_data_room: RoomHotelPartialUpdateSchema
):
    async with async_session_maker() as session:
        await RoomRepository(
            session=session, model=Rooms, schema=RoomHotelPartialUpdateSchema
        ).update(
            data=update_data_room, exclude_unset=True, hotel_id=hotel_id, id=room_id
        )
        await session.commit()

    return {"status": "ok"}


@router.delete("/hotels/{hotel_id}/rooms/{room_id}")
async def delete_room(hotel_id: int, room_id: int):
    async with async_session_maker() as session:
        await RoomRepository(session=session, model=Rooms).delete(
            id=room_id, hotel_id=hotel_id
        )
        await session.commit()

    return {"status": "ok"}
