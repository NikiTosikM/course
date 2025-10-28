from src.models.bookings import Booking
from src.service.base_service import BaseService
from src.api.dependencies import UserIdDepen
from src.schemas.bookings import RequestBookingSchema, DBResponceBookingSchema
from src.models import Rooms
from src.exceptions.exceptions import ObjectNotFoundError, RoomHotelBooked

class BookingService(BaseService):
    async def create_booking(self, booking_data: RequestBookingSchema, user_id: UserIdDepen):
        try:
            room: Rooms = await self.manager.room.get_one_or_none(
            room_id=booking_data.room_id,
            date_from=booking_data.date_from,
            date_to=booking_data.date_to,
            )
        except ObjectNotFoundError:
            raise RoomHotelBooked
        
        booking: DBResponceBookingSchema = await self.manager.booking.add_booking(
            booking_data=booking_data, room=room, user_id=user_id
        )
        await self.manager.commit()
        
        return booking
    
    async def get_all(self):
        bookings: list[Booking] = await self.manager.booking.get_all()
        
        return bookings
    
    async def get_specific(self, user_id: UserIdDepen):
        booking: list[Booking] = await self.manager.booking.get_filtered(user_id=user_id)
        
        return booking