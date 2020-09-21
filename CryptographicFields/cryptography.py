from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad
from django.conf import settings
key=getattr(settings, 'SECRET_KEY', None)[:32].encode()
iv=getattr(settings, 'SECRET_KEY', None)[-16:].encode()
def Encrypter(*args):
  cipher=AES.new(key,AES.MODE_CBC,iv)
  for i in args:
    if type(i)==bytes:
      data=i
    else:
      data=str(i).encode()
    cipher_text=cipher.encrypt(pad(data,AES.block_size))
    break
  return cipher_text

def Decrypter(*args):
  cipher=AES.new(key,AES.MODE_CBC,iv)
  for i in args:
    if type(i)==bytes:
      data=i
    else:
      data=str(i).encode()
    cipher_text=unpad(cipher.decrypt(data),AES.block_size)
    break
  return cipher_text
  
  
