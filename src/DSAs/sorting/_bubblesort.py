from ..util import swap, getkey


def bubblesort(arr, key=None):
    """Bubble sort. In place. Stable. O(N^2) time. O(1) space."""
    key = getkey(key)
    for i in range(len(arr)):
        for j in range(len(arr) - i - 1):
            if key(arr[j]) > key(arr[j + 1]):
                swap(arr, j, j + 1)
