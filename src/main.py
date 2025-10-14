from contextlib import asynccontextmanager

from fastapi import FastAPI

import uvicorn
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from api import main_router
from core.redis_.redis_connector import redis_manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_manager.connect()
    FastAPICache.init(RedisBackend(redis_manager.client), prefix="fastapi-cache")
    yield
    await redis_manager.close()


app = FastAPI(lifespan=lifespan)


        
app.include_router(main_router)


def main():
    uvicorn.run("main:app", reload=True)


if __name__ == "__main__":
    main()
