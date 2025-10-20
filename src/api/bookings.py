from fastapi import APIRouter

from src.schemas.bookings import (
    RequestBookingSchema,
    DBResponceBookingSchema,
)
from src.api.dependencies import UserIdDepen, DB_Dep
from src.models import Rooms, Booking


router = APIRouter(prefix="/bookings", tags=["Заказы"])


@router.post("/")
async def create_booking(
    booking_data: RequestBookingSchema, user_id: UserIdDepen, db_manager: DB_Dep
):
    room: Rooms = await db_manager.room.get_one_or_none(
        room_id=booking_data.room_id,
        date_from=booking_data.date_from,
        date_to=booking_data.date_to,
    )
    booking: DBResponceBookingSchema = await db_manager.booking.add_booking(
        booking_data=booking_data, room=room, user_id=user_id
    )
    await db_manager.commit()

    return {"status": "ok", "booking": booking}


@router.get("/")
async def get_all(db_manager: DB_Dep):
    bookings: list[Booking] = await db_manager.booking.get_all()

    return bookings


@router.get("/me")
async def get_specific(db_manager: DB_Dep, user_id: UserIdDepen):
    bookings: list[Booking] = await db_manager.booking.get_filtered(user_id=user_id)

    return bookings
