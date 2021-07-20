"""Test suite for DSAs.sorting."""

import tutil  # Must import tutil before DSAs for VSCode debugging to work.
import unittest
import DSAs.sorting as sorting
from itertools import combinations_with_replacement, permutations, product

test_maps = (bool,
             float,
             lambda x: x,
             lambda x: -x,
             lambda x: x // 2,
             lambda x: x**2,
             lambda _: 0)
test_keys = (None,
             str,
             lambda x: (x + 1, x),
             lambda x: str(x)[::-1]
             ) + test_maps


def sorter_test(sorter, stable, in_place):
    def tester(self):
        nonlocal sorter
        self.confirm_in_placeness(sorter, in_place)
        if in_place:
            sorter = sorting.not_in_place(sorter)
        self.confirm_stability(sorter, stable)
        if not stable:
            sorter = sorting.stabilize(False)(sorter)
        self.basic_sort_tests(sorter)
        self.thorough_sort_tests(sorter)
        self.random_sort_tests(sorter)
    return tester


class TestSorting(unittest.TestCase):

    def confirm_sorted(self, nip_sorter, arr, key=None, reverse=False):
        expected = sorted(arr, key=key, reverse=reverse)
        actual = nip_sorter(arr, key=key, reverse=reverse)
        self.assertEqual(actual, expected)

    def confirm_in_placeness(self, sorter, in_place):
        arr = [2, 5, 4, 1, 3]
        if in_place:
            sorter(arr)
            sorted_arr = arr
        else:
            copy = arr.copy()
            sorted_arr = sorter(arr)
            self.assertEqual(copy, arr)

        self.assertEqual(sorted_arr, [1, 2, 3, 4, 5])

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

    def test_decorators(self):
        def confirm_properties(sorter, stable, in_place):
            self.confirm_in_placeness(sorter, in_place)
            if in_place:
                nip = sorting.not_in_place(sorter)
                self.confirm_in_placeness(nip, False)
                self.confirm_in_placeness(sorting.in_place(nip), True)
                self.confirm_stability(nip, stable)
            else:
                ip = sorting.in_place(sorter)
                self.confirm_in_placeness(ip, True)
                self.confirm_in_placeness(sorting.not_in_place(ip), False)
                self.confirm_stability(sorter, stable)

            stabilized = sorting.stabilize(in_place)(sorter)
            if in_place:
                stabilized = sorting.not_in_place(stabilized)
            self.confirm_stability(stabilized, True)

        stable_ip_sorter = lambda arr, key=None, reverse=False: arr.sort(key=key, reverse=reverse)
        stable_nip_sorter = sorted
        unstable_ip_sorter = sorting.selectionsort
        unstable_nip_sorter = sorting.not_in_place(unstable_ip_sorter)

        confirm_properties(stable_ip_sorter, True, True)
        confirm_properties(stable_nip_sorter, True, False)
        confirm_properties(unstable_ip_sorter, False, True)
        confirm_properties(unstable_nip_sorter, False, False)

    test_bubblesort = sorter_test(sorting.bubblesort, True, True)
    test_selectionsort = sorter_test(sorting.selectionsort, False, True)


if __name__ == "__main__":
    print('Running from main...')
    try:
        unittest.main()
    except SystemExit:  # So debugger doesn't trigger.
        pass
