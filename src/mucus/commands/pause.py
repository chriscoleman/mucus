import mucus.command


class Command(mucus.command.Command):
    def __call__(self, player, **kwargs):
        if player.events.play.is_set():
            player.events.play.clear()
        else:
            player.events.play.set()
