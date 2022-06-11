"""Utility functions used in various places across the application."""

# Standard library imports
from typing import Tuple

# Third party imports
import numpy as np


def np_array_to_tuple(arr: np.ndarray | Tuple) -> Tuple | np.ndarray:
    """Utility function to convert an n-dimensional np.ndarray into a Tuple (for hashability)"""
    try:
        return tuple(np_array_to_tuple(element) for element in arr)
    except TypeError:  # Recursion has exhausted all dimensions
        return arr
