from functools import total_ordering, wraps


def swap(arr, i, j):
    arr[i], arr[j] = arr[j], arr[i]


@total_ordering
class Sortable:
    def __init__(self, value, key, reverse):
        self.value = value
        self.key = value if key is None else key(value)
        self.reverse = reverse

    def __eq__(self, other):
        return self.key == other.key

    def __lt__(self, other):
        if self.reverse:
            return self.key > other.key
        else:
            return self.key < other.key

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.value}, {self.key})"


def key_and_reverse(in_place=True):
    def decorator(sorter):
        @wraps(sorter)
        def wrapper(arr, *args, key=None, reverse=False, **kwargs):
            sortables = [Sortable(value, key, reverse) for value in arr]
            result = sorter(sortables, *args, **kwargs)
            if in_place:
                for i, sortable in enumerate(sortables):
                    arr[i] = sortable.value
                return result
            return [sortable.value for sortable in result]
        return wrapper
    return decorator
