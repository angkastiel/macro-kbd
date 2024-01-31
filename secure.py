import aesio
import adafruit_hashlib as hashlib
from binascii import hexlify
from binascii import unhexlify


def get_pincode_hash(s: bytes):
    h = hashlib.sha256()
    h.update(s)
    return h.digest()
    

def encrypt(data: bytes, key: bytes):
    data_encrypted = bytearray(len(data))
    cipher = aesio.AES(key, aesio.MODE_CTR)
    cipher.encrypt_into(data, data_encrypted)
    return data_encrypted
    

def decrypt(data_encrypted: bytes, key: bytes):
    data_decrypted = bytearray(len(data_encrypted))
    cipher = aesio.AES(key, aesio.MODE_CTR)
    cipher.decrypt_into(data_encrypted, data_decrypted)
    return data_decrypted


def encrypt_str(s: str, key: bytes):
    data = bytes(s, "UTF-8")
    data_encrypted = encrypt(data, key)
    return hexlify(data_encrypted).decode("UTF-8")


def decrypt_str(s_hex: str, key: bytes):
    data_encrypted = unhexlify(s_hex)
    data = decrypt(data_encrypted, key)
    return data.decode("UTF-8")