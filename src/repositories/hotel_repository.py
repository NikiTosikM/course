from datetime import date

from sqlalchemy import select, Result

from repositories.base_repository import BaseRepository
from models import Hotels, Rooms
from repositories.db_expressions import getting_available_rooms
from schemas import HotelResponceSchema, PaginationHotels


class HoterRepository(BaseRepository[Hotels]):
    model = Hotels
    schema = HotelResponceSchema

    def __init__(self, session):
        super().__init__(session)

    async def get_filtered(
        self,
        date_from: date,
        date_to: date,
        pig_hotels: PaginationHotels,
        location: str | None,
        title: str | None,
    ) -> list[Hotels] | None:
        result: Result = await self.session.execute(
            getting_available_rooms(date_from=date_from, date_to=date_to)
        )
        ids_all_available_rooms: list[int] = result.scalars().all()

        ids_available_hotels = select(Rooms.hotel_id).select_from(Rooms)
        if location:
            ids_available_hotels = ids_available_hotels.outerjoin(
                Hotels, Rooms.hotel_id == Hotels.id
            ).filter_by(location=location)
        if title:
            ids_available_hotels = ids_available_hotels.filter(
                Hotels.title.ilike(f"%{title}%")
            )
        ids_available_hotels = (
            ids_available_hotels.where(Rooms.id.in_(ids_all_available_rooms))
            .limit(pig_hotels.per_page)
            .offset((pig_hotels.page - 1) * 5)
        )

        return await self.get_filtered(Hotels.id.in_(ids_available_hotels))
