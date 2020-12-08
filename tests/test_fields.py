from django.conf import settings
from CryptographicFields.fields import *
from django.test import TestCase
from .models import *
from django.core import exceptions


class Fields(TestCase):
    setattr(settings, 'CRYPTOGRAPHIC_KEY',
            "XmeExmMq5tx1u9fbgLTKr26toW58OeC2sNvy1BEazSDBobWj0areehwvRUif")

    def test_boolean_get_prep_value(self):
        f = BooleanField()
        self.assertIs(f.get_prep_value(True), True)
        self.assertIs(f.get_prep_value('1'), True)
        self.assertIs(f.get_prep_value(1), True)
        self.assertIs(f.get_prep_value(False), False)
        self.assertIs(f.get_prep_value('0'), False)
        self.assertIs(f.get_prep_value(0), False)
        with self.assertRaises(exceptions.ValidationError):
            f.get_prep_value(None)
        f = BooleanField(null=True, blank=True)
        self.assertIsNone(f.get_prep_value(None))

    def test_boolean(self):
        obj = Boolean.objects.create(boolean=True)
        obj.refresh_from_db()
        self.assertEqual(obj.boolean, True)

    def test_binary(self):
        binary_data = b'\x00\x46\xFE'
        data_set = (binary_data, bytearray(
            binary_data), memoryview(binary_data))
        for bdata in data_set:
            with self.subTest(binary=repr(bdata)):
                dm = Binary(binary=bdata)
                dm.save()
                dm = Binary.objects.get(pk=dm.pk)
                self.assertEqual(dm.binary, bytes(bdata))
                dm.save()
                dm = Binary.objects.get(pk=dm.pk)
                self.assertEqual(dm.binary, bytes(bdata))

    def test_character(self):
        obj = Character.objects.create(char="test", email="abc@abc.com", text="test",
                                       slug="test", ip="127.0.0.1", url="https://www.google.com", file="test.png")
        obj.refresh_from_db()
        self.assertEqual(obj.char, "test")
        self.assertEqual(obj.email, "abc@abc.com")
        self.assertEqual(obj.text, "test")
        self.assertEqual(obj.slug, "test")
        self.assertEqual(obj.ip, "127.0.0.1")
        self.assertEqual(obj.url, "https://www.google.com")
        self.assertEqual(obj.file, "test.png")

    def test_email(self):
        e = EmailField()
        with self.assertRaises(exceptions.ValidationError):
            e.get_prep_value("abc")
        with self.assertRaises(exceptions.ValidationError):
            e.get_prep_value("abc@")
        with self.assertRaises(exceptions.ValidationError):
            e.get_prep_value("abc@abc")

    def test_ip(self):
        ip = GenericIPAddressField()
        with self.assertRaises(exceptions.ValidationError):
            ip.get_prep_value('1270.01.225.50')
        with self.assertRaises(exceptions.ValidationError):
            ip.get_prep_value("2001:0db86:85a3:0000:0000:8a2e:0370:733405")

    def test_url(self):
        url = URLField()
        with self.assertRaises(exceptions.ValidationError):
            url.get_prep_value("www.google.com")
        with self.assertRaises(exceptions.ValidationError):
            url.get_prep_value("http://google")

    def test_numeric(self):
        obj = Numeric.objects.create(bigint=890158413687135, smallint=-102, float=-25.0142546,
                                     decimal=25000, int=2050, positivebigint=25056479924, positiveint=25000,
                                     positivesmallint=125)
        obj.refresh_from_db()
        self.assertEqual(obj.bigint, 890158413687135)
        self.assertEqual(obj.smallint, -102)
        self.assertEqual(obj.float, -25.0142546)
        self.assertEqual(obj.decimal, 25000.00)
        self.assertEqual(obj.int, 2050)
        self.assertEqual(obj.positivebigint, 25056479924)
        self.assertEqual(obj.positiveint, 25000)
        self.assertEqual(obj.positivesmallint, 125)

    def test_postivie_ints(self):
        with self.assertRaises(exceptions.ValidationError):
            PositiveIntegerField().get_prep_value(-2500)
        with self.assertRaises(exceptions.ValidationError):
            PositiveSmallIntegerField().get_prep_value(-120)
        with self.assertRaises(exceptions.ValidationError):
            PositiveBigIntegerField().get_prep_value(-15896460658)

    def test_uuid(self):
        from uuid import uuid5, NAMESPACE_URL
        obj = Uuid.objects.create(uuid=uuid5(NAMESPACE_URL, "www.google.com"))
        obj.refresh_from_db()
        self.assertEqual(obj.uuid, uuid5(NAMESPACE_URL, "www.google.com"))
        obj = Uuid.objects.create(uuid=uuid5(
            NAMESPACE_URL, "www.google.com").hex)
        obj.refresh_from_db()
        self.assertEqual(obj.uuid, uuid5(NAMESPACE_URL, "www.google.com"))

    def test_datetime(self):
        from datetime import datetime
        datetime = datetime.now()
        obj = DateTime.objects.create(
            datetime=datetime, date=datetime.date(), time=datetime.time())
        obj.refresh_from_db()
        self.assertEqual(obj.datetime, datetime)
        self.assertEqual(obj.date, datetime.date())
        self.assertEqual(obj.time, datetime.time())
