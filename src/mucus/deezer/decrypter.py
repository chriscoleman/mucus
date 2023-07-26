import hashlib

from Crypto.Cipher import Blowfish


class Decrypter:
    def __init__(self, song_id, secret=b'g4el58wc0zvf9na1', iv=bytes(range(8))): # noqa
        h = hashlib.md5(song_id.encode()).hexdigest().encode()
        self.key = bytes([h[i] ^ h[i+16] ^ secret[i] for i in range(16)])
        self.iv = iv

    def decrypt(self, chunk):
        return Blowfish.new(self.key, Blowfish.MODE_CBC, self.iv).decrypt(chunk)
