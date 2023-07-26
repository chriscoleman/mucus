import httpx

from mucus.deezer.decrypter import Decrypter


class Stream:
    def __init__(self, song, license_token):
        try:
            song = song.data
        except AttributeError:
            pass
        self.song = song
        self.license_token = license_token

    def stream(self, format='FLAC'):
        media = httpx.post('https://media.deezer.com/v1/get_url', json={
            'license_token': self.license_token,
            'media': [{'type': 'FULL',
                       'formats': [{'cipher': 'BF_CBC_STRIPE',
                                    'format': format}]}],
            'track_tokens': [self.song['TRACK_TOKEN']]
        }).json()['data'][0]['media'][0]
        yield media
        decrypter = Decrypter(self.song['SNG_ID'])
        for source in media['sources']:
            with httpx.stream('GET', source['url']) as r:
                yield source
                for i, chunk in enumerate(r.iter_bytes(chunk_size=2048)):
                    if i % 3 == 0 and len(chunk) == 2048:
                        chunk = decrypter.decrypt(chunk)
                    yield chunk
                return
