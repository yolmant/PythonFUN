import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class KeyCreator:

    def __init__(self, pkey='pivet.key'):
    
        pivet_pass = open(pkey,'rb')
        pivet = pivet_pass.read()
        pivet_pass.close()

        salt = b"\x9c\xd3\xd4\x9f\x88\xc4x1d'DL\xe26\xf2K\xf4;\xdf\xe8\xc3l\\\x91"

        kdf = PBKDF2HMAC (
            algorithm = hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
            )

        self.key = base64.urlsafe_b64encode(kdf.derive(pivet))

    def get_key(self):

        return self.key

class DataCrypt:

    def __init__(self):

        kc = KeyCreator()
        self.key = kc.get_key()

    def Encryptado(self,data):

        data_enc = data.encode()
        fer = Fernet(self.key)
        nodata = fer.encrypt(data_enc)

        svdata = open('ddext.dat','wb')
        svdata.write(nodata)
        svdata.close()

    def DesEncrypt(self,path):

        file = open(path,'rb')
        data_dec = file.read()
        file.close()

        fer = Fernet(self.key)
        data = fer.decrypt(data_dec)

        ori_data = data.decode()

        return ori_data
        
        
