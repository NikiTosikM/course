from  httpx import Response


async def test_create_booking(authorized_user, db_manager):
    room_id: int = (await db_manager.room.get_all())[0].id
    responce: Response = await authorized_user.post(
        url="/bookings/",
        json={  
            "room_id": room_id,
            "date_from": "2025-01-01",
            "date_to": "2025-01-10"
        }
    )
    responce_data: dict = responce.json()
    
    assert responce.status_code == 200
    assert responce_data.get("status") == "ok"
    assert responce_data.get("booking")