from datetime import date

from sqlalchemy import func, select

from models import Booking, Rooms


def getting_available_rooms(
    date_from: date,
    date_to: date,
    hotel_id: int | None = None,
    room_id: int | None = None,
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
    )  # получаю id комнаты и количество свободных мест
    rooms_ids_for_hotel = select(Rooms.id)
    if room_id:
        rooms_ids_for_hotel = rooms_ids_for_hotel.filter_by(id=room_id)
    elif hotel_id:
        rooms_ids_for_hotel = rooms_ids_for_hotel.filter_by(hotel_id=hotel_id)
    rooms_ids_for_hotel = rooms_ids_for_hotel.subquery(
        name="available_rooms"
    )  # получаем id номеров, которые принадлежат отелю

    return free_rooms, rooms_ids_for_hotel


def get_info_available_rooms(
    date_from: date,
    date_to: date,
    hotel_id: int | None = None,
    only_ids: bool = True,
    room_id: int | None = None,
):
    free_rooms, rooms_ids_for_hotel = getting_available_rooms(
        date_from=date_from, date_to=date_to, hotel_id=hotel_id, room_id=room_id
    )
    if only_ids:
        query = select(free_rooms.c.room_id)
    else:
        query = select(free_rooms.c.room_id, free_rooms.c.count_free_rooms)
    query = query.select_from(free_rooms).where(
        free_rooms.c.count_free_rooms > 0,
        free_rooms.c.room_id.in_(rooms_ids_for_hotel),
    )

    return query
