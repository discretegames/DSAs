"""Utility methods and classes for sorting."""

from functools import total_ordering, wraps


def swap(arr, i, j):
    """Swaps the values in arr at indices i and j."""
    arr[i], arr[j] = arr[j], arr[i]


@total_ordering
class Sortable:
    """Helper class for key_and_reverse that represents an object to be sorted."""

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


# Decorated order of key_and_reverse and stabilize doesn't matter.
def key_and_reverse(in_place=True):
    """Factory for decorator that adds key and reverse args to a sorting algorithm that may be in-place or not."""
    def decorator(sorting_algorithm):
        """Decorator that adds key and reverse keyword args to a sorting algorithm."""
        @wraps(sorting_algorithm)
        def wrapper(arr, *args, key=None, reverse=False, **kwargs):
            to_sort = [Sortable(value, key, reverse) for value in arr]
            result = sorting_algorithm(to_sort, *args, **kwargs)
            if in_place:
                arr[:] = [sortable.value for sortable in to_sort]
                return result
            return [sortable.value for sortable in result]
        return wrapper
    return decorator


def stabilize(in_place=True):
    """Factory for decorator that makes a sorting algorithm, which may be in-place or not, stable."""
    def decorator(sorting_algorithm):
        """Decorator that makes a sorting algorithm stable."""
        @wraps(sorting_algorithm)
        def wrapper(arr, *args, **kwargs):
            if 'key' in kwargs:  # Patch in proper key that takes index into account.
                key = kwargs['key']
                kwargs['key'] = lambda x: (key(x[0]), x[1])
            to_sort = [(value, i) for i, value in enumerate(arr)]
            result = sorting_algorithm(to_sort, *args, **kwargs)
            if in_place:
                arr[:] = [value for value, _ in to_sort]
                return result
            return [value for value, _ in result]
        return wrapper
    return decorator


def in_place(sorting_algorithm):
    """Decorator that turns non-in-place sorting algorithm into an in-place one."""
    @wraps(sorting_algorithm)
    def wrapper(arr, *args, **kwargs):
        arr[:] = sorting_algorithm(arr, *args, **kwargs)
    return wrapper


def not_in_place(sorting_algorithm):
    """Decorator that turns an in-place sorting algorithm into an non-in-place one. Return values are lost."""
    @wraps(sorting_algorithm)
    def wrapper(arr, *args, **kwargs):
        copy = arr.copy()
        sorting_algorithm(copy, *args, **kwargs)
        return copy
    return wrapper