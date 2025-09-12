from sqlalchemy import select, Result

from repositories.base_repository import BaseRepository
from models.hotels import Hotels


class HoterRepository(BaseRepository[Hotels]):
    def __init__(self, session, model):
        super().__init__(session, model)

    async def get_all(
        self, location: str, title: str, page: int, per_page: int
    ) -> list[Hotels] | None:
        query = select(Hotels)
        if title:
            query = query.where(Hotels.title.ilike(f"%{title}%"))
        if location:
            query = query.where(Hotels.location.ilike(f"%{location}%"))
        query = query.limit(per_page).offset((page - 1) * per_page)
        result: Result = await self.session.execute(query)

        return result.scalars().all()
