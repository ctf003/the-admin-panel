from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os

redis_url = os.environ.get('REDIS_URL', 'redis://redis:6379')

limiter = Limiter(
    key_func=get_remote_address,
    storage_uri=redis_url,
    default_limits=["60 per minute"]
)
