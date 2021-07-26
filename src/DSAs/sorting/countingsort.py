import timeit
from collections import Counter


def countingsort(arr):
    out = [None] * len(arr)
    if arr:
        offset = min(arr)
        counts = [0] * (max(arr) - offset + 1)

        for value in arr:  # Count everything.
            counts[value - offset] += 1

        for i in range(1, len(counts)):  # Accumulate prefix sums.
            counts[i] += counts[i - 1]

        for value in arr:  # Build out from
            counts[value - offset] -= 1
            out[counts[value - offset]] = value

    return out


def countingsort_alt(arr):  # works but not for radix sort
    if arr:
        offset = min(arr)
        counts = [0] * (max(arr) - offset + 1)

        for value in arr:  # Count everything.
            counts[value - offset] += 1

        index_to_fill = 0
        for i in range(len(counts)):  # Refill arr based on counts.
            while counts[i] > 0:
                arr[index_to_fill] = i + offset
                index_to_fill += 1
                counts[i] -= 1


def countingsort2(arr):  # in place, memory efficient for large ranges
    if arr:
        i = 0
        counts = Counter(arr)
        for num in range(min(counts), max(counts) + 1):
            if num in counts:  # not necessary but speeds things up
                arr[i:i + counts[num]] = [num] * counts[num]
                i += counts[num]


# todo maybe time them?
L = [9]  # [1, 4, 1, 2, 7, 5, 2]
print(countingsort_alt(L))
print(L)


# setup = """
# from collections import Counter
# c = Counter()
# x = 0"""
# N = 100000
# p = print
# p(timeit.timeit('if 99 in c: x += 1', setup=setup, number=N))
# p(timeit.timeit('if c[99]: x += 1', setup=setup, number=N))
