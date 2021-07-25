"""Test suite for DSAs.sorting."""

import tutil  # Must import tutil before DSAs for VSCode debugging to work.
import unittest
import DSAs.sorting as sorting
from itertools import product

thoroughness = 4  # Higher is more thorough but exponentially slower. Keep at 4 or higher.
default_maps = (int,
                bool,
                float,
                lambda x: -x,
                lambda x: x // 2,
                lambda x: x**2,
                lambda _: 0)
default_keys = (None,
                str,
                lambda x: (x + 1, x),
                lambda x: str(x)[::-1]
                ) + default_maps
default_mapkeys = tuple(product(default_maps, default_keys))


def sorter_test(sorter, stable, in_place, mapkeys=default_mapkeys):
    def tester(self):
        nonlocal sorter
        self.confirm_in_placeness(sorter, in_place)
        if in_place:
            sorter = sorting.util.not_in_place(sorter)
        self.confirm_stability(sorter, stable)
        if not stable:
            sorter = sorting.util.stabilize(False)(sorter)
        self.basic_sort_tests(sorter)
        self.thorough_sort_tests(sorter, mapkeys)
        self.random_sort_tests(sorter)
    return tester


def gapped_sorter_test(sorter, stable, good_gaps, bad_gaps):
    def tester(self):
        def call_gapped_sorter(gaps):
            def gapped_sorter(arr, key=None, reverse=False):
                sorter(arr, key=key, reverse=reverse, gaps=gaps)
            sorter_test(gapped_sorter, stable, True)(self)

        for gaps in good_gaps:
            call_gapped_sorter(gaps)
        for gaps in bad_gaps:
            self.assertRaises(AssertionError, call_gapped_sorter, gaps)
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
        mapkeys = [(mapper, lambda x: x[0])]

        if stable:
            self.thorough_sort_tests(nip_sorter, mapkeys)
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
            self.thorough_sort_tests(nip_sorter, mapkeys, confirmer)
            self.random_sort_tests(nip_sorter, mapkeys, confirmer)
            self.assertTrue(failed, "No instability found. The sort may be stable.")

    def basic_sort_tests(self, nip_sorter):
        self.assertEqual(nip_sorter([]), [])
        self.assertEqual(nip_sorter([0]), [0])
        self.assertEqual(nip_sorter([0, 0]), [0, 0])
        self.assertEqual(nip_sorter([1, 2]), [1, 2])
        self.assertEqual(nip_sorter([2, 1]), [1, 2])
        self.assertEqual(nip_sorter([-2, -1]), [-2, -1])
        self.assertEqual(nip_sorter([-1, -2]), [-2, -1])
        self.assertEqual(nip_sorter([1, 1, 2]), [1, 1, 2])
        self.assertEqual(nip_sorter([1, 2, 1]), [1, 1, 2])
        self.assertEqual(nip_sorter([2, 1, 1]), [1, 1, 2])
        self.assertEqual(nip_sorter([1, 1, 2]), [1, 1, 2])
        self.assertEqual(nip_sorter([1, 2, 3, 4]), [1, 2, 3, 4])
        self.assertEqual(nip_sorter([4, 3, 2, 1]), [1, 2, 3, 4])
        self.assertEqual(nip_sorter([-2, 2, -1, 1, 0]), [-2, -1, 0, 1, 2])

    def thorough_sort_tests(self, nip_sorter, mapkeys=((lambda x: x, None),), confirmer=None):
        if not confirmer:
            confirmer = self.confirm_sorted
        # TODO True False and below
        for length, mapkey, reverse in product(range(thoroughness + 1), mapkeys, (False, True)):
            for arr in product(range(length), repeat=length):
                confirmer(nip_sorter, list(map(mapkey[0], arr)), key=mapkey[1], reverse=reverse)

    def random_sort_tests(self, nip_sorter, mapkeys=((lambda x: x, None),), confirmer=None):
        if not confirmer:
            confirmer = self.confirm_sorted

        def random_tests(min_len, max_len, min_val, max_val, times=10):
            for _, mapkey, reverse in product(range(times), mapkeys, (False, True)):
                arr = tutil.random_arr(min_len, max_len, min_val, max_val)
                confirmer(nip_sorter, list(map(mapkey[0], arr)), key=mapkey[1], reverse=reverse)

        random_tests(0, 10, 0, 100, 20)
        random_tests(0, 100, 0, 10, 20)
        random_tests(200, 500, -10, 10)
        random_tests(200, 500, -100_000, 100_000)

    def test_decorators(self):
        def confirm_properties(sorter, stable, in_place):
            self.confirm_in_placeness(sorter, in_place)
            if in_place:
                nip = sorting.util.not_in_place(sorter)
                self.confirm_in_placeness(nip, False)
                self.confirm_in_placeness(sorting.util.in_place(nip), True)
                self.confirm_stability(nip, stable)
            else:
                ip = sorting.util.in_place(sorter)
                self.confirm_in_placeness(ip, True)
                self.confirm_in_placeness(sorting.util.not_in_place(ip), False)
                self.confirm_stability(sorter, stable)

            stabilized = sorting.util.stabilize(in_place)(sorter)
            if in_place:
                stabilized = sorting.util.not_in_place(stabilized)
            self.confirm_stability(stabilized, True)

        stable_ip_sorter = lambda arr, key=None, reverse=False: arr.sort(key=key, reverse=reverse)
        stable_nip_sorter = sorted
        unstable_ip_sorter = sorting.selectionsort
        unstable_nip_sorter = sorting.util.not_in_place(unstable_ip_sorter)

        confirm_properties(stable_ip_sorter, True, True)
        confirm_properties(stable_nip_sorter, True, False)
        confirm_properties(unstable_ip_sorter, False, True)
        confirm_properties(unstable_nip_sorter, False, False)

    def test_is_sorted(self):
        is_sorted = sorting.util.is_sorted

        are_sorted = [
            [],
            [10],
            [1, 2, 3],
            [1, 2, 2],
            [1, 1, 1],
            ["Apple", "Banana", "atlas", "xylophone"]
        ]
        for arr in are_sorted:
            self.assertTrue(is_sorted(arr))

        are_not_sorted = [
            [2, 1],
            [3, 2, 1],
            [1e-19, 1e-20],
            [10, 20, 10],
            ["dab", "cab"]
        ]
        for test in are_not_sorted:
            self.assertFalse(is_sorted(test))

        self.assertTrue(is_sorted([1, 2, 3], key=bool))
        self.assertTrue(is_sorted([1, 2, 3], key=bool, reverse=True))
        self.assertTrue(is_sorted([3, 2, 1], reverse=True))

        self.assertTrue(is_sorted([0, 1, 2], key=bool))
        self.assertTrue(is_sorted([2, 1, 0], key=bool, reverse=True))
        self.assertFalse(is_sorted([2, 1, 0], key=bool))

        self.assertTrue(is_sorted([(999, 1), (555, 1), (222, 1)], key=lambda x: x[1]))
        self.assertFalse(is_sorted([(999, 1), (555, 1), (222, 1)], key=lambda x: x[0]))

    test_bubblesort = sorter_test(sorting.bubblesort, True, True)
    test_cocktailsort = sorter_test(sorting.cocktailsort, True, True)
    test_insertionsort = sorter_test(sorting.insertionsort, True, True)
    test_selectionsort = sorter_test(sorting.selectionsort, False, True)
    test_heapsort = sorter_test(sorting.heapsort, False, True)

    test_shellsort = gapped_sorter_test(sorting.shellsort, False, (None, [2, 1], [2, 1, 2], [100, 1]), ([2], [100]))
    test_stable_shellsort = gapped_sorter_test(sorting.shellsort, True, ([1], [1, 2]), ())

    test_combsort = gapped_sorter_test(sorting.combsort, False, (None, [2, 1], [100, 1]), ([2], [100]))
    test_stable_combsort = gapped_sorter_test(sorting.combsort, True, ([1],), ())

    test_pigeonholesort = sorter_test(sorting.pigeonholesort, True, True,
                                      [(lambda x: x, None), (lambda x: (f"num{x}", x), lambda x: x[1])])


if __name__ == "__main__":
    print('Running from main...')
    try:
        unittest.main()
    except SystemExit:  # So debugger doesn't trigger.
        pass
