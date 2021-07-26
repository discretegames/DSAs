from DSAs.sorting.util import key_and_reverse, default_left_right


def merge_in_place(arr, left, middle, right):
    merged = []
    i1, i2 = left, middle + 1
    while i1 <= middle and i2 <= right:
        if arr[i1] <= arr[i2]:
            merged.append(arr[i1])
            i1 += 1
        else:
            merged.append(arr[i2])
            i2 += 1
    merged.extend(arr[i1:middle + 1])
    merged.extend(arr[i2:right + 1])
    arr[left:right + 1] = merged


@key_and_reverse()
def mergesort(arr, left=None, right=None):
    """Recursive merge sort from left to right indices inclusive. Stable. In place. O(NlogN) time. O(NlogN) extra space."""
    left, right = default_left_right(arr, left, right)
    if right <= left:
        return arr.copy()
    middle = (left + right) // 2  # or left + (right - left) // 2 to avoid overflow
    mergesort(arr, left, middle)
    mergesort(arr, middle + 1, right)
    merge_in_place(arr, left, middle, right)


def merge(arr1, arr2):
    merged = []
    i1, i2 = 0, 0
    while i1 < len(arr1) and i2 < len(arr2):
        if arr1[i1] <= arr2[i2]:
            merged.append(arr1[i1])
            i1 += 1
        else:
            merged.append(arr2[i2])
            i2 += 1
    merged.extend(arr1[i1:])
    merged.extend(arr2[i2:])
    return merged


@key_and_reverse(False)
def mergesort_basic(arr):
    """Basic mergesort that doesn't use indices. Stable. Not in place. O(NlogN) time. O(NlogN) extra space."""
    if len(arr) <= 1:
        return arr
    middle = len(arr) // 2
    left_arr = mergesort_basic(arr[:middle])
    right_arr = mergesort_basic(arr[middle:])
    return merge(left_arr, right_arr)
