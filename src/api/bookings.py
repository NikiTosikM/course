from fastapi import APIRouter

from schemas.bookings import (
    RequestBookingSchema,
    DBBookingSchema,
    DBResponceBookingSchema,
)
from api.dependencies import UserIdDepen, DB_Dep
from models import Rooms, Booking


router = APIRouter(prefix="/bookings", tags=["Заказы"])


@router.post("/")
async def create_booking(
    booking_data: RequestBookingSchema, user_id: UserIdDepen, db_manager: DB_Dep
):
    room: Rooms = await db_manager.room.get_one_or_none(id=booking_data.room_id)
    total_cost_booking: int = Booking(
        date_from=booking_data.date_from, date_to=booking_data.date_to, price=room.price
    ).total_price

    booking = DBBookingSchema(
        user_id=user_id, price=total_cost_booking, **booking_data.model_dump()
    )

    booking: DBResponceBookingSchema = await db_manager.booking.add(data=booking)
    await db_manager.commit()
    
    return {"status": "ok", "booking": booking}
