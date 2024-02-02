import aesio
import adafruit_hashlib as hashlib
from binascii import hexlify
from binascii import unhexlify
import random

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

def random_byte():
    return random.randint(0, 255)
    
def pad_data(data: bytes):
    l = len(data)
    tail = (l + 1) % 16
    rest = 16 - tail if tail else 0 
    x = rest + 1
    rndata = bytearray(x)
    for i in range(x):
        rndata[i] = random_byte()
    rndata[-1] = (rndata[-1] & 0xf0) | (rest & 0x0f)
    return data + rndata
    
def unpad_data(data: bytes):
    l = data[-1] & 0x0f
    return data[0:-(l+1)]
    
def encode_data(data: bytes, key: bytes):
    return encrypt(pad_data(data), key)
    
def decode_data(data: bytes, key: bytes):
    return unpad_data(decrypt(data, key))

def encode_str(s: str, key: bytes):
    data = bytes(s, "UTF-8")
    return hexlify(encode_data(data, key)).decode("UTF-8")

def decode_str(s_hex: str, key: bytes):
    data = decode_data(unhexlify(s_hex), key)
    return data.decode("UTF-8")