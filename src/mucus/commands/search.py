import click

import mucus.command
import mucus.deezer.page
import mucus.history


class Command(mucus.command.Command):
    def __call__(self, client, command, player, **kwargs):
        query = command['line']
        search = mucus.deezer.page.Search(client=client, query=query, nb=10)
        choices = search.track['data'].copy()
        for i, track in enumerate(choices):
            click.echo(' '.join([
                click.style(f'{i:03}', fg='red'),
                click.style(track['ART_NAME'], fg='green'),
                click.style(track['SNG_TITLE'], fg='blue')
            ]))
        with mucus.history.History(__name__):
            try:
                i = input('# ')
            except EOFError:
                return
        if ':' in i:
            i = slice(*map(lambda x: x.isdigit() and int(x) or None, i.split(':')))
        else:
            try:
                i = int(i)
            except ValueError:
                return
            i = slice(i, i+1)
        for choice in choices[i]:
            player.queue.put(choice)
