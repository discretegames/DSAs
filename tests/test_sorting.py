"""Test suite for sorting methods."""


import unittest

# from DSAs.sorting import bubblesort

# from DSAs import *
from DSAs.sorting import bubblesort
from DSAs.util import swap as s


class TestMathDunders(unittest.TestCase):
    def test_sample(self):
        L = [3, 2, 1]
        # print(util)
        # print(sorting)
        bubblesort(L)
        s(L, 1, 1)
        self.assertEqual(L, [1, 2, 3])
        print('Tested!', L)


# unittest.main()
