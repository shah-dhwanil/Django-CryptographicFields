from django.conf import settings
from .exceptions import LengthError
from Crypto.Cipher import AES
def get_key(settings)->str:
    try:
        cipher_key=settings.ENCRYPTION_KEY
    except AttributeError:
        cipher_key=settings.SECRET_KEY
    finally:
        if len(cipher_key) < 50:
            raise LengthError(len(cipher_key))
        else:
            return cipher_key

def type_check(string)->bytearray:
    if isinstance(string,bytearray):
        return string
    elif isinstance(string,bytes):
        return bytearray(string)
    else:
        return bytearray(str(string),"UTF-8")

def to_hex(string)->hex:
    return bytearray(string).hex()

def from_hex(hexstring)->bytearray:
    return bytearray.fromhex(hexstring)

def encrypt(string)->hex:
    print('encrypt called')
    return to_hex(AES.new(type_check(get_key(settings)[:32]),AES.MODE_CFB,type_check(get_key(settings)[-16:])).encrypt(type_check(string)))
def decrypt(hexstring)->bytearray:
    print('decrypt called')
    return bytearray(AES.new(type_check(get_key(settings)[:32]),AES.MODE_CFB,type_check(get_key(settings)[-16:])).decrypt(type_check(from_hex(hexstring))))