import unittest
import sys

sys.path.append("src")

from sqlite_phone_directory import SqlitePhoneDirectoryActions

class TestSqlitePhoneDirectory(unittest.TestCase):

    def setUp(self):
        self._db = SqlitePhoneDirectoryActions(database="sqlite:///:memory:")
        self._db._add_a_user(user_id=1122, phone='1'*10, name='ben')

    def test_user_exists(self):
        assert self._db.user_exists(1122)

    def test_user_does_not_exist(self):
        assert not self._db.user_exists(1123)

    def test_get_name(self):
        assert self._db.get_name(1122) == 'ben'

    def test_get_phone_number(self):
        assert self._db.get_phone_number(1122) == '1'*10

    def test_update_phone_number(self):
        self._db.update_phone_number(user_id=1122, new_number='2'*10)
        assert self._db.get_phone_number(1122) == '2'*10




