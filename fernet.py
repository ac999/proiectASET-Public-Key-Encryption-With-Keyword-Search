import base64
import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from utils import int_to_bytes

def generateSalt():
    return os.urandom(16)

def encrypt(message, key, salt = b""):
    message = message.encode('utf-8')
    key = int_to_bytes(key)
    kdf = PBKDF2HMAC(
    hashes.SHA256(), 32, salt, 100000
    )
    key = base64.urlsafe_b64encode(kdf.derive(key))
    f = Fernet(key)
    return f.encrypt(message)

def decrypt(crypto, key, salt):
    key = int_to_bytes(key)
    kdf = PBKDF2HMAC(
    hashes.SHA256(), 32, salt, 100000
    )
    key = base64.urlsafe_b64encode(kdf.derive(key))
    f = Fernet(key)
    return f.decrypt(crypto)
