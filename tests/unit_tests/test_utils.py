"""Unit test module for the utility functions."""

# Third party imports
import numpy as np

# Local application imports
from utils import np_array_to_tuple


class TestArrayToTuple:
    def test_np_array_to_tuple_one_d(self):
        expected_tuple = (1, 2)
        array = np.array([1, 2])
        assert np_array_to_tuple(array) == expected_tuple

    def test_np_array_to_tuple_two_d(self):
        expected_tuple = ((1, 2), (3, 4))
        array = np.array([[1, 2], [3, 4]])
        assert np_array_to_tuple(array) == expected_tuple

    def test_np_array_to_tuple_four_d(self):
        expected_tuple = ((((1, 2), (3, 4)), ((5, 6), (7, 8))),  # 3d
                          (((9, 10), (11, 12)), ((13, 14), (15, 16))))  # 4d
        array = np.array([[[[1, 2], [3, 4]], [[5, 6], [7, 8]]],
                         [[[9, 10], [11, 12]], [[13, 14], [15, 16]]]])
        assert np_array_to_tuple(array) == expected_tuple
