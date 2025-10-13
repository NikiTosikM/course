from repositories.mappers.base_mapper import BaseDataMapper
from models import Hotels, Rooms, User, Booking, Facilities, RoomFacilities
from schemas import (
    ResponceRoomHotelSchema,
    DBResponceBookingSchema,
    RoomFacilityResponceSchema,
    HotelResponceSchema,
    FacilityResponceSchema
)


class UserDataMapper(BaseDataMapper):
    model = User
    schema = ResponceRoomHotelSchema


class BookingDataMapper(BaseDataMapper):
    model = Booking
    schema = DBResponceBookingSchema


class FacilityDataMapper(BaseDataMapper):
    model = Facilities
    schema = FacilityResponceSchema
    
class RoomFacilityDataMapper(BaseDataMapper):
    model = RoomFacilities
    schema = RoomFacilityResponceSchema

class HotelDataMapper(BaseDataMapper):
    model = Hotels
    schema = HotelResponceSchema


class RoomDataMapper(BaseDataMapper):
    model = Rooms
    schema = ResponceRoomHotelSchema
