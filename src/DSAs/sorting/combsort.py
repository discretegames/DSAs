from DSAs.sorting.util import swap, key_and_reverse, get_gaps


@key_and_reverse()
def combsort(arr, gaps=None, shrink_factor=1.3):
    """Comb sort. Unstable in general. In place. O(N^2) time (varies). O(1) space besides gaps.

    A generalization of bubble sort where the swaps are decreasing gap sizes apart.
    The optional argument gaps should be a decreasing list of ints ending with 1.
    By default gaps is [N//k^1, N//k^2, N//k^3, ..., 1] where k is shrink_factor.
    True time complexity depends on gaps.
    """
    if gaps is None:
        gaps = get_gaps(len(arr), shrink_factor)
    # for gap in gaps + [1, 1, 1]:
    #     for i in range(len(arr) - gap):
    #         if arr[i] > arr[i + gap]:
    #             swap(arr, i, i + gap)

    index = 0
    done = False
    while not done:
        gap = gaps[index]
        done = True
        for i in range(len(arr) - gap):
            if arr[i] > arr[i + gap]:
                swap(arr, i, i + gap)
                done = False
        i = max(len(arr) - 1, i + 1)
    # TODO something here is broken
