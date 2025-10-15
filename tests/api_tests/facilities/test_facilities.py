from httpx import Response



async def test_create(create_client):
    responce: Response = await create_client.post(
        url="/facilities/", json={"title": "Бесплатный WIFI"}
    )

    assert responce.status_code == 200
    assert responce.json()["data"] 

async def test_get_all(create_client):
    responce: Response = await create_client.get(url="/facilities/")

    assert responce.status_code == 200
    assert responce.json()


