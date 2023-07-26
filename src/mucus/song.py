class Song:
    def __init__(self, data):
        self.data = data

    @property
    def artist(self):
        return self.data['ART_NAME']

    @property
    def title(self):
        return self.data['SNG_TITLE']

    @property
    def track(self):
        return self.data['TRACK_NUMBER']

    @property
    def album(self):
        return self.data['ALB_TITLE']

    def __repr__(self):
        return f'<Song title={self.title!r} artist={self.artist!r}>'

    def __str__(self):
        return f'{self.artist} - {self.title}'
