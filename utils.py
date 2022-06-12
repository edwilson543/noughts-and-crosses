"""Utility functions used in various places across the application."""

# Standard library imports
from typing import Tuple

# Third party imports
import numpy as np


def np_array_to_tuple(arr: np.ndarray | Tuple, remaining_dimensions: int = None) -> Tuple | np.ndarray:
    """Utility function to convert an n-dimensional np.ndarray into a Tuple (for hashability)"""
    if remaining_dimensions is None:  # This is the first call
        remaining_dimensions = np.ndim(arr)
    if remaining_dimensions == 0:  # Recursion has exhausted all dimensions
        return arr
    else:
        return tuple(np_array_to_tuple(element, remaining_dimensions - 1) for element in arr)
