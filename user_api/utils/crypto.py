#Dependencies
from os import getenv
from cryptography.fernet import Fernet

def Crypt(data):
    cipher_suite = Fernet(getenv('SECRETKEY'))
    cipher = cipher_suite.encrypt(str.encode(data))
    return cipher  #str(cipher, 'utf-8')

def Decrypt(cipher):
    cipher_suite = Fernet(getenv('SECRETKEY'))
    data = cipher_suite.decrypt(str.encode(cipher))  #str.encode(
    return str(data, 'utf-8') 