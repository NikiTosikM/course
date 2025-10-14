from contextlib import asynccontextmanager

from redis.asyncio import Redis, ConnectionPool, ConnectionError

from core.config import settings



class RedisConfig:
    def __init__(self, host: str, port: int, max_connection: int):
        self.host = host
        self.port = port
        self.max_connection = max_connection
        self.client = None
        
    def connect(self):
        self.client = Redis(host=self.host, port=self.port)
        
    async def close(self):
        await self.client.aclose()
        
    async def set(self, key: str, value: str, expire: int = None):
        if expire:
            await self.client.set(key, value, ex=expire)
        else:
            await self.client.set(key, value)

    async def get(self, key: str):
        return await self.client.get(key)

    async def delete(self, key: str):
        await self.client.delete(key)
            
    
redis_manager = RedisConfig(
    host=settings.redis.host,
    port=settings.redis.port, 
    max_connection=settings.redis.max_connection
)


            
    