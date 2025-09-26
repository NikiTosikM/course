from core.schemas.base_schema import BaseModelSchema


class RoomHotelSchema(BaseModelSchema):
    title: str
    description: str | None = None
    price: int
    quantity: int
    facilities_ids: list[int] = []
    

class RoomHotelAddSchema(BaseModelSchema):
    title: str
    description: str | None = None
    price: int
    quantity: int
    
class ResponceRoomHotelSchema(RoomHotelSchema): 
    id: int
    hotel_id: int
    

class UpdateRoomHotelSchema(RoomHotelSchema):
    hotel_id: int
    

class RoomHotelPartialUpdateSchema(BaseModelSchema):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None