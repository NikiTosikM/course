from datetime import date

from src.core.schemas.base_schema import BaseModelSchema

from pydantic import Field


class RequestBookingSchema(BaseModelSchema):
    room_id: int = Field(ge=0)
    date_from: date
    date_to: date


class DBBookingSchema(RequestBookingSchema):
    user_id: int
    price: int = Field(ge=0)


class DBResponceBookingSchema(DBBookingSchema):
    id: int
