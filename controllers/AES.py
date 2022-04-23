import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from controllers.db import *



def encrypt(id, task):
    key = getKey(id)
    IV = os.urandom(16)
    c = AES.new(key, AES.MODE_CBC, IV)
    cipher = IV + c.encrypt(pad(bytes(task, 'utf-8'),AES.block_size))
    return cipher


def decrypt(id, result):
    key = getKey(id)
    IV = result[:AES.block_size]
    cipher = AES.new(key, AES.MODE_CBC, IV)
    pt = cipher.decrypt(result[AES.block_size:])
    pt = unpad(pt,16).decode('utf-8')
    return pt