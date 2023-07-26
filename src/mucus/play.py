import queue
import subprocess
import threading
import time

from mucus.exception import NoMedia, NoSource
from mucus.song import Song


class Player:
    def __init__(self, client):
        self.client = client
        self.queue = queue.Queue()
        self.events = {name: threading.Event() for name in ('pause', 'stop')}
        self.thread = None
        self.state = {}

    def play(self, song):
        data = self.client.stream(song)

        media = next(data)
        if media is None:
            raise NoMedia

        source = next(data)
        if source is None:
            raise NoSource

        song = Song(data=song)

        self.state.update({'song': song})

        with subprocess.Popen(['sox', '-', '-d', '-q', '-V0'], stdin=subprocess.PIPE) as p: # noqa
            for chunk in data:
                if self.events['stop'].is_set():
                    break
                while self.events['pause'].is_set():
                    time.sleep(0.1)
                p.stdin.write(chunk)

        self.state.update({'last_song': song, 'song': None})

    def loop(self):
        self.events['stop'].clear()
        self.state.update({'state': 'playing'})
        while not self.events['stop'].is_set():
            try:
                song = self.queue.get(timeout=1)
            except queue.Empty:
                continue
            if song is None:
                break
            self.play(song)
            self.queue.task_done()
        self.state.update({'state': 'stopped'})

    def start(self):
        self.thread = threading.Thread(target=self.loop, daemon=True)
        self.thread.start()
