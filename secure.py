import aesio
import adafruit_hashlib as hashlib
from binascii import hexlify
from binascii import unhexlify
from binascii import crc32
import random
import microcontroller

def get_data_hash(data: bytes):
    h = hashlib.sha256()
    h.update(data)
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
    
def calc_key_signature(key: bytes, salt: bytes):
    return encrypt(crc32(key + salt).to_bytes(4, 'big'), get_data_hash(key))
    
def encode_data(data: bytes, key: bytes):
    enc_data = encrypt(pad_data(data), key)
    key_signature = calc_key_signature(key, enc_data[-4:])
    return key_signature + enc_data
    
def decode_data(data: bytes, key: bytes):
    return unpad_data(decrypt(data[4:], key))

def encode_str(s: str, key: bytes):
    data = bytes(s, 'utf-8')
    return hexlify(encode_data(data, key)).decode('ascii')

def decode_str(s_hex: str, key: bytes):
    data = decode_data(unhexlify(s_hex), key)
    return data.decode('ascii')

def str_can_be_decoded(s_hex: str, key: bytes):
    stored_key_signature = unhexlify(s_hex[0:8])
    salt = unhexlify(s_hex[-8:])
    key_signature = calc_key_signature(key, salt)
    return stored_key_signature == key_signature

keys = [get_data_hash(microcontroller.cpu.uid)]

def decode_str_use_keys(s_hex: str):
    for k in keys:
        if str_can_be_decoded(s_hex, k):
            return decode_str(s_hex, k)
    raise Exception("Has no key to decode string")
