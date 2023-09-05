import os

import click

import mucus.command
import mucus.commands


class Command(mucus.command.Command):
    def __call__(self, **kwargs):
        for f in os.listdir(mucus.commands.__path__[0]):
            if f.startswith('_'):
                continue
            if f.endswith('.py'):
                click.echo(f[:-3])
