class Page:
    method = None
    params = None

    def __init__(self, client, **kwargs):
        self._data = client.post(self.method, json={**self.params, **kwargs})

    def __repr__(self):
        return f'<{self.__class__.__name__}>'

    def __getattr__(self, name):
        try:
            return self._data[name.upper()]
        except KeyError:
            raise AttributeError(name)


class Artist(Page):
    method = 'deezer.PageArtist'
    params = {'art_id': None, 'lang': 'en', 'tab': 0}


class Album(Page):
    method = 'deezer.PageAlbum'
    params = {'alb_id': None, 'lang': 'en', 'tab': 0, 'header': True}


class Search(Page):
    method = 'deezer.PageSearch'
    params = {
        'query': None,
        'start': 0,
        'nb': 10,
        'suggest': True,
        'artist_suggest': True,
        'top_tracks': True
    }

    def __iter__(self):
        def generator():
            for track in self.data['TRACKS']:
                yield track
        return generator()
