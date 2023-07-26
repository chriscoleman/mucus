import httpx
import redis

from mucus.deezer.exception import AuthException


def discover(key):
    with redis.Redis(decode_responses=True) as db:
        value = db.get(f'mucus:deezer:{key}')
        if value is not None:
            return value
    raise AuthException(key)


class Auth(httpx.Auth):
    def __init__(self, sid=None, arl=None):
        if sid is None:
            sid = discover('sid')
        if arl is None:
            arl = discover('arl')
        self.sid = sid
        self.arl = arl

    def auth_flow(self, request):
        request.cookies['sid'] = self.sid
        request.cookies['arl'] = self.arl
        yield request
