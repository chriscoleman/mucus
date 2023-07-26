import rich

import mucus.command


class Command(mucus.command.Command):
    def __call__(self, player, **kwargs):
        def default(obj):
            return str(obj)
        rich.print_json(data=player.state, default=default)
