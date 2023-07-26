import readline

import redis


class History:
    def __init__(self, namespace, n=1000, sep=':'):
        self.namespace = namespace
        self.n = n
        self.sep = sep

    def __enter__(self):
        try:
            with redis.Redis(decode_responses=True) as db:
                self.backup = [readline.get_history_item(i+1)
                               for i in range(readline.get_current_history_length())] # noqa
                readline.clear_history()
                for item in db.lrange(self.key, -self.n, -1):
                    readline.add_history(item)
                db.expire(self.key, 86400)
        except redis.exceptions.RedisError:
            pass

    def __exit__(self, *args):
        try:
            with redis.Redis(decode_responses=True) as db:
                for i in range(readline.get_current_history_length()):
                    db.rpush(self.key, readline.get_history_item(i+1))
                db.expire(self.key, 86400)
                readline.clear_history()
                for item in self.backup:
                    readline.add_history(item)
        except redis.exceptions.RedisError:
            pass

    @property
    def key(self):
        return self.sep.join((__name__, self.namespace))
