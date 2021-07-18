"""Miscellaneous scratch and test area."""


def selectionsort(arr):
    """Selection sort. In place. Unstable. O(N^2) time. O(1) space."""
    for i in range(len(arr)):
        rest =
        min_index = min(range(len(arr)), key=arr.__getitem__)
        arr[i], arr[min_index] = arr[min_index], arr[i]


# def selectionsort(lst):
#     for i in range(len(lst)):
#         j, _ = min(enumerate(lst[i:]), key=lambda t: t[1])
#         lst[i], lst[j + i] = lst[j + i], lst[i]


a = [1, 2]
selectionsort(a)
print(a)


a = [2, 1]
selectionsort(a)
print(a)
