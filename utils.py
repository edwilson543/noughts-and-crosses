"""Utility functions used in various places across the application."""

# Standard library imports
from typing import Tuple, Set

# Third party imports
import numpy as np
from numba import jit


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

# @jit  # TODO profile code with this on/off
def get_symmetry_set_of_tuples_from_array(array: np.ndarray) -> Set[Tuple]:
    """
    Method to get the arrays that are rotationally and reflectively symmetric to the passed array, and then convert
    this into a set of tuples. Note that this function only works in 2D i.e. for matrices (although could be easily
    extended, currently not for performance). This could use a recursion along the lines of the search directions
    method.
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
