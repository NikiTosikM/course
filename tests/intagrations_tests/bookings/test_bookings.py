from datetime import date

from src.schemas.bookings import DBBookingSchema, DBResponceBookingSchema


async def test_create_booking(db_manager):
    # create
    user_id = (await db_manager.user.get_all())[0].id
    room_id = (await db_manager.room.get_all())[0].id

    date_from = date(year=2025, month=10, day=10)
    date_to = date(year=2025, month=10, day=15)

    booking = DBBookingSchema(
        room_id=room_id,
        user_id=user_id,
        price=20000,
        date_from=date_from,
        date_to=date_to,
    )
    booking_add: DBResponceBookingSchema = await db_manager.booking.add(booking)

    # read
    booking_read: DBResponceBookingSchema = await db_manager.booking.get_one_or_none(
        id=booking_add.id
    )
    assert booking_read
    assert booking_read.id == booking_add.id

    # update
    booking = DBBookingSchema(
        room_id=room_id,
        user_id=user_id,
        price=30000,
        date_from=date(year=2025, month=10, day=20),
        date_to=date(year=2025, month=10, day=25),
    )
    await db_manager.booking.update(data=booking, id=booking_read.id)
    update_booking: DBResponceBookingSchema = await db_manager.booking.get_one_or_none(
        id=booking_add.id
    )
    assert update_booking.id == booking_read.id
    assert update_booking.date_from == booking.date_from
    assert update_booking.date_to == booking.date_to

    # # delete
    await db_manager.booking.delete(id=booking_read.id)
    booking_delete: DBResponceBookingSchema = await db_manager.booking.get_one_or_none(
        id=booking_add.id
    )
    assert booking_delete is None

    await db_manager.commit()
