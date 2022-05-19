import numpy as np

# TODO
def check_for_horizontal_wint(self, playing_grid: np.array) -> bool:
    array_string_list = playing_grid.astype(str).to_list()
    list_joined_strings = ["".join(array_string_list) for row in array_string_list]
    if "1111" or "-1-1-1-1" in list_joined_strings:
        return True  # The row contains a winning row
    else:
        return False

def check_for_horizontal_win(self, playing_grid: np.array) -> bool:

    for row_index in range(0, self.game_rows_m):
        convoluted_array = np.convolve(playing_grid[row_index],
                                       np.ones(self.win_length_k, dtype=int),
                                       mode="same") # same key word prevents including first and last index
        max_consecutive = max(abs(convoluted_array))
        if max_consecutive == self.win_length_k:
            return True  # The row contains a winning row
        else:
            continue
    return False

arr = np.array([[1, 2, 3], [4, 5, 6]])
print(arr)
print(np.roll(arr, shift=(2, 1), axis=(1, 1)))