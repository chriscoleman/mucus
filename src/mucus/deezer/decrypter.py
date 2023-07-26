import hashlib

import Crypto.Cipher.Blowfish


class Decrypter:
    def __init__(self, song_id, secret=b'g4el58wc0zvf9na1', iv=bytes(range(8))): # noqa
        h = hashlib.md5(song_id.encode()).hexdigest().encode()
        self.key = bytes([h[i] ^ h[i+16] ^ secret[i] for i in range(16)])
        self.iv = iv

    def decrypt(self, chunk):
        return Crypto.Cipher.Blowfish.new(self.key, Crypto.Cipher.Blowfish.MODE_CBC, self.iv).decrypt(chunk) # noqa
