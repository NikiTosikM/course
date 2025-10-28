from fastapi import APIRouter

from src.schemas.bookings import (
    RequestBookingSchema,
)
from src.api.dependencies import UserIdDepen, DB_Dep
from src.models import  Booking
from src.service.bookings_service import BookingService
from src.exceptions.exceptions import RoomHotelBooked,  RoomHotelBookedHTTPException

router = APIRouter(prefix="/bookings", tags=["Заказы"])


@router.post("/")
async def create_booking(
    booking_data: RequestBookingSchema, user_id: UserIdDepen, db_manager: DB_Dep
):
    try:
        booking = await BookingService(manager=db_manager).create_booking(booking_data, user_id)
    except RoomHotelBooked:
        raise RoomHotelBookedHTTPException

    return {"status": "ok", "booking": booking}


@router.get("/")
async def get_all(db_manager: DB_Dep):
    bookings: list[Booking] = await BookingService(db_manager).get_all()
    
    return bookings


@router.get("/me")
async def get_specific(db_manager: DB_Dep, user_id: UserIdDepen):
    booking: list[Booking] = await BookingService(db_manager).get_specific(user_id)    
    
    return booking
