from src.schemas import HotelSchema, HotelResponceSchema


async def test_create_hotel(db_manager):
    hotel = HotelSchema(title="Samara five stars", location="Samara")
    responce_hotel: HotelResponceSchema = await db_manager.hotel.add(data=hotel)
    await db_manager.commit()
        
    received_hotel: HotelResponceSchema = await db_manager.hotel.specific_object(
            hotel_id=responce_hotel.id
        )
        
    assert responce_hotel == received_hotel
    
    