from src.repositories.hotel_repository import HoterRepository
from src.repositories.room_repository import RoomRepository
from src.repositories.user_repository import UserRepository
from src.repositories.booking_repository import BookingRepository
from src.repositories.facility_repository import FacilityRepository, RoomFacilitiesRepository


class DBManager:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session = self.session_factory()

        self.user: UserRepository = UserRepository(session=self.session)
        self.room = RoomRepository(session=self.session)
        self.hotel = HoterRepository(session=self.session)
        self.booking = BookingRepository(
            session=self.session
        )
        self.facility = FacilityRepository(session=self.session)
        self.room_facility = RoomFacilitiesRepository(session=self.session)

        return self

    async def __aexit__(self, *args):
        await self.session.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()
