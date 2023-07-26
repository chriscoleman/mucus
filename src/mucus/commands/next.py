import mucus.command


class Command(mucus.command.Command):
    def __call__(self, player, **kwargs):
        player.events['stop'].set()
        player.thread.join()
        player.start()
