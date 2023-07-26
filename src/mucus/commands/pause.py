import mucus.command


class Command(mucus.command.Command):
    def __call__(self, player, **kwargs):
        pause = player.events['pause']
        if pause.is_set():
            pause.clear()
        else:
            pause.set()
