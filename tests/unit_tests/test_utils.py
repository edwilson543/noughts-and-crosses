"""Unit test module for the utility functions."""

# Third party imports
import numpy as np

# Local application imports
from utils import np_array_to_tuple, get_array_symmetry_set_of_tuples


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


class TestGetArraySymmetrySet:
    def test_get_array_symmetry_set_one_unique_tuples(self):
        playing_grid = np.array([
            [0, 0, 0],
            [0, 1, 0],
            [0, 0, 0]
        ])
        expected_symmetry_set = {((0, 0, 0), (0, 1, 0), (0, 0, 0))}
        actual_symmetry_set = get_array_symmetry_set_of_tuples(array=playing_grid)
        assert expected_symmetry_set == actual_symmetry_set

    def test_get_array_symmetry_set_four_unique_tuples(self):
        playing_grid = np.array([
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 0]
        ])
        expected_symmetry_set = {((1, 0, 0), (0, 1, 0), (0, 0, 0)),
                                 ((0, 0, 1), (0, 1, 0), (0, 0, 0)),
                                 ((0, 0, 0), (0, 1, 0), (1, 0, 0)),
                                 ((0, 0, 0), (0, 1, 0), (0, 0, 1))}
        actual_symmetry_set = get_array_symmetry_set_of_tuples(array=playing_grid)
        assert actual_symmetry_set == expected_symmetry_set

    def test_get_array_symmetry_set_eight_tuples(self):
        playing_grid = np.array([
            [1, 1, 0],
            [0, 0, 0],
            [0, 0, -1]
        ])
        expected_symmetry_set = {((1, 1, 0), (0, 0, 0), (0, 0, -1)),  # No transformation
                                 ((0, 0, -1), (0, 0, 0), (1, 1, 0)),  # Horizontal reflection
                                 ((0, 1, 1), (0, 0, 0), (-1, 0, 0)),  # Vertical reflection
                                 ((1, 0, 0), (1, 0, 0), (0, 0, -1)),  # South east reflection (transpose)
                                 ((-1, 0, 0), (0, 0, 1), (0, 0, 1)),  # South west reflection (anti-transpose)
                                 ((0, 0, 1), (0, 0, 1), (-1, 0, 0)),  # 90 degree rotation
                                 ((-1, 0, 0), (0, 0, 0), (0, 1, 1)),  # 180 degree rotation
                                 ((0, 0, -1), (1, 0, 0), (1, 0, 0)),  # 270 degree rotation
                                 }
        actual_symmetry_set = get_array_symmetry_set_of_tuples(array=playing_grid)
        assert actual_symmetry_set == expected_symmetry_set

    def test_non_square_symmetry_set_all_of_same_shape(self):
        """Test that none of the diagonal reflections and 90/270 degree rotations get applied to rectangular matrix."""
        playing_grid = np.array([
            [1, 1, 0, 0],
            [1, -1, 0, 0],
            [0, 0, 0, -1]
        ])
        symmetry_set = get_array_symmetry_set_of_tuples(playing_grid)
        for tup in symmetry_set:
            assert np.array(tup).shape == (3, 4)
