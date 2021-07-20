"""Test suite for DSAs.sorting."""

import tutil  # Must import tutil before DSAs for VSCode debugging to work.
import DSAs.sorting as sorting
from itertools import permutations, product
import unittest


def sorter_test(sorter, stable=True, in_place=True):
    def tester(self):
        nip_sorter = sorting.not_in_place(sorter) if in_place else sorter
        self.basic_sort_tests(nip_sorter)
        self.confirm_stability(nip_sorter, stable)

        # else:
        #     self.confirm_unstable(sorter)
        #     sorter = sorting.util.stabilize(sorter)

        # if in_place:
        #     self.confirm_in_place(sorter)
        # else:
        #     self.confirm_not_in_place(sorter)
        #     sorter = sorting.util.in_place(sorter)

        # self.thorough_sort_tests(sorter)
        # self.random_sort_tests(sorter)
    return tester


class TestSorting(unittest.TestCase):

    def confirm_stability(self, nip_sorter, stable):
        def make_map(f):
            incrementer = 0

            def mapper(x):
                nonlocal incrementer
                incrementer += 1
                return f(x), incrementer
            return mapper
        maps = lambda x: 0, lambda x: x // 2, lambda x: x // 3
        assertion = all if stable else lambda data: False in data
        self.thorough_sort_tests(nip_sorter, map(make_map, maps), [lambda x: x[0]], assertion, 6)

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

    def get_sort_checker(self, nip_sorter):
        def sort_checker(*arrs, key=None, reverse=False):
            for arr in arrs:
                result = nip_sorter(arr, key=key, reverse=reverse)
                if result != sorted(arr, key=key, reverse=reverse):
                    return False
            return True
        return sort_checker

    def get_maps_and_keys(self):  # todo move and add bool and more
        maps = [int, float,
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
                ] + maps
        return maps, keys

    def thorough_sort_tests(self, nip_sorter, maps=None, keys=None, assertion=all, max_length=6):
        checker = self.get_sort_checker(nip_sorter)
        checker_data = []
        for length, map_, key, reverse in product(range(max_length + 1), maps, keys, [True, False]):
            arrs = [list(map(map_, perm)) for perm in permutations(range(length), length)]
            checker_data.append(checker(*arrs, key=key, reverse=reverse))
        self.assertTrue(assertion(checker_data))

    def random_sort_tests(self, sorter):
        checker = self.get_sort_checker(sorter)

        def random_tests(min_length, max_length, min_value, max_value, times=10):
            for _ in range(times):
                self.assertTrue(all(checker(tutil.random_arr(min_length, max_length, min_value, max_value))))

        random_tests(0, 10, 0, 100, 20)
        random_tests(0, 100, -20, 20, 20)
        random_tests(500, 1000, -10, 10, 5)
        random_tests(500, 1000, -10**9, 10**9, 5)

    test_bubblesort = sorter_test(sorting.bubblesort)
    test_selectionsort = sorter_test(sorting.selectionsort, False)

    # todo test decorators


if __name__ == "__main__":
    try:
        unittest.main()
    except SystemExit:  # So debugger doesn't trigger.
        pass
