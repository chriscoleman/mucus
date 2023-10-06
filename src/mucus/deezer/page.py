class Page:
    method = None
    params = None

    def __init__(self, client, **kwargs):
        self.data = client.post(self.method, json={**self.params, **kwargs})

    def __repr__(self):
        return f'<{self.__class__.__name__}>'


class Artist(Page):
    method = 'deezer.PageArtist'
    params = {'art_id': None, 'lang': 'en', 'tab': 0}

    def __iter__(self):
        def generator():
            for song in self.data['TOP']['data']:
                yield song
        return generator()


class Album(Page):
    method = 'deezer.PageAlbum'
    params = {'alb_id': None, 'lang': 'en', 'tab': 0, 'header': True}


class Track(Page):
    method = 'deezer.PageTrack'
    params = {'sng_id': None}


class Playlist(Page):
    method = 'deezer.PagePlaylist'
    params = {
        'nb': 2000,
        'start': 0,
        'playlist_id': None,
        'lang': 'en',
        'tab': 0,
        'tags': True,
        'header': True
    }

    def __iter__(self):
        for song in self.data['SONGS']['data']:
            yield song


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
        for track in self.data['TRACKS']:
            yield track


class SearchMusic(Page):
    method = 'search.music'
    params = {
        'query': None,
        'start': 0,
        'nb': 40,
        'filter': 'all',
        'output': 'TRACK'
    }

    def __iter__(self):
        for track in self.data:
            yield track
