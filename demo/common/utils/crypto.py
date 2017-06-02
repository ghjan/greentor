#coding:utf-8

from M2Crypto.EVP import Cipher
from M2Crypto import m2
import base64, zlib
from common.settings import CRYPTO_KEY, CRYPTO_IV

def encrypto(s):
    ''' 压缩加密字符串 '''
    if isinstance(s, unicode):
        s = s.encode('utf8')
    s = zlib.compress(s)
    cipher = Cipher(alg='des_cbc', key=CRYPTO_KEY, iv=CRYPTO_IV, op=1)
    cipher.set_padding(padding=m2.no_padding)
    out = cipher.update(s)
    out += cipher.final()
    del cipher
    return base64.encodestring(out)


def decrypto(s):
    ''' des_cbc对称解密 '''
    #buf = base64.decodestring(s.decode('utf8'))
    buf = base64.decodestring(s)
    cipher = Cipher(alg='des_cbc', key=CRYPTO_KEY, iv=CRYPTO_IV, op=0)
    cipher.set_padding(padding=m2.no_padding)
    out = cipher.update(buf)
    out += cipher.final()
    del cipher
    return zlib.decompress(out)


def simple_encrypto(s):
    ''' 加密字符串 '''
    s = s.encode('utf8')
    cipher = Cipher(alg='des_cbc', key=CRYPTO_KEY, iv=CRYPTO_IV, op=1)
    cipher.set_padding(padding=m2.no_padding)
    out = cipher.update(s)
    out += cipher.final()
    del cipher
    return base64.encodestring(out)

def simple_decrypto(s):
    ''' des_cbc对称解密 '''
    buf = base64.decodestring(s.decode('utf8'))
    cipher = Cipher(alg='des_cbc', key=CRYPTO_KEY, iv=CRYPTO_IV, op=0)
    cipher.set_padding(padding=m2.no_padding)
    out = cipher.update(buf)
    out += cipher.final()
    del cipher
    return out
