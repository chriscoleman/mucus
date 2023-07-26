import click

import mucus.command


class Command(mucus.command.Command):
    def __call__(self, **kwargs):
        click.clear()
