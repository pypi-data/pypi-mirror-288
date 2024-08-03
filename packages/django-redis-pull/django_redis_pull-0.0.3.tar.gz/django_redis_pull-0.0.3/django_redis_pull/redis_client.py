from django.conf import settings
import redis

REDIS_CLIENT = redis.Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB,
    charset="utf-8",
    decode_responses=True,
)
