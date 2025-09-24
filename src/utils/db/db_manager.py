from repositories.hotel_repository import HoterRepository
from repositories.room_repository import RoomRepository
from repositories.user_repository import UserRepository
from repositories.booking_repository import BookingRepository
from models import User, Rooms, Hotels, Booking
from schemas import DBResponceBookingSchema


class DBManager:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()

        self.user = UserRepository(session=self.session)
        self.room = RoomRepository(session=self.session)
        self.hotel = HoterRepository(session=self.session)
        self.booking = BookingRepository(
            session=self.session
        )

        return self

    async def __aexit__(self, *args):
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()
