from django.test import SimpleTestCase

from . import calc


class CalcTests(SimpleTestCase):

    def test_add(self):
        res = calc.add(3, 8)
        self.assertEqual(res, 11)

    def test_subtract(self):
        res = calc.subtract(5, 11)
        self.assertEqual(res, 6)
