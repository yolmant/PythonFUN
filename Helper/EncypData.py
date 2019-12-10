
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

import base64
import os
import random
import string

#Class that creates the key
class KeyCreator:

    #Take your password and encode and created encrypted key
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

    #Get key or just get the object (function not nescessary)
    def get_key(self):

        return self.key

#Class to encrypt data
class DataCrypt:

    #Call keycreator and get key
    def __init__(self):

        kc = KeyCreator()
        self.key = kc.get_key()

    #Encrypt data and dump it to path
    def Encryptado(self,data,path='ddext.dat'):

        data_enc = data.encode()
        fer = Fernet(self.key)
        nodata = fer.encrypt(data_enc)

        svdata = open(path,'wb')
        svdata.write(nodata)
        svdata.close()

    #Decrypt data from path
    def DesEncrypt(self,path='ddext.dat'):

        file = open(path,'rb')
        data_dec = file.read()
        file.close()

        fer = Fernet(self.key)
        data = fer.decrypt(data_dec)

        ori_data = data.decode()

        return ori_data
    
#Class to generate  random passwords      
class PassGenerator():

    #Define a list to store all passwords
    def __init__(self,queu):

        self.passwords=[]
        for repit in range(queu):
            code= self.pass_generator()
            while not self.hasNumbers(code) or not self.hasSpecials(code) or not self.capLetter(code) or not self.lowLetter(code):
                code=self.pass_generator()
            self.passwords.append(code)

    #Verify the password contains at least a number    
    def hasNumbers(self,code):
            return any(char.isdigit() for char in code)

    #Verify the password contains at least a special character
    def hasSpecials(self,code):
            symbols = ['!','@','(',')','#','$','^','%','&','*']
            return any(char in code for char in symbols)

    #verify the password contains at least a capital letter
    def capLetter(self,code):
            return any(char.isupper() for char in code)

    #Verify the password contains at least a lower letter
    def lowLetter(self,code):
            return any(char.islower() for char in code)

    #Generate a set of strings randomly 
    def pass_generator (self,size= 12, char=string.ascii_uppercase + string.digits + string.ascii_lowercase + '!@()#$^%&*') :
            code =''.join(random.choice(char) for i in range(size))
            return code

        
            
    
