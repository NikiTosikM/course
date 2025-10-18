import asyncio
from httpx import Response, AsyncClient, ASGITransport
import pytest

from tests.parametrize_datas.auth import datas_for_full_check_user
from src.schemas.user import UserResponceSchema


@pytest.mark.parametrize(
    "name, email, password, status_code", datas_for_full_check_user
)
async def test_full_check_user(name, email, password, status_code, async_client):
    # register
    register_res: Response = await async_client.post(
        url="/auth/register", json={"name": name, "email": email, "password": password}
    )
    assert register_res.status_code == status_code
    assert register_res.json()

    if register_res.status_code != 200:
        return

    # login
    login_res: Response = await async_client.post(
        url="/auth/login", json={"email": email, "password": password}
    )
    assert login_res.status_code == status_code
    assert async_client.cookies.get("access_token")

    # info about user
    about_res: Response = await async_client.get(url="/auth/me")
    user_data: dict = UserResponceSchema.model_validate(about_res.json())
    assert about_res.status_code == status_code
    assert not all(parametr not in user_data for parametr in user_data)

    # logout
    logout_res: Response = await async_client.post(url="/auth/logout")
    assert logout_res.status_code == status_code
    assert not async_client.cookies.get("access_token")
