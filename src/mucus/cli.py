#!/usr/bin/env python3

import click

import mucus.command
import mucus.config
import mucus.deezer.client
import mucus.deezer.exception
import mucus.exception
import mucus.history
import mucus.play


@click.command()
@click.option('--alias', '-a', 'aliases', type=(str, str), multiple=True)
def command(aliases):
    aliases = dict(aliases)
    config = mucus.config.Config()

    with mucus.history.History(__name__) as history:
        try:
            client = mucus.deezer.client.Client()
        except mucus.deezer.exception.AuthException as e:
            raise click.ClickException(e)
        player = mucus.play.Player(client)
        player.start()

        def inputs():
            while True:
                try:
                    yield input('> ')
                except EOFError:
                    break

        for line in inputs():
            if line.strip() == '':
                continue

            try:
                loader = mucus.command.Loader(line=line, aliases=aliases)
            except mucus.command.NoSuchCommand:
                loader = mucus.command.Loader(name='search')

            runner = mucus.command.Runner(
                loader,
                context={
                    'client': client,
                    'command': {
                        'line': line,
                        'name': loader.name
                    },
                    'config': config,
                    'history': history,
                    'player': player
                }
            )

            try:
                runner()
            except mucus.exception.Exit:
                break
            except Exception as e:
                raise click.ClickException(e)


def main():
    return command(default_map=mucus.config.Config().flatten())
