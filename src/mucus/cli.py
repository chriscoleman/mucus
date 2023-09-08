#!/usr/bin/env python3

import click

import mucus.command
import mucus.config
import mucus.deezer.client
import mucus.deezer.exception
import mucus.exception
import mucus.history
import mucus.play.player


@click.command(help='music cli thing', epilog='\b\n' + click.style('''
 ███▄ ▄███▓ █    ██  ▄████▄   █    ██   ██████
▓██▒▀█▀ ██▒ ██  ▓██▒▒██▀ ▀█   ██  ▓██▒▒██    ▒
▓██    ▓██░▓██  ▒██░▒▓█    ▄ ▓██  ▒██░░ ▓██▄
▒██    ▒██ ▓▓█  ░██░▒▓▓▄ ▄██▒▓▓█  ░██░  ▒   ██▒
▒██▒   ░██▒▒▒█████▓ ▒ ▓███▀ ░▒▒█████▓ ▒██████▒▒
░ ▒░   ░  ░░▒▓▒ ▒ ▒ ░ ░▒ ▒  ░░▒▓▒ ▒ ▒ ▒ ▒▓▒ ▒ ░
░  ░      ░░░▒░ ░ ░   ░  ▒   ░░▒░ ░ ░ ░ ░▒  ░ ░
░      ░    ░░░ ░ ░ ░         ░░░ ░ ░ ░  ░  ░
       ░      ░     ░ ░         ░           ░
                    ░
'''.strip(), fg='green'))
@click.option('--alias', '-a', 'aliases', type=(str, str),
              metavar='<name> <command>', multiple=True)
@click.option('--default', '-d', default='search', show_default=True,
              metavar='<command>', help='default command')
def command(aliases, default):

    aliases = dict(aliases)
    config = mucus.config.Config()

    with mucus.history.History(__name__) as history:
        try:
            client = mucus.deezer.client.Client()
        except mucus.deezer.exception.AuthException as e:
            raise click.ClickException(e)
        player = mucus.play.player.Player(client)
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
                try:
                    loader = mucus.command.Loader(name=default)
                except mucus.command.NoSuchCommand as e:
                    raise click.ClickException(e)

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
