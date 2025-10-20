from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.core.config import settings


class Base(DeclarativeBase):
    pass


async_engine = create_async_engine(url=settings.db.get_db_url, echo=True)

async_session_maker: async_sessionmaker = async_sessionmaker(
    async_engine, expire_on_commit=False
)
