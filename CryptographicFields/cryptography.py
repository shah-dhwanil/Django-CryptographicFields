from Crypto.Cipher import AES
from django.conf import settings
key=getattr(settings, 'SECRET_KEY', None)[:32].encode()
iv=getattr(settings, 'SECRET_KEY', None)[-16:].encode()
def encrypter(*args):
  cipher=AES.new(key,AES.MODE_CFB,iv)
  for i in args:
    if type(i)==bytes:
      data=i
    else:
      data=str(i).encode()
    cipher_text=cipher.encrypt(data)
    break
  return cipher_text

def decrypter(*args):
  cipher=AES.new(key,AES.MODE_CFB,iv)
  for i in args:
    if type(i)==bytes:
      data=i
    else:
      data=str(i).encode()
    cipher_text=cipher.decrypt(data)
    break
  return cipher_text
  
  
