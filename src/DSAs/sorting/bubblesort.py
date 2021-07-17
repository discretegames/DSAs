from DSAs.sorting.sortutil import swap, getkey


def bubblesort(arr, key=None):  # In place. Stable.
    key = getkey(key)
    for i in range(len(arr)):
        for j in range(len(arr) - i - 1):
            if key(arr[j]) > key(arr[j + 1]):
                swap(arr, i, j)
