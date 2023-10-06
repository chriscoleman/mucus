import click

import mucus.command
import mucus.deezer.page
import mucus.history


class Command(mucus.command.Command):
    def __call__(self, client, command, player, **kwargs):
        params = {'query': command['line'], 'nb': 40, 'start': 0}

        def generate():
            search = mucus.deezer.page.Search(client=client, **params)
            for k in search.data['ORDER']:
                results = search.data[k]
                if results:
                    try:
                        results = results['data']
                    except (KeyError, TypeError):
                        pass
                    for result in results:
                        t = result.get('__TYPE__')
                        if t == 'song':
                            yield result
                        elif t == 'artist':
                            artist = mucus.deezer.page.Artist(
                                client=client,
                                art_id=result['ART_ID']
                            )
                            for song in artist:
                                yield song
                        elif t == 'playlist':
                            playlist = mucus.deezer.page.Playlist(
                                client=client,
                                playlist_id=result['PLAYLIST_ID']
                            )
                            for song in playlist:
                                yield song

        def uniq(songs):
            seen = set()
            for song in songs:
                if song['SNG_ID'] not in seen:
                    yield song
                    seen.add(song['SNG_ID'])

        songs = uniq(generate())

        while True:
            choices = []
            while len(choices) < 20:
                try:
                    choices.append(next(songs))
                except StopIteration:
                    break
            if len(choices) == 0:
                break
            for i, track in enumerate(choices):
                click.echo(' '.join([
                    click.style(f'{i:02}', fg='red'),
                    click.style(track['ART_NAME'], fg='green'),
                    click.style(track['SNG_TITLE'], fg='blue')
                ]))
            with mucus.history.History(__name__):
                try:
                    i = input('# ')
                except EOFError:
                    return
            if i == '.':
                continue
            elif ':' in i:
                i = slice(*map(lambda x: x.isdigit() and int(x) or None, i.split(':'))) # noqa
            else:
                try:
                    i = int(i)
                except ValueError:
                    return
                i = slice(i, i+1)
            for choice in choices[i]:
                player.queue.put(choice)
            break
