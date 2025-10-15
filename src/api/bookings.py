from fastapi import APIRouter

from schemas.bookings import (
    RequestBookingSchema,
    DBBookingSchema,
    DBResponceBookingSchema,
)
from src.api.dependencies import UserIdDepen, DB_Dep
from models import Rooms, Booking


router = APIRouter(prefix="/bookings", tags=["Заказы"])


@router.post("/")
async def create_booking(
    booking_data: RequestBookingSchema, user_id: UserIdDepen, db_manager: DB_Dep
):
    room: Rooms = await db_manager.room.get_one_or_none(id=booking_data.room_id)
    room_price = room.price
    total_cost_booking: int = (
        room_price * (booking_data.date_to - booking_data.date_from).days
    )

    booking = DBBookingSchema(
        user_id=user_id, price=total_cost_booking, **booking_data.model_dump()
    )

    booking: DBResponceBookingSchema = await db_manager.booking.add(data=booking)
    await db_manager.commit()

    return {"status": "ok", "booking": booking}


@router.get("/")
async def get_all(
    db_manager: DB_Dep
):
    bookings: list[Booking] = await db_manager.booking.get_all()
    
    return bookings


@router.get("/me")
async def get_specific(db_manager: DB_Dep, user_id: UserIdDepen):
    bookings: list[Booking] = await db_manager.booking.get_filtered(user_id=user_id)
    
    return bookings