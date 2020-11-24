import unittest 
from django.conf import settings
from CryptographicFields.cryptography import *

class Cryptography(unittest.TestCase):
    settings.configure(CRYPTOGRAPHY_KEY="",SECRET_KEY="")
    def test_get_key_prefrence(self):
        setattr(settings,'CRYPTOGRAPHY_KEY',"XmeExmMq5tx1u9fbgLTKr26toW58OeC2sNvy1BEazSDBobWj0areehwvRUif")
        setattr(settings,"SECRET_KEY","98sgfit47#^&%dkfgfylaffsfvsk)w9bysdfv;[fgyeva47054^*7fuzgf7*^E7bjfae7be7")
        self.assertEqual(get_key(settings),"XmeExmMq5tx1u9fbgLTKr26toW58OeC2sNvy1BEazSDBobWj0areehwvRUif")
    def test_get_key_exception(self):    
        with self.assertRaises(LengthError):
            setattr(settings,'CRYPTOGRAPHY_KEY',"XmeExmMq5tx1u9fbgLTKr26")
            self.assertEqual(get_key(settings),"XmeExmMq5tx1u9fbgLTKr26")
            setattr(settings,"SECRET_KEY","98sgfit47#^&%dkfgfylaffsfvsk)")
            delattr(settings,'CRYPTOGRAPHY_KEY')
            self.assertEqual(get_key(settings),"98sgfit47#^&%dkfgfylaffsfvsk)")
    def test_get_key_secret(self):
        setattr(settings,"SECRET_KEY","98sgfit47#^&%dkfgfylaffsfvsk)w9bysdfv;[fgyeva47054^*7fuzgf7*^E7bjfae7be7")
        delattr(settings,'CRYPTOGRAPHY_KEY')
        self.assertEqual(get_key(settings),"98sgfit47#^&%dkfgfylaffsfvsk)w9bysdfv;[fgyeva47054^*7fuzgf7*^E7bjfae7be7")
    def test_type_check(self):
        from datetime import datetime
        from uuid import uuid5,NAMESPACE_URL
        self.assertEqual(type_check("CryptographicFields"),bytearray("CryptographicFields","UTF-8"))
        self.assertEqual(type_check(b"CryptographicFields"),bytearray(b"CryptographicFields"))
        self.assertEqual(type_check(149),bytearray(str(149),"UTF-8"))
        self.assertEqual(type_check(149.250),bytearray(str(149.250),"UTF-8"))
        self.assertEqual(type_check(datetime.now()),bytearray(str(datetime.now()),"UTF-8"))
        self.assertEqual(type_check(uuid5(NAMESPACE_URL,"www.google.com")),bytearray(str('c74a196f-f19d-5ea9-bffd-a2742432fc9c'),"UTF-8"))

if __name__ == '__main__':
    unittest.main()
