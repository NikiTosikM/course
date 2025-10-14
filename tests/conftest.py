import json

import pytest
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from httpx import AsyncClient, ASGITransport

from src.core.config import settings
from src.core.db.base_model import Base
from src.models import *  # noqa: F403
from src.utils.db.db_manager import DBManager
from src.schemas.hotels import HotelSchema
from src.schemas.rooms import RoomHotelFacilitieSchema
from src.main import app


engine_null_pool = create_async_engine(settings.db.get_db_url, poolclass=NullPool)
async_session_maker = async_sessionmaker(engine_null_pool, expire_on_commit=False)


@pytest.fixture(autouse=True, scope="session")
async def create_tables():
    assert settings.mode == "TEST"

    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        

@pytest.fixture(autouse=True, scope="session")
async def adding_data_to_database(create_tables):
        with open("tests/db_datas/mock_hotels.json", encoding="utf-8") as file:
            file_hotels = json.load(file)

        with open("tests/db_datas/mock_rooms.json", encoding="utf-8") as file:
            file_rooms = json.load(file)
            rooms_schemas = [RoomHotelFacilitieSchema(**room) for room in file_rooms]
            
        hotels_schemes = [HotelSchema(**hotel) for hotel in file_hotels]
        rooms_schemas = [RoomHotelFacilitieSchema(**room) for room in file_rooms]
            
        async with DBManager(session_factory=async_session_maker) as db_man:
            await db_man.hotel.add_bulk(hotels_schemes)
            await db_man.room.add_bulk(rooms_schemas)
            
            await db_man.commit()
        

@pytest.fixture()
async def db_manager() -> DBManager:
    async with DBManager(session_factory=async_session_maker) as db:
        yield db


@pytest.fixture(scope="session")
async def create_client() -> AsyncClient:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client
        
        
@pytest.fixture(scope="session" ,autouse=True)
async def register_user(create_client):
    await create_client.post(
        url="/auth/register",
        json={
            "name": "nikita",
            "email": "12345@mail.ru",
            "password": "1234567899"
        }
    )