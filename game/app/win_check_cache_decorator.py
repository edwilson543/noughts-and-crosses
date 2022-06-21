"""
Module to define the decorator that is used for caching the win search.
"""

# Standard library imports
from collections import OrderedDict
from enum import Enum
from functools import update_wrapper
from typing import Tuple, List, Callable, Set, Union

# Third party imports
import numpy as np

# Local application imports
from utils import np_array_to_tuple, get_symmetry_set_of_tuples_from_array


class WinSearchKwarg(Enum):
    PLAYING_GRID = "playing_grid"
    GET_WIN_LOCATION = "get_win_location"


class LRUCacheWinSearch:
    """
    (Callable) decorator class to implement a tailor made lru cache for the win search method above.
    The idea is to only include the playing_grid and get_win_locations arguments in the hash keys of the cache, as these
    are the only arguments that affect the return value. In particular, the last_played_index does NOT affect the return
    value.
    Challenge therefore is to cache the search function based only on a chosen subset of its kwargs, and also to make
    these arguments hashable as they are implemented as numpy arrays.

    Decorator parameters:
    ----------
    maxsize: the maximum number of return values of the decorated function stored in the cache (OPTIONAL, defaults
    to infinity in effect)
    use_symmetry: True means that each time the win search is called, we also cache it's symmetric equivalence class,
    (OPTIONAL, defaults to False)
    """

    def __init__(self,
                 maxsize: int = None,
                 use_symmetry: bool = False):
        self.cache_maxsize = maxsize
        self.use_symmetry = use_symmetry
        self.win_search_func: Union[None, Callable] = None  # PyCharm linter doesn't like None | Callable
        self.cache: OrderedDict = OrderedDict({})

    def __call__(self, win_search_func: Callable = None, *args, **kwargs):
        """
        Because this is a decorator class, we need to make it callable by implementing __call__.

        Due to the decorator arguments, we need the if/elif below, rather than just to always return the search_return.
        The if executes at the first call when the decorator parameters have just been passed. An instance of the
        class has thus already been created at the point at which we decorate the search function.

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
            if self.use_symmetry and not kwargs[WinSearchKwarg.GET_WIN_LOCATION.value]:
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

    @staticmethod
    def _create_hash_key_from_kwargs(*args, **kwargs) -> Tuple:
        """
        Method to get the kwargs that we want to use as keys for the cache, make them hashable, and generate a key
        to use for the cache.
        The flexibility to define this method is the core reason for defining a custom class to implement a lru_cache
        rather than just using the built-in functools lru_cache decorator.
        Note that get_win_location is included in the tuple so that we can still get a unique return value depending
        on whether get_win_location is set to True or False - otherwise when using minimax in the GUI the cache would
        return no win location, as minimax uses get_win_location=False and GUI uses get_win_location=True.

        Returns: the hash key that will correspond to the call to the search function using *args and **kwargs.
        """
        try:
            playing_grid = kwargs[WinSearchKwarg.PLAYING_GRID.value]
            get_win_location = kwargs[WinSearchKwarg.GET_WIN_LOCATION.value]
        except KeyError:
            raise KeyError("Attempted to call _create_hash_keys_from_kwargs with kwargs that do not"
                           f"include {WinSearchKwarg.PLAYING_GRID.value} or "
                           f"{WinSearchKwarg.GET_WIN_LOCATION.value}. kwargs: {kwargs}")

        if isinstance(playing_grid, np.ndarray):
            hash_key_tuple = tuple((np_array_to_tuple(playing_grid), get_win_location))
            return hash_key_tuple
        else:
            hash_key_tuple = tuple((playing_grid, get_win_location))
            return hash_key_tuple

    @classmethod
    def _create_hash_key_list_for_symmetry_set_from_kwargs(cls, *args, **kwargs) -> List[Tuple]:
        """
        Method to create a list of hash keys from kwargs for each tuple in the symmetry set of a given playing grid.
        These can then be used to cache all of these different tuples against the same return value.

        Returns: A list of hash keys - one for each tuple in the symmetry set.
        """
        if WinSearchKwarg.PLAYING_GRID.value not in kwargs:
            raise KeyError("Attempted to call _create_hash_key_list_for_symmetry_set_from_kwargs with kwargs that do "
                           f"not include {WinSearchKwarg.PLAYING_GRID.value}. kwargs: {kwargs}")
        if WinSearchKwarg.GET_WIN_LOCATION.value not in kwargs:
            raise KeyError("Attempted to call _create_hash_key_list_for_symmetry_set_from_kwargs with kwargs that do "
                           f"not include {WinSearchKwarg.GET_WIN_LOCATION.value}. kwargs: {kwargs}")
        else:
            playing_grid: np.ndarray = kwargs[WinSearchKwarg.PLAYING_GRID.value]
            symmetry_set: Set[Tuple] = get_symmetry_set_of_tuples_from_array(array=playing_grid)
            hash_key_list = [cls._create_hash_key_for_symmetric_equivalent_tuple(symmetric_tuple, *args, **kwargs) for
                             symmetric_tuple in symmetry_set]
            return hash_key_list

    @classmethod
    def _create_hash_key_for_symmetric_equivalent_tuple(cls, symmetric_tuple: Tuple, *args, **kwargs) -> Tuple:
        """
        Method to create a hash key for a tuple that is symmetrically equivalent to the playing grid - the
        playing_grid is extracted from the kwargs and then replaced with the symmetric_tuple, before creating the
        hash key.
        """
        # replace the playing grid in kwargs with the symmetric equivalent
        kwargs[WinSearchKwarg.PLAYING_GRID.value] = symmetric_tuple
        hash_key = cls._create_hash_key_from_kwargs(*args, **kwargs)
        return hash_key
