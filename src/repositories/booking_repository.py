from repositories.base_repository import BaseRepository
from models.bookings import Booking
from schemas.bookings import DBBookingSchema


class BookingRepository(BaseRepository):
    model = Booking
    
    def __init__(self, session):
        super().__init__(session)
        