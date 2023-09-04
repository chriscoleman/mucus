import json

import redis


class History:
    def __init__(self):
        self.redis = redis.Redis(decode_responses=True)
        self.key = ':'.join((__name__, self.__class__.__name__))

    def __repr__(self):
        return f'<{self.__class__.__name__}>'

    def append(self, song):
        self.redis.lpush(self.key, json.dumps(song, separators=(',', ':')))
