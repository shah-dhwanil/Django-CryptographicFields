from django.conf import settings
from .utils import LengthError
from Crypto.Cipher import AES
def get_key(settings)->str:
    """
    Gets the encryption for encrypting & decrypting data.
    Gets value from ENCRYPTION_KEY & if not defined then from SECRET_KEY
    Checks the len of the key id less than 50 then raise LengthError
    """
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
    """
    Checks weather the inputed data is in correct format which is required for encryption & decryption.
    Which is in this case is bytearray
    """
    if isinstance(string,bytearray):
        return string
    elif isinstance(string,bytes):
        return bytearray(string)
    else:
        return bytearray(str(string),"UTF-8")

def to_hex(string)->hex:
    # converts bytes to hex
    return bytearray(string).hex()

def from_hex(hexstring)->bytearray:
    #converts hex to bytearray
    return bytearray.fromhex(hexstring)

def encrypt(string)->hex:
    # encrypts the data & returns it
    return to_hex(AES.new(type_check(get_key(settings)[:32]),AES.MODE_CFB,type_check(get_key(settings)[-16:])).encrypt(type_check(string)))
def decrypt(hexstring)->bytearray:
    # decrypts the data & returns it
    return bytearray(AES.new(type_check(get_key(settings)[:32]),AES.MODE_CFB,type_check(get_key(settings)[-16:])).decrypt(type_check(from_hex(hexstring))))