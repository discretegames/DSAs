from DSAs.sorting import swap, key_and_reverse


@key_and_reverse()
def shellsort(arr, gaps=None):
    """Shell sort. Stable. In place. O(N^2) time (varies). O(1) space besides gaps.

    A generalization of insertion sort where the swaps are decreasing gap sizes apart.
    The optional argument gaps should be a decreasing list of ints ending with 1.
    By default gaps is [N//2, N//4, N//8, ..., 1].
    Time and space complexities depend on gaps. See wiki: wikipedia.org/wiki/Shellsort
    """
    if gaps is None:
        gaps = []
        n = len(arr) // 2
        while n:
            gaps.append(n)
            n //= 2
    for gap in gaps:
        for i in range(gap, len(arr)):
            while i >= gap and arr[i] < arr[i - gap]:
                swap(arr, i, i - gap)
                i -= gap
