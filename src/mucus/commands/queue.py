import queue

import click

import mucus.command


class Command(mucus.command.Command):
    def __call__(self, command, player, **kwargs):
        items = []
        while True:
            try:
                items.append(player.queue.get(block=False))
            except queue.Empty:
                break
        if '!' in command['line']:
            return
        for i, item in enumerate(items):
            click.echo(' '.join([
                click.style(f'{i:03}', fg='red'),
                click.style(item['ART_NAME'], fg='green'),
                click.style(item['SNG_TITLE'], fg='blue')
            ]))
            player.queue.put(item)
