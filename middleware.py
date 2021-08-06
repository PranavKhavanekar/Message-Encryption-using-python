import os
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes


class crypto:
    def __init__(self, path) -> None:
        path = os.path.join('Keys', path)
        self.privatePath = os.path.join(path, 'private.rem')
        self.publicPath = os.path.join(path, 'public.rem')

        if os.path(path):
            self.public = RSA.import_key(open(self.publicPath).read())
            if os.path(self.privatePath): self.key = RSA.import_key(open(self.privatePath).read())
        
        else:
            os.mkdir(path)
            self.key = RSA.generate(2048)
            self.public = self.key.public_key()
            with open(self.privatePath) as F: F.write(self.key.export_key())
            with open(self.publicPath) as F: F.write(self.public.export_key())


    def encrypt(
        self,
        text: str
    ):
        cipher = PKCS1_OAEP.new(self.public)
        text = text.encode('utf-8')
        return cipher.encrypt(text)


    def decrypt(self, key, text):
        if not self.key:
            raise('No Private Key to decrypt')
        cipher = PKCS1_OAEP.new(self.key)
        return cipher.decrypt(text).decode('utf-8')