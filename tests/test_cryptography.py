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

if __name__ == '__main__':
    unittest.main()
