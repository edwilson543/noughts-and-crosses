"""
Module to define different decorators that can be used for caching the win search, with the aim of finding the
best one that speeds it up.
"""

# Standard library imports
from typing import Tuple, List
from functools import lru_cache, wraps
from collections import OrderedDict

# Third party imports
import numpy as np


##########
# Option 1 - a custom class decorator implementing a lru_cache
##########
class LRUCacheWinSearch:
    """
    Class to implement a tailor made lru cache for the win search method.
    The idea is to only include the playing_grid and get_win_locations arguments as keys in the hash, as these are the
    only arguments that affect the return value. In particular, the last_played_index does NOT affect the return value.
    """

    def __init__(self,
                 win_search_func,
                 maxsize: int = None):
        self.win_search_func = win_search_func
        self.cache_maxsize = maxsize
        self.cache = OrderedDict({})

    def __call__(self, maxsize: int = None, *args, **kwargs):
        if self.cache_maxsize is None:
            return self._get_search_return_value(*args, **kwargs)
        elif isinstance(maxsize, int) and maxsize > 0:
            def wrapper(*wrapper_args, **wrapper_kwargs):
                self.cache_maxsize = maxsize  # This is then used in the _cache_return_value method
                return self._get_search_return_value(*args, **kwargs)
            return wrapper
        else:
            raise ValueError(f"Invalid maxsize for the LRUCacheWinSearch of {maxsize} passed in the constructor.")

    def _get_search_return_value(self, *args, **kwargs) -> (bool, List[Tuple[int]]):
        """
        Method to retrieve a value from the cache if available, or call the search function and then cache the
        return if it is not available.
        Returns: Equivalent to the win_check_and_location_search method
        """
        hash_key = self._create_hash_key_from_kwargs(*args, **kwargs)
        if hash_key in self.cache:
            self.cache.move_to_end(hash_key)  # Now the most recently used
            return self.cache[hash_key]
        else:
            search_return_value = self.win_search_func(*args, **kwargs)
            self._cache_return_value(hash_key=hash_key, return_value=search_return_value)
            return search_return_value

    def _cache_return_value(self, hash_key: Tuple[Tuple, bool], return_value: (bool, List[Tuple[int]])) -> None:
        """
        Method to cache the passed return_value with the passed hash_key, and if the maximum size of the cache
        is exceeded, remove the least recently used item. Note that return_value becomes the most recently used item.
        """
        self.cache[hash_key] = return_value
        self.cache.move_to_end(key=hash_key)  # Now the most recently used
        if self.cache_maxsize is not None and len(self.cache) > self.cache_maxsize:
            self.cache.popitem(last=False)  # last=False specifies the LRU item in this case

    @staticmethod
    def _create_hash_key_from_kwargs(*args, **kwargs) -> Tuple[Tuple, bool]:
        """
        Method to get the kwargs that we want to use as keys for the cache, make them hashable, and generate one
        key we want to use for the cache.
        The flexibility to define this method is the core reason for defining a custom class to implement a lru_cache
        rather than just using the built-in functools lru_cache decorator.
        Note that the get_win_location is included in the tuple so that we can still get a unique return value depending
        on whether get_win_location is set to True or False - otherwise when using minimax in the GUI the cache would
        return no win location, as minimax uses get_win_location=False and GUI uses get_win_location=True.
        """
        if "playing_grid" in kwargs and "get_win_location" in kwargs:
            playing_grid: np.ndarray = kwargs["playing_grid"]
            get_win_location: bool = kwargs["get_win_location"]
            playing_grid_tuple: tuple = np_array_to_tuple(arr=playing_grid)
            return playing_grid_tuple, get_win_location
        else:
            raise KeyError("Attempted to create a hashable cache key for the win search cache in method: "
                           "_create_hashable_cache_key_from_kwargs\n."
                           "However, the kwargs did not contain either a playing_grid or a get_win_location kwarg.\n"
                           f"args: {args}, kwargs: {kwargs}.")


##########
# Option 2 - a modified version of the built-in functools lru_cache
##########
def lru_cache_hashable(maxsize: int):
    """
    Decorator that can be used to cache functions taking numpy arrays as argument.
    The standard lru_cache only works on functions with hashable arguments and returns (cache entries are stored in a
    dict). The decorator therefore:
    1) When the function is called, converts any numpy arrays to tuples (lru_cache_hashable_wrapper) by modifying
    *args and **kwargs. *args and **kwargs are now hashable
    2) Calls another function (cached_wrapper) using these *args and **kwargs which is itself cached. The cached_wrapper
    just converts back any tuples to np.arrays and calls the decorated function.

    Parameters: cache_maxsize (maintained from the lru_cache decorator)
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
            return cached_wrapper(*hashable_args, **hashable_kwargs)

        # copy lru_cache attributes over too
        lru_cache_hashable_wrapper.cache_info = cached_wrapper.cache_info
        lru_cache_hashable_wrapper.cache_clear = cached_wrapper.cache_clear

        return lru_cache_hashable_wrapper

    return lru_cache_hashable_decorator


def np_array_to_tuple(arr: np.ndarray | Tuple) -> Tuple| np.ndarray:
    """Utility function to convert an n-dimensional np.ndarray into a Tuple (for hashability)"""
    try:
        return tuple(np_array_to_tuple(element) for element in arr)
    except TypeError:  # Recursion has exhausted all dimensions
        return arr

