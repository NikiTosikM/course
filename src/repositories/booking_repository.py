from datetime import date

from fastapi import HTTPException, status

from src.repositories.base_repository import BaseRepository
from src.models.bookings import Booking
from src.schemas.bookings import DBResponceBookingSchema
from src.repositories.db_expressions import get_info_available_rooms
from src.schemas import ResponceRoomHotelSchema, RequestBookingSchema, DBBookingSchema


class BookingRepository(BaseRepository):
    model = Booking
    schema = DBResponceBookingSchema

    def __init__(self, session):
        super().__init__(session)

    async def add_booking(
        self,
        booking_data: RequestBookingSchema,
        room: ResponceRoomHotelSchema,
        user_id: int
    ):
        if not room:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "message": "seats are occupied",
                    "detail": "all seats in this room are occupied during this period",
                },
            )

        room_price = room.price
        total_cost_booking: int = (
            room_price * (booking_data.date_to - booking_data.date_from).days
        )

        booking_schema = DBBookingSchema(
            user_id=user_id, price=total_cost_booking, **booking_data.model_dump()
        )
        
        return await self.add(data=booking_schema) 
