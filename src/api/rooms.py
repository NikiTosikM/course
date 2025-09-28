from typing import Annotated
from datetime import date

from fastapi import APIRouter, Query

from schemas.rooms import (
    RoomHotelSchema,
    ResponceRoomHotelSchema,
    UpdateRoomHotelSchema,
    RequestRoomHotelPartialUpdateSchema,
    RoomHotelParticalUpdateSchema,
    RoomHotelAddSchema,
)
from schemas.facility import RoomFacilityAddSchema
from models.rooms import Rooms
from api.dependencies import DB_Dep


router = APIRouter(prefix="/hotels", tags=["Rooms"])


@router.get("/{hotel_id}/rooms")
async def get_all_rooms(
    hotel_id: int,
    db_manager: DB_Dep,
    data_from: Annotated[
        date, Query(description="Дата заезда в номер", example="2025-09-10")
    ],
    data_to: Annotated[
        date, Query(description="Дата выезда из номера", example="2025-09-15")
    ],
):
    rooms: list[Rooms] = await db_manager.room.get_all(
        date_from=data_from, date_to=data_to, hotel_id=hotel_id
    )

    return rooms


@router.get("/{hotel_id}/rooms/{room_id}")
async def get_room(db_manager: DB_Dep, hotel_id: int, room_id: int):
    room: Rooms | None = await db_manager.room.get_one_or_none(
        hotel_id=hotel_id, id=room_id
    )

    return room


@router.post("/{hotel_id}")
async def create_room(
    db_manager: DB_Dep,
    hotel_id: int,
    room: RoomHotelSchema,
):
    room_data = RoomHotelAddSchema(**room.model_dump())
    room_data: ResponceRoomHotelSchema = await db_manager.room.add(
        data=room_data, hotel_id=hotel_id
    )

    room_facilities = [
        RoomFacilityAddSchema(room_id=room_data.id, facility_id=facil_id)
        for facil_id in room.facilities_ids
    ]
    await db_manager.room_facility.add_bulk(room_facilities)

    await db_manager.commit()

    return room_data


@router.put("/{hotel_id}/rooms/{room_id}")
async def update_room(
    db_manager: DB_Dep,
    hotel_id: int,
    room_id: int,
    update_data_room: UpdateRoomHotelSchema,
):
    room_data = RoomHotelAddSchema(**update_data_room.model_dump())
    await db_manager.room.update(data=room_data, hotel_id=hotel_id, id=room_id)

    await db_manager.room_facility.update(
        room_id=room_id, necessary_ids_facilities=update_data_room.facilities_ids
    )

    await db_manager.commit()

    return {"status": "ok"}


@router.patch("/{hotel_id}/rooms/{room_id}")
async def change_room(
    db_manager: DB_Dep,
    hotel_id: int,
    room_id: int,
    update_data_room: RequestRoomHotelPartialUpdateSchema,
):
    room_data = RoomHotelParticalUpdateSchema(
        **update_data_room.model_dump(exclude_unset=True)
    )
    if room_data:
        await db_manager.room.update(
            data=room_data, exclude_unset=True, hotel_id=hotel_id, id=room_id
        )
    if update_data_room.facilities_ids:
        await db_manager.room_facility.update(
            necessary_ids_facilities=update_data_room.facilities_ids, room_id=room_id
        )

    await db_manager.commit()

    return {"status": "ok"}


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(db_manager: DB_Dep, hotel_id: int, room_id: int):
    await db_manager.room.delete(id=room_id, hotel_id=hotel_id)
    await db_manager.commit()

    return {"status": "ok"}
