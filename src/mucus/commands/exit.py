import mucus.command
import mucus.exception


class Command(mucus.command.Command):
    def __call__(self, **kwargs):
        raise mucus.exception.Exit
