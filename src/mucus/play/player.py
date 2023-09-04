import collections
import queue
import subprocess
import threading

from mucus.exception import NoMedia, NoSource
from mucus.song import Song

events = ('play', 'stop')


class Events(collections.namedtuple('Events', events)):
    def __new__(cls):
        return super().__new__(cls, *(threading.Event() for _ in events))


class Player:
    def __init__(self, client):
        self.client = client
        self.queue = queue.Queue()
        self.events = Events()
        self.thread = None
        self.song = None
        self.history = []

    def loop(self):
        self.events.stop.clear()
        while not self.events.stop.is_set():
            try:
                song = self.queue.get(timeout=1)
            except queue.Empty:
                continue
            if song is None:
                break
            self.play(song)
            self.queue.task_done()

    def play(self, song):
        self.history.append(song)

        data = self.client.stream(song)
        media = next(data)
        if media is None:
            raise NoMedia
        source = next(data)
        if source is None:
            raise NoSource

        self.events.play.set()

        with subprocess.Popen(['sox', '-', '-d', '-q', '-V0'], stdin=subprocess.PIPE) as p: # noqa
            for chunk in data:
                if self.events.stop.is_set():
                    break
                self.events.play.wait()
                p.stdin.write(chunk)

        self.events.play.clear()

    def start(self):
        self.thread = threading.Thread(target=self.loop, daemon=True)
        self.thread.start()

    @property
    def state(self):
        try:
            song = self.history[-1]
        except IndexError:
            song = None
        return {
            'playing': self.events.play.is_set(),
            'song': Song(song)
        }
