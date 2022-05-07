import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from controllers.db import *
from base64 import b64decode, b64encode
 

def encrypt(id, task):
    k = getKey(id)
    base64_bytes = k.encode("ascii")
    key = b64decode(base64_bytes)
    IV = os.urandom(16)
    c = AES.new(key, AES.MODE_CBC, IV)
    ct = IV + c.encrypt(pad(bytes(task, 'utf-8'),AES.block_size))
    base64_bytes = b64encode(ct)
    cipher = base64_bytes.decode("ascii")
    return cipher


def decrypt(id, eresult):
    k = getKey(id)
    base64_bytes = k.encode("ascii")
    key = b64decode(base64_bytes)
    #base64_bytes = eresult.encode("ascii")
    result = b64decode(eresult)
    IV = result[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, IV)
    pt = cipher.decrypt(result[AES.block_size:])
    pt = unpad(pt,16).decode('utf-8')
    return pt