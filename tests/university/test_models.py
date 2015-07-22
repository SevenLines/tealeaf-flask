from datetime import datetime
from app import Group
from tests import TestCaseBase


class TestGroup(TestCaseBase):
    def test_current_year(self):
        self.assertEqual(2013, Group.current_year(datetime(2014, 1, 1)))
        self.assertEqual(2013, Group.current_year(datetime(2014, 8, 1)))
        self.assertEqual(2014, Group.current_year(datetime(2014, 9, 1)))
        self.assertEqual(2014, Group.current_year(datetime(2014, 12, 1)))
