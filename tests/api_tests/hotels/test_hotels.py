from httpx import Response


async def test_get_hotels(create_client):
    responce: Response = await create_client.get(
        url="/hotels",
        params={
            "date_from": "2025-10-10",
            "date_to": "2025-10-15"
        }
    )
    
    assert responce.status_code == 200
    assert responce.json()
    print(responce.json())