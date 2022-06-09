"""
Module to define different decorators that can be used for caching the win search, with the aim of finding the
best one that speeds it up.
"""

# Standard library imports
from typing import Tuple
from functools import lru_cache, wraps

# Third party imports
import numpy as np


def np_array_to_tuple(array: np.ndarray) -> Tuple:
    tuple_array = array.copy()
    for _ in range(0, array.ndim):
        tuple_array = tuple(tuple_array)
    return tuple_array


def lru_cache_hashable(maxsize: int):
    """
    Decorator that can be used to cache functions taking numpy arrays as argument.
    The standard lru_cache only works on functions with hashable arguments and returns (cache entries are stored in a
    dict). The decorator therefore:
    1) When the function is called, converts any numpy arrays to tuples (lru_cache_hashable_wrapper) by modifying
    *args and **kwargs. *args and **kwargs are now hashable
    2) Calls another function (cached_wrapper) using these *args and **kwargs which is itself cached. The cached_wrapper
    just converts back any tuples to np.arrays and calls the decorated function.

    Parameters: maxsize (maintained from the lru_cache decorator)
    """
    def lru_cache_hashable_decorator(func):
        @lru_cache(maxsize=maxsize)
        def cached_wrapper(*hashable_args,
                           **hashable_kwargs):  # the lru_cache only works on functions with hashable args and returns
            unhashable_args = tuple(np.array(arg) if type(arg) == tuple else arg for arg in hashable_args)
            unhashable_kwargs = {key: np.array(kwarg) if type(kwarg) == tuple else kwarg for key, kwarg in
                                 hashable_kwargs.items()}
            return func(*unhashable_args, **unhashable_kwargs)

        @wraps(func)
        def lru_cache_hashable_wrapper(*unhashable_args, **unhashable_kwargs):
            hashable_args = tuple(np_array_to_tuple(arg) if type(arg) == np.ndarray else arg for arg in unhashable_args)
            hashable_kwargs = {key: np_array_to_tuple(kwarg) if type(kwarg) == np.ndarray else kwarg for key, kwarg in
                               unhashable_kwargs.items()}
            # print(hashable_kwargs)
            return cached_wrapper(*hashable_args, **hashable_kwargs)

        # copy lru_cache attributes over too
        lru_cache_hashable_wrapper.cache_info = cached_wrapper.cache_info
        lru_cache_hashable_wrapper.cache_clear = cached_wrapper.cache_clear
        print(lru_cache_hashable_wrapper.cache_info().hits)

        return lru_cache_hashable_wrapper

    return lru_cache_hashable_decorator

# from time import perf_counter_ns
#
# times = []
# for trial in range(0, 50):
#     start_time = perf_counter_ns()
#
#     x = 5
#     @lru_cache_hashable(maxsize=10)
#     def func_test(arr: np.ndarray, num: int, *args, **kwargs) -> np.ndarray:
#         print(f"args: {args}, kwargs: {kwargs}")
#         print("Cache not used")
#         return arr * arr + num *x
#
#     array = np.array([1, 2, 3])
#     print(func_test(arr=array, num=4))
#     print(func_test(arr=array, num=4))
#
#     end_time = perf_counter_ns()
#
#     time = end_time - start_time
#     times.append(time)
#
# print(f"Min duration (nano seconds): {min(times)}")
