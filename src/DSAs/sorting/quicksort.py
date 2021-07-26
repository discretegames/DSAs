import random
from DSAs.sorting.util import swap, key_and_reverse, default_left_right


def random_pivot(arr, left=None, right=None):
    left, right = default_left_right(arr, left, right)
    return random.randint(left, right)


def partition(arr, left, right, pivot):  # Unstable.
    swap(arr, left, pivot)  # Keep pivot value at left until the end.
    swap_index = left + 1
    for i in range(left + 1, right + 1):
        if arr[i] < arr[left]:
            swap(arr, i, swap_index)
            swap_index += 1
    swap(arr, left, swap_index - 1)  # Put pivot value in its place.
    return swap_index - 1


@key_and_reverse()
def quicksort(arr, left=None, right=None, pivot_chooser=random_pivot):
    """Quicksort. Unstable. In place. O(NlogN) time on average. O(logN) extra space."""
    left, right = default_left_right(arr, left, right)
    if left < right:
        pivot = pivot_chooser(arr, left, right)
        pivot = partition(arr, left, right, pivot)
        quicksort(arr, left, pivot - 1, pivot_chooser)
        quicksort(arr, pivot + 1, right, pivot_chooser)


def partition3(arr, pivot):  # Stable.
    less, equal, greater = [], [], []
    for value in arr:
        if value < arr[pivot]:
            less.append(value)
        elif value > arr[pivot]:
            greater.append(value)
        else:
            equal.append(value)
    return less, equal, greater


@key_and_reverse(False)
def quicksort_basic(arr, pivot_chooser=random_pivot):
    """Basic quicksort that uses more memory. Stable. Not in place. O(NlogN) time on average. O(NlogN) extra space."""
    if len(arr) <= 1:
        return arr.copy()
    pivot = pivot_chooser(arr)
    less, equal, greater = partition3(arr, pivot)
    return quicksort_basic(less, pivot_chooser) + equal + quicksort_basic(greater, pivot_chooser)
