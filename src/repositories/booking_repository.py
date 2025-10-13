from repositories.base_repository import BaseRepository
from models.bookings import Booking
from repositories.mappers.mappers import BookingDataMapper


class BookingRepository(BaseRepository):
    model = Booking
    mapper = BookingDataMapper
    
    def __init__(self, session):
        super().__init__(session)
        