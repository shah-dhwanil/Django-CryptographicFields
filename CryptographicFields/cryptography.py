from django.conf import settings
from Crypto.Cipher import AES


class LengthError(Exception):
    def __init__(self, length) -> None:
        super().__init__(
            f"Length of Encryption Key is '{length}' which is less than '50'")


def get_key(settings) -> str:
    """
    Gets the encryption for encrypting & decrypting data.

    Gets value from ENCRYPTION_KEY & if not defined then from SECRET_KEY
    Checks the len of the key id less than 50 then raise LengthError

    :raises LengthError: It raises when the len of Encryption is less than 50 chars
    :return: Key for cryptography
    :rtype: str

    """
    try:
        cipher_key = getattr(settings,'CRYPTOGRAPHY_KEY')
    except AttributeError:
        cipher_key = getattr(settings,'SECRET_KEY')
    finally:
        if len(cipher_key) < 50:
            raise LengthError(len(cipher_key))
        else:
            return cipher_key


def type_check(string) -> bytearray:
    """
    Checks weather the inputed data is in correct format which is required for encryption & decryption.

    Checks weather the inputed data is in correct format which is required for encryption & decryption.
    Which is in this case is bytearray

    :param string: Data from User
    :type string: Any
    :return: bytes
    :rtype: bytearray
    """
    if isinstance(string, bytearray):
        return string
    elif isinstance(string, bytes):
        return bytearray(string)
    else:
        return bytearray(str(string), "UTF-8")


def to_hex(string) -> hex:
    # converts bytes to hex
    """
    Converts bytes to hex

    Converts the bytes received after encryption to hex for storing it in database

    :param string: encrypted bytes
    :type string: bytes
    :return: hexify the bytes
    :rtype: hex
    """
    return bytearray(string).hex()


def from_hex(hexstring) -> bytearray:
    # converts hex to bytearray
    """
    converts hex to bytearray

    Converts the hex string received from databse to bytes for decryption

    :param hexstring: hex string recieved from database
    :type hexstring: hex
    :return: bytes from hex string
    :rtype: bytearray
    """
    return bytearray.fromhex(hexstring)


def encrypt(string) -> hex:
    """
    Encrypts the data 

    Encrypts the data recieved from user using AES-256 CFB 

    :param string: Data from User
    :type string: Any
    :return: the hex of the encrypted string
    :rtype: hex
    """
    # encrypts the data & returns it
    return to_hex(AES.new(type_check(get_key(settings)[:32]), AES.MODE_CFB, type_check(get_key(settings)[-16:])).encrypt(type_check(string)))


def decrypt(hexstring) -> bytearray:
    # decrypts the data & returns it
    """
    Decrypts the data

    Decrypts the data recieved from database using AES-256 CFB 

    :param hexstring: hex string recieved from database
    :type hexstring: hex
    :return: bytes of decrypted string
    :rtype: bytearray
    """
    return bytearray(AES.new(type_check(get_key(settings)[:32]), AES.MODE_CFB, type_check(get_key(settings)[-16:])).decrypt(type_check(from_hex(hexstring)))).decode()
