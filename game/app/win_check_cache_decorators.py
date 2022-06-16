"""
Module to define different decorators that can be used for caching the win search, with the aim of finding the
best one that speeds it up.
"""

# Standard library imports
from collections import OrderedDict
from functools import update_wrapper
from typing import Tuple, List, Callable, Set, Union

# Third party imports
import numpy as np

# Local application imports
from utils import np_array_to_tuple, get_symmetry_set_of_tuples_from_array


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
                 use_symmetry: bool = False):
        self.hash_key_kwargs = hash_key_kwargs
        self.cache_maxsize = maxsize
        self.use_symmetry = use_symmetry
        self.win_search_func: Union[None, Callable] = None  # PyCharm linter doesn't like None | Callable
        self.cache: OrderedDict = OrderedDict({})

    def __call__(self, win_search_func: Callable = None, *args, **kwargs):
        """
        Because this is a decorator class, we need to make it callable.
        Due to the decorator arguments, we need the if/elif below, rather than just to always return the search_return.
        The if executes in the case where a maxsize argument has been passed to the decorator and therefore an instance
        of the class has already been created, at the point at which we call the decorator on the search function. This
        returns an instance of the class (which as a decorator in effect replaces the search function), and because it
        now has a self.win_search_func, when called the second elif will be True.
        The second elif essentially reflects the normal calling of the win check and location search, but with the
        added functionality of caching.

        Parameters:
        win_search_func: The function we are decorating (present as an arg for the if but not the elif)
        *args/**kwargs: The args/kwargs of the search function (present for the elif but not the if)
        """
        if win_search_func is not None and self.win_search_func is None:
            self.win_search_func = win_search_func
            update_wrapper(self, win_search_func)
            return self
        elif win_search_func is None and self.win_search_func is not None:
            return self._get_search_return_value(*args, **kwargs)

    def _get_search_return_value(self, *args, **kwargs) -> Tuple[bool, List[Tuple[int]] | None]:
        """
        Method to retrieve a value from the cache if available, or call the search function and then cache the
        return if it is not available.
        Note that if self.use_symmetry is set to True, then all arrays symmetrically equivalent to the
        passed playing grid are automatically cached against the same return value, when "get_win_location" is not True,
        otherwise using symmetry is invalid.

        Parameters/Returns: As for the win_check_and_location_search method
        """
        hash_key = self._create_hash_key_from_kwargs(*args, **kwargs)
        if hash_key in self.cache:
            self.cache.move_to_end(hash_key)  # Now the most recently used
            return self.cache[hash_key]
        else:  # Must directly call function and cache
            search_return_value = self.win_search_func(*args, **kwargs)
            if self.use_symmetry and not kwargs["get_win_location"]:
                # note the not kwargs["get_win_location"] is to avoid symmetry returning the wrong win location
                hash_key_list = self._create_hash_key_list_for_symmetry_set_from_kwargs(*args, **kwargs)
                for symm_hash_key in hash_key_list:
                    self._cache_return_value(hash_key=symm_hash_key, return_value=search_return_value)
            else:
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
                                   isinstance(kwargs[key_kwarg], np.ndarray) else
                                   kwargs[key_kwarg] for key_kwarg in self.hash_key_kwargs)
            return hash_key_tuple
        else:
            raise KeyError("No kwargs were specified to construct the hash key for the lru cache from.")

    def _create_hash_key_list_for_symmetry_set_from_kwargs(self, *args, **kwargs) -> List[Tuple]:
        """
        Method to create a list of hash keys from kwargs for each tuple in the symmetry set of a given playing grid.
        These can then be used to cache all of these different tuples against the same return value.

        Returns: A list of hash_keys based on the hash_key_kwargs instance attribute.
        """
        if "playing_grid" not in kwargs:
            raise KeyError("Attempted to call _create_list_of_hash_keys_from_kwargs with kwargs that do not"
                           f"include 'playing_grid'. kwargs: {kwargs}")
        if "get_win_location" not in kwargs:
            raise KeyError("Attempted to call _create_list_of_hash_keys_from_kwargs with kwargs that do not"
                           f"include 'get_win_location'. kwargs: {kwargs}")
        else:
            playing_grid: np.ndarray = kwargs["playing_grid"]
            symmetry_set: Set[Tuple] = get_symmetry_set_of_tuples_from_array(array=playing_grid)
            hash_key_list = []
            for symmetric_tup in symmetry_set:
                kwargs["playing_grid"] = symmetric_tup
                hash_key = self._create_hash_key_from_kwargs(*args, **kwargs)
                hash_key_list.append(hash_key)
            return hash_key_list
