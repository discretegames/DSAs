from DSAs.sorting import swap, key_and_reverse


@key_and_reverse()
def insertionsort(arr):
    """Insertion sort. Stable. In place. O(N^2) time. O(1) space."""
    for i in range(1, len(arr)):
        while i and arr[i] < arr[i - 1]:
            swap(arr, i, i - 1)
            i -= 1
