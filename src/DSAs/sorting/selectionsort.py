from DSAs.sorting.sorting_util import swap, key_and_reverse


@key_and_reverse()
def selectionsort(arr):
    """Selection sort. In place. Unstable. O(N^2) time. O(1) space."""
    for i in range(len(arr)):
        min_index = i + min(range(len(arr) - i), key=arr[i:].__getitem__)
        swap(arr, i, min_index)
