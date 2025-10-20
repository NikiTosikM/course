from pydantic import ConfigDict
from src.core.schemas.base_schema import BaseModelSchema
from src.schemas.facility import FacilityResponceSchema


class RoomHotelSchema(BaseModelSchema):
    title: str
    description: str | None = None
    price: int
    quantity: int
    facilities_ids: list[int] = []

    model_config = ConfigDict(extra="ignore")


class RoomHotelFacilitieSchema(RoomHotelSchema):
    hotel_id: int


class RoomHotelAddSchema(BaseModelSchema):
    title: str
    description: str | None = None
    price: int
    quantity: int


class ResponceRoomHotelSchema(BaseModelSchema):
    id: int
    hotel_id: int
    title: str
    description: str | None = None
    price: int
    quantity: int
    facilities: list[FacilityResponceSchema] = []


class RequestRoomHotelPartialUpdateSchema(BaseModelSchema):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None
    facilities_ids: list[int] = []


class RoomHotelParticalUpdateSchema(BaseModelSchema):
    title: str | None = None
    description: str | None = None
    price: int | None = None
    quantity: int | None = None
