def pigeonholesort(arr, key=None, reverse=False):
    """Pigeonhole sort. Stable. In place. O(N + range) time. O(N + range) space."""
    if not arr:
        return
    keys = arr if key is None else list(map(key, arr))

    if reverse:
        keys = [-k for k in keys]

    offset = min(keys)
    holes = [[] for _ in range(max(keys) - offset + 1)]
    for k, value in zip(keys, arr):
        holes[k - offset].append(value)

    i = 0
    for hole in holes:
        for value in hole:
            arr[i] = value
            i += 1
