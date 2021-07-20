"""Test suite for DSAs.sorting."""

import tutil  # Must import tutil before DSAs for VSCode debugging to work.
import DSAs.sorting as sorting
from itertools import combinations_with_replacement, permutations, product
import unittest

test_maps = (bool, float,
             lambda x: x,
             lambda x: -x,
             lambda x: x // 2,
             lambda x: x**2,
             lambda _: 0)
test_keys = (None, str,
             lambda x: (x + 1, x),
             lambda x: str(x)[::-1]
             ) + test_maps


def sorter_test(sorter, stable=True, in_place=True):
    def tester(self):
        nip_sorter = sorter if not in_place else sorting.not_in_place(sorter)

        self.confirm_stability(nip_sorter, stable)

        stable_sorter = sorter if stable else sorting.stabilize(in_place)(sorter)

        # else:
        #     self.confirm_unstable(sorter)
        #     sorter = sorting.util.stabilize(sorter)

        # if in_place:
        #     self.confirm_in_place(sorter)
        # else:
        #     self.confirm_not_in_place(sorter)
        #     sorter = sorting.util.in_place(sorter)

        snip_sorter = nip_sorter if stable else sorting.stabilize(False)(nip_sorter)

        self.basic_sort_tests(snip_sorter)
        self.thorough_sort_tests(snip_sorter)
        self.random_sort_tests(snip_sorter)
    return tester


class TestSorting(unittest.TestCase):

    def confirm_sorted(self, nip_sorter, arr, key=None, reverse=False):
        expected = sorted(arr, key=key, reverse=reverse)
        actual = nip_sorter(arr, key=key, reverse=reverse)
        self.assertEqual(actual, expected)

    def confirm_stability(self, nip_sorter, stable):
        incrementer = 0

        def mapper(value):
            nonlocal incrementer
            incrementer += 1
            return value, incrementer
        maps, keys = [mapper], [lambda x: x[0]]

        if stable:
            self.thorough_sort_tests(nip_sorter, maps, keys)
        else:
            failed = False

            def confirmer(nip_sorter, arr, key=None, reverse=False):
                if len(set(map(key, arr))) == len(arr):
                    self.confirm_sorted(nip_sorter, arr, key, reverse)
                else:
                    expected = sorted(arr, key=key, reverse=reverse)
                    actual = nip_sorter(arr, key=key, reverse=reverse)
                    if expected != actual:  # When unstable some failures should happen.
                        nonlocal failed
                        failed = True
            self.thorough_sort_tests(nip_sorter, maps, keys, confirmer)
            self.assertTrue(failed, "No instability found. The sort may be stable.")

    def confirm_in_placeness(self, stable_sorter, in_place):
        pass  # todo

    def basic_sort_tests(self, nip_sorter):  # Doesn't check stability.
        self.assertEqual(nip_sorter([]), [])
        self.assertEqual(nip_sorter([1, 2]), [1, 2])
        self.assertEqual(nip_sorter([2, 1]), [1, 2])
        self.assertEqual(nip_sorter(["A", "B"]), ["A", "B"])
        self.assertEqual(nip_sorter(["B", "A"]), ["A", "B"])
        self.assertEqual(nip_sorter(["10", "2"]), ["10", "2"])
        self.assertEqual(nip_sorter(["2", "10"]), ["10", "2"])
        self.assertEqual(nip_sorter([1, 2, 3, 4]), [1, 2, 3, 4])
        self.assertEqual(nip_sorter([4, 3, 2, 1]), [1, 2, 3, 4])

    def thorough_sort_tests(self, nip_sorter, maps=test_maps, keys=test_keys, confirmer=None, max_length=5):
        if not confirmer:
            confirmer = self.confirm_sorted

        arrays = set()
        for length in range(max_length + 1):
            for combo in combinations_with_replacement(range(length), length):
                for perm in permutations(combo):  # Probably a better way to get all permutations here.
                    arrays.add(perm)
        for arr, map_, key, reverse in product(arrays, maps, keys, [False, True]):
            confirmer(nip_sorter, list(map(map_, arr)), key=key, reverse=reverse)

    def random_sort_tests(self, nip_sorter):
        def random_tests(min_length, max_length, min_value, max_value, times=10):
            for _ in range(times):
                arr = tutil.random_arr(min_length, max_length, min_value, max_value)
                self.confirm_sorted(nip_sorter, arr)
                self.confirm_sorted(nip_sorter, arr, reverse=True)

        random_tests(0, 10, 0, 100, 20)
        random_tests(0, 100, -20, 20, 20)
        random_tests(500, 1000, -10, 10, 5)
        random_tests(500, 1000, -10**9, 10**9, 5)

    test_bubblesort = sorter_test(sorting.bubblesort)
    test_selectionsort = sorter_test(sorting.selectionsort, False)

    # todo test decorators
    # def test_decorators(self):
    #     stable_sort = sorted


if __name__ == "__main__":
    try:
        unittest.main()
    except SystemExit:  # So debugger doesn't trigger.
        pass
