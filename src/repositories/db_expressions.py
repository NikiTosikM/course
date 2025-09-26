from datetime import date

from sqlalchemy import select, func
from sqlalchemy.sql import Select
from models import Rooms, Booking, RoomFacilities


def getting_available_rooms(
    date_from: date,
    date_to: date,
    hotel_id: int | None = None
):
    room_booking = (
            select(Booking.room_id, func.count("*").label("count_booked_rooms"))
            .select_from(Booking)
            .filter(Booking.date_from <= date_to, Booking.date_to >= date_from)
            .group_by(Booking.room_id)
            .cte("room_booking")
        )
    free_rooms = (
        select(
            Rooms.id.label("room_id"),
            (
                Rooms.quantity - func.coalesce(room_booking.c.count_booked_rooms, 0)
            ).label("count_free_rooms"),
        )
        .select_from(Rooms)
        .outerjoin(room_booking, Rooms.id == room_booking.c.room_id)
        .cte("free_rooms")
    )
    available_rooms: Select = (
        select(Rooms.id)
        .select_from(Rooms)
    ) # получение свободных  комнат
    if hotel_id:
        available_rooms = available_rooms.filter_by(hotel_id=hotel_id)
    rooms_ids_for_hotel = (
        select(Rooms.id)
        .subquery(name="available_rooms")
    )
    query = (
        select(free_rooms.c.room_id, free_rooms.c.count_free_rooms)
        .select_from(free_rooms)
        .where(
            free_rooms.c.count_free_rooms > 0,
            free_rooms.c.room_id.in_(rooms_ids_for_hotel),
        )
    )
    
    return query

