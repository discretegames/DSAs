"""Test suite for DSAs.sorting."""

import tutil  # Must import tutil before DSAs for VSCode debugging to work.
import DSAs.sorting as sorting
from itertools import permutations, product
import unittest


class TestSorting(unittest.TestCase):
    def get_sort_checker(self, sorter):  # todo probably update to allow not-in-place sorters
        def sort_checker(*arrs, key=None, reverse=False):
            for arr in arrs:
                copy = arr.copy()
                expected = sorted(copy, key=key, reverse=reverse)
                sorter(copy, key=key, reverse=reverse)
                self.assertEqual(copy, expected)
        return sort_checker

    def get_modifiers_and_keys(self):
        mods = [int, float,  # todo bool and others may make unstable sorts fail tests
                lambda x: x,
                lambda x: -x,
                lambda x: x / 10.0,
                lambda x: x + 100,
                lambda x: x - 100,
                lambda x: x**2,
                lambda x: 7e+9 * x,
                lambda x: 7e-9 * x]
        keys = [None, str,
                lambda x: [x],
                lambda x: [x, x - 1],
                lambda x: (x,),
                lambda x: (x + 1, x),
                lambda x: f"No. {x}",
                lambda x: str(x)[::-1]
                ] + mods
        return mods, keys

    def basic_sort_tests(self, sorter):
        def sort(arr):
            copy = arr.copy()
            sorter(copy)
            return copy
        self.assertEqual(sort([]), [])
        self.assertEqual(sort([1, 2]), [1, 2])
        self.assertEqual(sort([2, 1]), [1, 2])
        self.assertEqual(sort(["A", "B"]), ["A", "B"])
        self.assertEqual(sort(["B", "A"]), ["A", "B"])
        self.assertEqual(sort(["10", "2"]), ["10", "2"])
        self.assertEqual(sort(["2", "10"]), ["10", "2"])
        self.assertEqual(sort([1, 2, 3, 4]), [1, 2, 3, 4])
        self.assertEqual(sort([4, 3, 2, 1]), [1, 2, 3, 4])

    def thorough_sort_tests(self, sorter, max_length=5):
        checker = self.get_sort_checker(sorter)
        modifiers, keys = self.get_modifiers_and_keys()
        count = 0
        for modifier, key, length, reverse in product(modifiers, keys, range(max_length), [True, False]):
            for r in range(length):
                perms = map(list, permutations(range(1, length + 1), r))
                arrs = [list(map(modifier, arr)) for arr in perms]
                count += len(arrs)
                checker(*arrs, key=key, reverse=reverse)
        # print(f"Thoroughly tested {count} lists.")
        return count

    def random_sort_tests(self, sorter):
        checker = self.get_sort_checker(sorter)

        def random_tests(min_length, max_length, min_value, max_value, times=10):
            for _ in range(times):
                checker(tutil.random_arr(min_length, max_length, min_value, max_value))

        random_tests(0, 10, 0, 100, 20)
        random_tests(0, 100, -20, 20, 20)
        random_tests(500, 1000, -10, 10, 5)
        random_tests(500, 1000, -10**9, 10**9, 5)

    def all_sort_tests(self, sorter):
        self.basic_sort_tests(sorter)
        self.thorough_sort_tests(sorter)
        self.random_sort_tests(sorter)

    # todo random for unstable sorts

    # todo stability test

    def test_bubblesort(self):
        self.all_sort_tests(sorting.bubblesort)

    def test_selectionsort(self):
        self.basic_sort_tests(sorting.selectionsort)
        self.thorough_sort_tests(sorting.selectionsort)


if __name__ == "__main__":
    try:
        unittest.main()
    except SystemExit:  # So debugger doesn't trigger.
        pass
