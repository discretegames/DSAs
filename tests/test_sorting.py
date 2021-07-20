"""Test suite for DSAs.sorting."""

import tutil  # Must import tutil before DSAs for VSCode debugging to work.
import DSAs.sorting as sorting
from itertools import permutations, product
import unittest

test_maps = (int, float, bool,
             lambda x: x,
             lambda x: 0,
             lambda x: -x,
             lambda x: x // 2,
             lambda x: x + 100,
             lambda x: x - 100,
             lambda x: x**2,
             lambda x: 7e+9 * x,
             lambda x: 7e-9 * x)
test_keys = (None, str,
             lambda x: [x],
             lambda x: [x, x - 1],
             lambda x: (x,),
             lambda x: (x + 1, x),
             lambda x: f"No. {x}",
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

    def get_sort_checker(self, nip_sorter):
        def checker(arr, key=None, reverse=False):
            expected = sorted(arr, key=key, reverse=reverse)
            actual = nip_sorter(arr, key=key, reverse=reverse)
            return actual == expected
        return checker

    # todo rewrite so checker asserts sorted for better error msgs
    def thorough_sort_tests(self, nip_sorter, maps=test_maps, keys=test_keys, assertion=all, max_length=5):
        checker = self.get_sort_checker(nip_sorter)
        results = []
        for length, map_, key, reverse in product(range(max_length + 1), maps, keys, [False, True]):
            for perm in permutations(range(length), length):
                arr = list(map(map_, perm))
                results.append(checker(arr, key=key, reverse=reverse))
        self.assertTrue(assertion(results))

    def random_sort_tests(self, nip_sorter):
        checker = self.get_sort_checker(nip_sorter)

        def random_tests(min_length, max_length, min_value, max_value, times=10):
            for _ in range(times):
                self.assertTrue(checker(tutil.random_arr(min_length, max_length, min_value, max_value)))

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
