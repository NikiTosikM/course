from sqlalchemy import select, Result, delete, insert

from src.repositories.base_repository import BaseRepository
from src.models.facilities import Facilities, RoomFacilities
from src.schemas.facility import FacilityResponceSchema


class FacilityRepository(BaseRepository[Facilities]):
    model = Facilities
    schema = FacilityResponceSchema


class RoomFacilitiesRepository(BaseRepository[RoomFacilities]):
    model = RoomFacilities

    async def update(
        self,
        necessary_ids_facilities: list[int],
        room_id: int,
    ):
        now_room_ids_facilities = (
            select(self.model.facility_id)
            .select_from(self.model)
            .filter(self.model.room_id == room_id)
        )
        result: Result = await self.session.execute(now_room_ids_facilities)
        now_room_ids_facilities = result.scalars().all()  # список всех удобств в бд

        delete_m2m_facilities = list(
            set(now_room_ids_facilities) - set(necessary_ids_facilities)
        )
        insert_m2m_facilities = list(
            set(necessary_ids_facilities) - set(now_room_ids_facilities)
        )

        if delete_m2m_facilities:
            delete_ids_stmt = delete(self.model).filter(
                self.model.facility_id.in_(delete_m2m_facilities)
            )
            await self.session.execute(delete_ids_stmt)
        if insert_m2m_facilities:
            insert_ids_stmt = insert(self.model).values(
                [
                    {"room_id": room_id, "facility_id": f_id}
                    for f_id in insert_m2m_facilities
                ]
            )
            await self.session.execute(insert_ids_stmt)
