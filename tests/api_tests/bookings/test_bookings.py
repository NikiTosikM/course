from httpx import Response
import pytest

from tests.parametrize_datas.bookings import datas_for_test_add_get_user_bookings
from src.schemas.bookings import DBResponceBookingSchema
from tests.conftest import test_db_manager


# async def test_create_booking(authorized_user, db_manager):
#     room_id: int = (await db_manager.room.get_all())[0].id
#     responce: Response = await authorized_user.post(
#         url="/bookings/",
#         json={"room_id": room_id, "date_from": "2025-01-01", "date_to": "2025-01-10"},
#     )
#     responce_data: dict = responce.json()

#     assert responce.status_code == 200
#     assert responce_data.get("status") == "ok"
#     assert responce_data.get("booking")


@pytest.fixture(scope="session")
async def delete_bookings():
    async for db in test_db_manager():
        await db.booking.delete()
        await db.commit()


@pytest.mark.parametrize(
    "room_id, date_from, date_to, count_user_bookings, status_code",
    datas_for_test_add_get_user_bookings,
)
async def test_add_get_user_bookings(
    delete_bookings,
    authorized_user,
    room_id,
    date_to,
    date_from,
    count_user_bookings,
    status_code,
):
    create_booking_responce: Response = await authorized_user.post(
        url="/bookings/",
        json={
            "room_id": room_id,
            "date_to": date_to,
            "date_from": date_from,
        },
    )
    assert create_booking_responce.status_code == status_code

    get_booking_responce: Response = await authorized_user.get(url="/bookings/me")
    user_bookings: list[DBResponceBookingSchema] = get_booking_responce.json()

    assert len(user_bookings) == count_user_bookings
