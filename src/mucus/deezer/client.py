import random

import httpx

from mucus.deezer.stream import Stream
from mucus.deezer.auth import Auth
from mucus.deezer.exception import ApiException, AuthException


class Client(httpx.Client):
    def __init__(self, sid=None, arl=None, user_data=None):
        super().__init__(base_url='https://www.deezer.com/ajax/')

        auth = Auth(sid, arl)
        self.cookies['sid'] = auth.sid
        self.cookies['arl'] = auth.arl
        self.user = {}
        self.user.update(self.post('deezer.getUserData'))
        if self.user['USER']['USER_ID'] <= 0:
            raise AuthException

    @property
    def license_token(self):
        try:
            return self.user['USER']['OPTIONS']['license_token']
        except KeyError:
            return None

    def request(self, method, url, **kwargs):
        kwargs['params'] = {
            'method': url,
            'input': 3,
            'api_version': '1.0',
            'api_token': self.user.get('checkForm', ''),
            'cid': random.randrange(0, 1000000000)
        }
        r = super().request(method, 'gw-light.php', **kwargs)
        r.raise_for_status()
        r = r.json()
        if r['error']:
            raise ApiException(r['error'])
        return r['results']

    def stream(self, song, format='FLAC'):
        return Stream(song, self.license_token).stream(format)
