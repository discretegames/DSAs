import random


def random_arr(min_length, max_length, min_value, max_value):
    length = random.randint(min_length, max_length)
    return [random.randint(min_value, max_value) for _ in range(length)]
