"""Utility functions used in various places across the application."""

# Standard library imports
from functools import lru_cache, wraps
from typing import Tuple, Set

# Third party imports
import numpy as np


def np_array_to_tuple(array: np.ndarray | Tuple, remaining_dimensions: int = None) -> Tuple:
    """
    Utility function to convert an n-dimensional np.ndarray into a Tuple (for hashability).
    Note that this is a n-dimensional function
    """
    if remaining_dimensions is None:  # This is the first call
        remaining_dimensions = np.ndim(array)
    if remaining_dimensions == 0:  # Recursion has exhausted all dimensions
        return array
    else:
        return tuple(np_array_to_tuple(subarray, remaining_dimensions - 1) for subarray in array)


# Have ruled out using @jit here by profiling with/without
def get_symmetry_set_of_tuples_from_array(array: np.ndarray) -> Set[Tuple]:
    """
    Method to get the arrays that are rotationally and reflectively symmetric to the passed array, and then convert
    this into a set of tuples. Note that this function only works in 2D i.e. for matrices (although could be easily
    extended, currently not for performance). This could use a recursion along the lines of the search directions
    method.
    Note that a set is used so that we only get the unique tuples.
    """
    if np.ndim(array) != 2:
        raise ValueError(f"Attempted to generate a symmetry set for array: {array} that is not 2-dimensional, "
                         "using the get_array_symmetry_set_of_tuples, which is only implemented for 2D arrays.")

    # Symmetries relevant to matrices not necessarily square
    horizontal_reflection_tuple = np_array_to_tuple(np.flipud(array))
    vertical_reflection_tuple = np_array_to_tuple(np.fliplr(array))
    rot_180_tuple = np_array_to_tuple(np.rot90(array, k=2))

    # Create the symmetry set now so can add most elements in one go
    symmetry_set = {np_array_to_tuple(array=array), horizontal_reflection_tuple,
                    vertical_reflection_tuple, rot_180_tuple}

    # Symmetries only valid for square matrices
    if array.shape[0] == array.shape[1]:
        south_east_reflection_tuple = np_array_to_tuple(np.transpose(array))
        south_west_reflection_tuple = np_array_to_tuple(np.transpose(np.rot90(array, k=2)))

        rot_90_tuple = np_array_to_tuple(np.rot90(array))
        rot_270_tuple = np_array_to_tuple(np.rot90(array, k=3))

        symmetry_set.update([south_east_reflection_tuple, south_west_reflection_tuple, rot_90_tuple, rot_270_tuple])

    return symmetry_set


##########
# A modified version of the built-in functools lru_cache, which allows for hashable arguments
##########
def lru_cache_hashable(_func=None, maxsize: int = None):
    """
    Decorator that can be used to cache functions taking numpy arrays as argument.
    The standard lru_cache only works on functions with hashable arguments and returns (cache entries are stored in a
    dict). The decorator therefore:
    1) When the function is called, converts any numpy arrays to tuples (lru_cache_hashable_wrapper) by modifying
    *args and **kwargs. *args and **kwargs are now hashable
    2) Calls another function (cached_wrapper) using these *args and **kwargs which is itself cached. The cached_wrapper
    just converts back any tuples to np.arrays and calls the decorated function.

    Parameters:
    _funcs: The decorated function in the case that maxsize is None, otherwise is not used
    maxsize (maintained from the lru_cache decorator)

    Note the major downside of this cache is it creates unique cache entries for calls to the search function which
    only differ by the last_played_index.
    """

    def lru_cache_hashable_decorator(func, *args, **kwargs):
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

    if maxsize is not None:
        return lru_cache_hashable_decorator
    else:  # We need to call the first inner function
        return lru_cache_hashable_decorator(_func)
