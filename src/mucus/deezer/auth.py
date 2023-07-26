import redis

from mucus.deezer.exception import AuthException


def discover(key):
    try:
        with redis.Redis(decode_responses=True) as db:
            value = db.get(f'mucus:deezer:{key}')
            if value is not None:
                return value
    except redis.exceptions.RedisError:
        pass
    raise AuthException(key)


class Auth:
    def __init__(self, sid=None, arl=None):
        if sid is None:
            sid = discover('sid')
        if arl is None:
            arl = discover('arl')
        self.sid = sid
        self.arl = arl
