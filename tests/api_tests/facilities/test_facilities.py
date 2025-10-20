from httpx import Response


async def test_get_all(async_client):
    responce: Response = await async_client.get(url="/facilities/")

    assert responce.status_code == 200
    assert isinstance(responce.json(), list)


async def test_create(async_client):
    responce: Response = await async_client.post(
        url="/facilities/", json={"title": "Бесплатный WIFI"}
    )

    assert responce.status_code == 200
    assert responce.json()["data"]
