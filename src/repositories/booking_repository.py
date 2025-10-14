from repositories.base_repository import BaseRepository
from models.bookings import Booking
from repositories.mappers.mappers import BookingDataMapper
from schemas.bookings import DBResponceBookingSchema


class BookingRepository(BaseRepository):
    model = Booking
    schema = DBResponceBookingSchema
    
    def __init__(self, session):
        super().__init__(session)
        