"""
Module to define different decorators that can be used for caching the win search, with the aim of finding the
best one that speeds it up.
"""

# Standard library imports
from typing import Tuple, List
from functools import lru_cache, update_wrapper, wraps
from collections import OrderedDict

# Third party imports
import numpy as np


##########
# Option 1 - a custom class decorator implementing a lru_cache
##########
class LRUCacheWinSearch:
    """
    Decorator class to implement a tailor made lru cache for the win search method.
    The idea is to only include the playing_grid and get_win_locations arguments in the hash keys of the cache, as these
    are the only arguments that affect the return value. In particular, the last_played_index does NOT affect the return
    value.
    Challenge therefore is to cache the search function based only on a chosen subset of its kwargs, and also to make
    these arguments hashable as they are implemented as numpy arrays.

    Decorator parameters:
    ----------
    hash_key_kwargs: a set of the keys joined in a tuple that the hash key should be created out of (REQUIRED)
    maxsize: the maximum number of return values of the decorated function stored in the cache (OPTIONAL, defaults
    to infinity in effect.)
    """

    def __init__(self,
                 hash_key_kwargs: set,
                 maxsize: int = None,
                 win_search_func=None):
        self.hash_key_kwargs = hash_key_kwargs
        self.cache_maxsize = maxsize
        self.win_search_func = win_search_func
        self.cache = OrderedDict({})
        if win_search_func is not None:
            update_wrapper(self, win_search_func)

    def __call__(self, win_search_func=None, *args, **kwargs):
        """
        Because this is a decorator class, we need to make it callable.
        Due to the decorator arguments, we need the if/elif below, rather than just to always return the search_return.
        The if executes in the case where a maxsize argument has been passed to the decorator and therefore an instance
        of the class has already been created, at the point at which we call the decorator on the search function. This
        returns an instance of the class (which as a decorator in effect replaces the search function), and because it
        now has a self.win_search_func, when called the second elif will be True.
        The second elif essentially reflects the normal calling of the win check and location search, but with the
        added functionality of caching.
        """
        if win_search_func is not None and self.win_search_func is None:
            self.win_search_func = win_search_func
            return self
        elif win_search_func is None and self.win_search_func is not None:
            return self._get_search_return_value(*args, **kwargs)

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

    # @staticmethod
    def _create_hash_key_from_kwargs(self, *args, **kwargs) -> Tuple:
        """
        Method to get the kwargs that we want to use as keys for the cache, make them hashable, and generate one
        key we want to use for the cache.
        The flexibility to define this method is the core reason for defining a custom class to implement a lru_cache
        rather than just using the built-in functools lru_cache decorator.
        Note that the get_win_location is included in the tuple so that we can still get a unique return value depending
        on whether get_win_location is set to True or False - otherwise when using minimax in the GUI the cache would
        return no win location, as minimax uses get_win_location=False and GUI uses get_win_location=True.
        """
        if self.hash_key_kwargs is not None:
            hash_key_tuple = tuple(np_array_to_tuple(kwargs[key_kwarg]) if
                             (key_kwarg in kwargs and key_kwarg in self.hash_key_kwargs) else
                             kwargs[key_kwarg] for key_kwarg in self.hash_key_kwargs)
            return hash_key_tuple
        else:
            raise KeyError("No kwargs were specified to construct the hash key for the lru cache from.")


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


def np_array_to_tuple(arr: np.ndarray | Tuple) -> Tuple | np.ndarray:
    """Utility function to convert an n-dimensional np.ndarray into a Tuple (for hashability)"""
    try:
        return tuple(np_array_to_tuple(element) for element in arr)
    except TypeError:  # Recursion has exhausted all dimensions
        return arr
