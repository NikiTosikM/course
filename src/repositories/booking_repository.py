from repositories.base_repository import BaseRepository
from models.bookings import Booking
from schemas.bookings import DBBookingSchema


class BookingRepository(BaseRepository):
    def __init__(self, session, model, schema):
        super().__init__(session, model, schema)
        