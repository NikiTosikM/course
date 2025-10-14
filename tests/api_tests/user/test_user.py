from httpx import Response


async def test_register(create_client):
    responce: Response = await create_client.post(
        url="/auth/register",
        json={
            "name": "nikita",
            "email": "1234@mail.ru",
            "password": "1234567899"
        }
    )
    
    assert responce.status_code == 200