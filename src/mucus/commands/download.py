import os

import mucus.command


class Command(mucus.command.Command):
    def __call__(self, client, config, player, **kwargs):
        song = None
        for k in ('song', 'last_song'):
            try:
                song = player.state[k]
            except KeyError:
                continue
        if song is None:
            return
        data = client.stream(song)
        media = next(data)
        if media is None:
            raise Exception
        source = next(data)
        if source is None:
            raise Exception
        root = config['download']['directory'].get()
        for path in (os.path.join(root, song.artist),
                     os.path.join(root, song.artist, song.album)):
            os.mkdir(path)
        dn = os.path.join(config['download']['directory'].get(),
                          song.artist,
                          song.album)
        fn = f'{song.track} {song.title}.flac'
        with open(os.path.join(dn, fn), 'wb') as f:
            for chunk in data:
                f.write(chunk)
