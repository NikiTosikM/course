from fastapi import APIRouter

from schemas.rooms import (
    RoomHotelSchema,
    ResponceRoomHotelSchema,
    UpdateRoomHotelSchema,
    RoomHotelPartialUpdateSchema,
)
from models.rooms import Rooms
from api.dependencies import DB_Dep


router = APIRouter(prefix="/hotels", tags=["Rooms"])


@router.get("/{hotel_id}/rooms")
async def get_all_rooms(hotel_id: int, db_manager: DB_Dep):
    rooms: list[Rooms] = await db_manager.room.get_filtered(
        hotel_id=hotel_id
    )

    return rooms


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(db_manager: DB_Dep, hotel_id: int, room_id: int):
    room: Rooms | None = await db_manager.room.get_one_or_none(hotel_id=hotel_id, id=room_id)

    return room


@router.post("/{hotel_id}")
async def create_room(db_manager: DB_Dep, hotel_id: int, room: RoomHotelSchema):
    room_data: ResponceRoomHotelSchema = await db_manager.room.add(data=room, hotel_id=hotel_id)
    await db_manager.commit()

    return room_data


@router.put("/{hotel_id}/rooms/{room_id}")
async def update_room(
    db_manager: DB_Dep, hotel_id: int, room_id: int, update_data_room: UpdateRoomHotelSchema
):
    await db_manager.room.update(data=update_data_room, hotel_id=hotel_id, id=room_id)
    await db_manager.commit()

    return {"status": "ok"}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def change_room(
    db_manager: DB_Dep, hotel_id: int, room_id: int, update_data_room: RoomHotelPartialUpdateSchema
):
    await db_manager.room.update(
            data=update_data_room, exclude_unset=True, hotel_id=hotel_id, id=room_id
        )
    await db_manager.commit()

    return {"status": "ok"}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(db_manager: DB_Dep, hotel_id: int, room_id: int):
    await db_manager.room.delete(
            id=room_id, hotel_id=hotel_id
        )
    await db_manager.commit()

    return {"status": "ok"}
