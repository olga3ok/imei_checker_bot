import aioredis
from dotenv import load_dotenv
import os

load_dotenv()

REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')

async def get_redis_client():
    """
    Возвращает клиент Redis
    """
    try:
        redis = await aioredis.from_url(REDIS_URL)

        return redis
    except aioredis.exceptions.ConnectionError as e:
        print(f"Error connecting to Redis: {e}")
        return None