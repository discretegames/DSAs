"""Test suite for DSAs.sorting."""

from itertools import permutations, product
import unittest
import random
import sys
import os

# Needed to allow direct debugging in VSCode.
sys.path.append(f'{os.path.dirname(__file__)}/../src')
# TODO put elsewhere or rethink


class TestSorting(unittest.TestCase):
    import DSAs.sorting as sorting

    def get_sort_checker(self, sorter):
        def sort_checker(*arrs, key=None, reverse=False):
            for arr in arrs:
                copy = arr.copy()
                expected = sorted(copy, key=key, reverse=reverse)
                sorter(copy, key=key, reverse=reverse)
                if copy != expected:
                    print(999)
                    pass

                self.assertEqual(copy, expected)
        return sort_checker

    def get_modifiers_and_keys(self):
        mods = [int, float, bool,
                lambda x: x,
                lambda x: -x,
                lambda x: 1,
                lambda x: x // 10,
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

    def thorough_sort_tests(self, sorter, max_length=6):
        checker = self.get_sort_checker(sorter)
        modifiers, keys = self.get_modifiers_and_keys()
        count = 0
        for modifier, key, length, reverse in product(modifiers, keys, range(max_length), [True, False]):
            for r in range(length):
                perms = map(list, permutations(range(1, length + 1), r))
                arrs = [list(map(modifier, arr)) for arr in perms]
                count += len(arrs)
                checker(*arrs, key=key, reverse=reverse)
        print(f"Thoroughly tested {count} lists.")
        return count

    def random_sort_tests(self, sorter, seed=None):
        random.seed(seed)
        checker = self.get_sort_checker(sorter)
        modifiers, keys = self.get_modifiers_and_keys()

        def random_arr(max_length, minimum, maximum):
            length = random.randint(0, max_length + 1)
            return [random.randint(minimum, maximum) for _ in range(length)]

        def random_tests(max_length, minimum, maximum, times=10):
            times = 2
            for modifier, key, _ in product(modifiers, keys, range(times)):
                arr = random_arr(max_length, minimum, maximum)
                checker(list(map(modifier, arr)), key=key)

        # TODO likely remove modifier and keys since too slow here and unnecessary
        # random_tests(10, -20, 20)
        # random_tests(100, -20, 20)
        # random_tests(1000, -20, 2, 100)

    def all_sort_tests(self, sorter):
        self.basic_sort_tests(sorter)
        self.thorough_sort_tests(sorter)
        self.random_sort_tests(sorter)

    def test_bubblesort(self):
        self.all_sort_tests(self.sorting.bubblesort)


if __name__ == "__main__":
    try:
        unittest.main()
    except SystemExit:  # So debugger doesn't trigger.
        pass
