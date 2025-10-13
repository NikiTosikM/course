from tests.conftest import async_session_maker

from src.utils.db.db_manager import DBManager
from src.schemas import HotelSchema, HotelResponceSchema


async def test_create_hotel():
    hotel = HotelSchema(title="Samara five stars", location="Samara")
    async with DBManager(session_factory=async_session_maker) as db_manager:
        responce_hotel: HotelResponceSchema = await db_manager.hotel.add(data=hotel)
        await db_manager.commit()
        
        received_hotel: HotelResponceSchema = await db_manager.hotel.specific_object(
            hotel_id=responce_hotel.id
        )
        
        assert responce_hotel == received_hotel