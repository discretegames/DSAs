def pigeonholesort(arr, key=None, reverse=False):
    """Pigeonhole sort. Stable. In place. O(N + range) time. O(N + range) space.

    Pigeonhole sort, similar to counting sort, is not a comparison sort.
    If key is None, arr should only contain integers. If key is not None it must
    be a function that returns an integer over the possible range of key values.
    """
    if not arr:
        return

    keys = [key(value) for value in arr] if key else arr
    if reverse:
        keys = [-k for k in keys]

    offset = min(keys)
    holes = [[] for _ in range(max(keys) - offset + 1)]
    for k, value in zip(keys, arr):
        holes[k - offset].append(value)

    insert = 0
    for hole in holes:
        for value in hole:
            arr[insert] = value
            insert += 1
