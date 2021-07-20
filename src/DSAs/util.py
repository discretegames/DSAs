"""Utility methods and classes for DSAs."""

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
        return f"{'R' * self.reverse}{self.__class__.__name__}({self.value}, {self.key})"


def key_and_reverse(in_place=True):
    def decorator(sorting_algorithm):
        @wraps(sorting_algorithm)
        def wrapper(arr, *args, key=None, reverse=False, **kwargs):
            sortables = [Sortable(value, key, reverse) for value in arr]
            result = sorting_algorithm(sortables, *args, **kwargs)
            if in_place:
                for i, sortable in enumerate(sortables):
                    arr[i] = sortable.value
                return result
            return [sortable.value for sortable in result]
        return wrapper
    return decorator


# Decorator order of key_and_reverse and stabilize doesn't matter.
def stabilize(in_place=True):
    def decorator(sorting_algorithm):
        @wraps(sorting_algorithm)
        def wrapper(arr, *args, **kwargs):
            enum_arr = [(value, i) for i, value in enumerate(arr)]
            if 'key' in kwargs:
                key = kwargs['key']
                kwargs['key'] = lambda x: (key(x[0]), x[1])
            result = sorting_algorithm(enum_arr, *args, **kwargs)
            if in_place:
                for i, (value, _) in enumerate(enum_arr):
                    arr[i] = value
                return result
            return [value for value, _ in result]
        return wrapper
    return decorator
