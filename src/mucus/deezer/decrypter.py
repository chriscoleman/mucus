import hashlib

from Crypto.Cipher import Blowfish as bf


class Decrypter:
    secret = b'g4el58wc0zvf9na1'
    iv = bytes(range(8))

    def __init__(self, song_id):
        h = hashlib.md5(song_id.encode()).hexdigest().encode()
        self.key = bytes([h[i] ^ h[i+16] ^ self.secret[i] for i in range(16)])

    def decrypt(self, chunk):
        return bf.new(self.key, bf.MODE_CBC, self.iv).decrypt(chunk)
