import re

from mucus.exception import NoSuchCommand
from mucus.lazy import import_module as lazy_import


class Command:
    pass


class Loader:
    def __init__(self, line=None, name=None, aliases=None):
        if aliases is None:
            aliases = {}
        if line is not None:
            if line in aliases:
                name = aliases[line]
            else:
                match = re.match(r'^([A-Za-z0-9_-]+)(.*)', line)
                if match is None:
                    raise NoSuchCommand
                name = match.group(1).replace('-', '_')
        if name is None:
            raise NoSuchCommand
        try:
            name = aliases[name]
        except KeyError:
            pass
        try:
            self.mod = lazy_import('.' + name, 'mucus.commands')
        except ModuleNotFoundError as e:
            raise NoSuchCommand(e)
        self.cmd = self.mod.Command()
        self.name = name


class Runner:
    def __init__(self, loader, context):
        self.loader = loader
        self.context = context

    def __call__(self):
        return self.loader.cmd(**self.context)
