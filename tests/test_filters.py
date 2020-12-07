from CryptographicFields.filters import *
from .models import User
from django.test import TestCase
from re import compile
import datetime
from django.conf import settings


class Filters(TestCase):
    queryset = User.objects.all()
    setattr(settings, 'CRYPTOGRAPHIC_KEY',
            "XmeExmMq5tx1u9fbgLTKr26toW58OeC2sNvy1BEazSDBobWj0areehwvRUif")
    def setUp(self) -> None:
        from uuid import uuid5, NAMESPACE_URL
        self.user1 = User.objects.create(uuid=uuid5(NAMESPACE_URL, "https://www.a.random.com"), username="admin", first_name="Albert",
                                         last_name="Frost", age=24, email="albert@gmail.com", joined=datetime.datetime(2015, 12, 26, 18, 35, 54))
        self.user2 = User.objects.create(uuid=uuid5(NAMESPACE_URL, "https://www.b.random.com"), username="empi16", first_name="Empi",
                                         last_name="Tsar", age=16, email="empi@rediff.com", joined=datetime.datetime(2025, 12, 28, 12, 35, 34))
        self.user3 = User.objects.create(uuid=uuid5(NAMESPACE_URL, "https://www.c.random.com"), username="dextEr", first_name="Dexter",
                                         last_name="Flutnes", age=28, email="dextEr@random.com", joined=datetime.datetime(2018, 2, 20, 20, 50, 15))
        self.user4 = User.objects.create(uuid=uuid5(NAMESPACE_URL, "https://www.d.random.com"), username="shahprogrammer", first_name="Dhwanil",
                                         last_name="Shah", age=18, email="shahprogrammer@random.com", joined=datetime.datetime(2018, 4, 1, 20, 25, 14))
        self.user5 = User.objects.create(uuid=uuid5(NAMESPACE_URL, "https://www.e.random.com"), username="graphin", first_name="Graphin",
                                         last_name="frost", age=30, email="graphin@yahoo.com", joined=datetime.datetime(2005, 9, 22, 9, 33, 40))
        self.user6 = User.objects.create(uuid=uuid5(NAMESPACE_URL, "https://www.f.random.com"), username="abc", first_name="abc",
                                         last_name="xyz", age=16, email="abc@yahoo.com", joined=datetime.datetime(2009, 7, 22, 14, 5, 40))
        self.user1.refresh_from_db()
        self.user2.refresh_from_db()
        self.user3.refresh_from_db()
        self.user4.refresh_from_db()
        self.user5.refresh_from_db()
        self.user6.refresh_from_db()
        return super().setUp()

    def get_data(self, queryset):
        return getattr(queryset, "_result_cache")

    def test_lt(self):
        self.assertEqual(self.get_data(sort(self.queryset, lt, 'age', 18)), [
                         self.user2, self.user6])

    def test_lte(self):
        self.assertEqual(self.get_data(sort(self.queryset, lte, 'age', 18)), [
                         self.user2, self.user4, self.user6])

    def test_gt(self):
        self.assertEqual(self.get_data(sort(self.queryset, gt, 'age', 18)), [
                         self.user1, self.user3, self.user5])

    def test_gte(self):
        self.assertEqual(self.get_data(sort(self.queryset, gte, 'age', 18)), [
                         self.user1, self.user3, self.user4, self.user5])

    def test_startswith(self):
        self.assertEqual(self.get_data(
            sort(self.queryset, startswith, 'last_name', "F")), [self.user1, self.user3])

    def test_istartswith(self):
        self.assertEqual(self.get_data(sort(self.queryset, istartswith, 'last_name', "F")), [
                         self.user1, self.user3, self.user5])

    def test_endswith(self):
        self.assertEqual(self.get_data(
            sort(self.queryset, endswith, 'username', "er")), [self.user4])

    def test_iendswith(self):
        self.assertEqual(self.get_data(
            sort(self.queryset, iendswith, 'username', "er")), [self.user3, self.user4])

    def test_contains(self):
        self.assertEqual(self.get_data(sort(self.queryset, contains, 'email', "er")), [
                         self.user1, self.user4])

    def test_icontains(self):
        self.assertEqual(self.get_data(sort(self.queryset, icontains, 'email', "er")), [
                         self.user1, self.user3, self.user4])

    def test_range(self):
        self.assertEqual(self.get_data(sort(self.queryset, range, "age", [18, 30])), [
                         self.user1, self.user3])

    def test_date(self):
        self.assertEqual(self.get_data(
            sort(self.queryset, date, "joined", datetime.date(2009, 7, 22))), [self.user6])

    def test_year(self):
        self.assertEqual(self.get_data(sort(self.queryset, year, "joined", 2018)), [
                         self.user3, self.user4])

    def test_month(self):
        self.assertEqual(self.get_data(sort(self.queryset, month, "joined", 12)), [
                         self.user1, self.user2])

    def test_day(self):
        self.assertEqual(self.get_data(sort(self.queryset, day, "joined", 22)), [
                         self.user5, self.user6])

    def test_time(self):
        self.assertEqual(self.get_data(
            sort(self.queryset, time, "joined", datetime.time(14, 5, 40))), [self.user6])

    def test_order_by(self):
        self.assertEqual(self.get_data(order_by(self.queryset, ("age", "username"))), [
                         self.user6, self.user2, self.user4, self.user1, self.user3, self.user5])

    def test_date_lt(self):
        self.assertEqual(self.get_data(sort(self.queryset, date_lt, "joined",
                                            datetime.datetime(2010, 1, 1))), [self.user5, self.user6])

    def test_date_lte(self):
        self.assertEqual(self.get_data(sort(self.queryset, date_lte, "joined", datetime.datetime(
            2015, 12, 26))), [self.user1, self.user5, self.user6])

    def test_date_gt(self):
        self.assertEqual(self.get_data(sort(self.queryset, date_gt, "joined", datetime.datetime(
            2015, 12, 26))), [self.user2, self.user3, self.user4])

    def test_date_gte(self):
        self.assertEqual(self.get_data(sort(self.queryset, date_gte, "joined", datetime.datetime(
            2015, 12, 26))), [self.user1, self.user2, self.user3, self.user4])

    def test_date_range(self):
        self.assertEqual(self.get_data(sort(self.queryset, date_range, "joined", [datetime.datetime(
            2015, 12, 26), datetime.datetime(2020, 1, 1)])), [self.user3, self.user4])

    def test_time_lt(self):
        self.assertEqual(self.get_data(
            sort(self.queryset, time_lt, "joined", datetime.time(12, 0, 0))), [self.user5])

    def test_time_lte(self):
        self.assertEqual(self.get_data(sort(self.queryset, time_lte, "joined", datetime.time(
            14, 30, 0))), [self.user2, self.user5, self.user6])

    def test_time_gt(self):
        self.assertEqual(self.get_data(
            sort(self.queryset, time_gt, "joined", datetime.time(20, 25, 14))), [self.user3])

    def test_time_gte(self):
        self.assertEqual(self.get_data(sort(self.queryset, time_gte,
                                            "joined", datetime.time(20, 25, 14))), [self.user3, self.user4])

    def test_time_range(self):
        self.assertEqual(self.get_data(sort(self.queryset, time_range, "joined", [datetime.time(
            18, 0, 0), datetime.time(23, 0, 0)])), [self.user1, self.user3, self.user4])

    def test_regex(self):
        self.assertEqual(self.get_data(sort(self.queryset, regex, "email", compile(
            r'[a-zA-z0-9_]+@\w+\.\w'))), [self.user1, self.user2, self.user3, self.user4, self.user5, self.user6])
