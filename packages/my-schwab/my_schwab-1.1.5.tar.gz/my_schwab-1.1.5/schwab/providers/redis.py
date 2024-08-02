from .base import Provider

try:
    from redis import Redis
    from redis.backoff import ExponentialBackoff
    from redis.retry import Retry
    from redis.client import Redis
    from redis.exceptions import (
    BusyLoadingError,
    ConnectionError,
    TimeoutError
    )
except ImportError:
    raise ImportError("Redis provider requires redis")

retry = Retry(ExponentialBackoff(), retries=3)
retry_errors = (ConnectionError, TimeoutError, BusyLoadingError)

class RedisProvider(Provider):
    __slots__ = ('_db',)

    def __init__(self, key='schwab', encrypt=False,  host='localhost', port=6379, db=0, protocol=3, decode_responses=True, **kwargs):
        super().__init__(key=key, encrypt=encrypt, **kwargs)
        self._db = Redis(
            host=host,
            port=port,
            db=db,
            protocol=protocol,
            decode_responses=decode_responses,
            retry=retry,
            retry_on_error=retry_errors,
            **kwargs
        )
        self._db.ping()
        print("Redis provider initialized")

    def close(self):
        self._db.close()

    def retrieve(self, key=None, **kwargs):
        key = key or self._key
        return self._db.hgetall(name=key)

    def store(self, key=None, data=None, **kwargs):
        key = key or self._key
        print(f"Storing data: {data}")
        if data is None:
            raise ValueError('Data must be provided')
        self._db.hset(name=key, mapping=data)