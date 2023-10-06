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
        formats = ['FLAC', 'MP3_320', 'MP3_128', 'MP3_64', 'MP3_MISC']
        if format is not None:
            formats = [format, *[f for f in formats if f != format]]
        formats = [{'cipher': 'BF_CBC_STRIPE', 'format': format}
                   for format in formats]
        r = httpx.post('https://media.deezer.com/v1/get_url', json={
            'license_token': self.license_token,
            'media': [{'type': 'FULL', 'formats': formats}],
            'track_tokens': [self.song['TRACK_TOKEN']]
        }).json()
        try:
            errors = r['data'][0]['errors']
        except KeyError:
            pass
        else:
            print(errors[0])
            yield None
            return
        media = r['data'][0]['media'][0]
        yield media
        source = media['sources'][0]
        yield source
        decrypter = Decrypter(self.song['SNG_ID'])
        url = source['url']
        pos = 0
        while True:
            try:
                with httpx.stream('GET', url, headers={'range': f'bytes={pos}-'}, timeout=1.0) as r: # noqa
                    for chunk in r.iter_bytes(chunk_size=2048):
                        if (pos // 2048) % 3 == 0 and len(chunk) == 2048:
                            chunk = decrypter.decrypt(chunk)
                        yield chunk
                        pos += len(chunk)
                    return
            except httpx.HTTPError:
                continue
