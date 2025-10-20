from datetime import date

from sqlalchemy import select, Result

from src.repositories.base_repository import BaseRepository
from src.models import Hotels, Rooms
from src.repositories.db_expressions import get_info_available_rooms
from src.schemas import HotelResponceSchema, PaginationHotels
from src.exceptions.exceptions import DateFromLaterDateToError


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
        if date_from > date_to:
            raise DateFromLaterDateToError

        result: Result = await self.session.execute(
            get_info_available_rooms(date_from=date_from, date_to=date_to)
        )
        ids_all_available_rooms: list[int] = result.scalars().all()

        ids_available_hotels = (
            select(Rooms.hotel_id)
            .select_from(Rooms)
            .where(Rooms.id.in_(ids_all_available_rooms))
        )

        query = (
            select(Hotels)
            .select_from(Hotels)
            .where(Hotels.id.in_(ids_available_hotels))
            .limit(pig_hotels.per_page)
            .offset((pig_hotels.page - 1) * pig_hotels.per_page)
        )
        if location:
            query = query.filter_by(location=location)
        if title:
            query = query.filter(Hotels.title.ilike(f"%{title}%"))

        result: Result = await self.session.execute(query)

        return [self.schema.model_validate(model) for model in result.scalars().all()]
