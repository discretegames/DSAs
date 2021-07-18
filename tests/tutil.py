""""Utility methods for tests."""

import os
import sys
import random
# Appending src lets test files be run in the VSCode debugger for quick testing.
sys.path.append(f'{os.path.dirname(__file__)}/../src')


def random_arr(min_length, max_length, min_value, max_value):
    length = random.randint(min_length, max_length)
    return [random.randint(min_value, max_value) for _ in range(length)]
