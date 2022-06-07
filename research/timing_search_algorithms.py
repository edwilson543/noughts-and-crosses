import numpy as np
from time import perf_counter_ns


# TODO look into this - currently only some rough ideas noted down

def timer(func):
    def timer_wrapper(*args, **kwargs):
        time_trial = np.zeros(1000)
        for n in range(0, 1000):
            tick = perf_counter_ns()
            func(*args, **kwargs)
            tock = perf_counter_ns()
            time_trial[n] = tock - tick
        return time_trial.mean(), time_trial.std()

    return timer_wrapper


def check_for_horizontal_win_two(self, playing_grid: np.array) -> bool:  # TODO
    array_string_list = playing_grid.astype(str).to_list()
    list_joined_strings = ["".join(array_string_list) for row in array_string_list]
    if "1111" or "-1-1-1-1" in list_joined_strings:
        return True  # The row contains a winning row
    else:
        return False


@timer
def check_for_horizontal_win(playing_grid: np.array, rows: int, win_length: int) -> bool:
    for row_index in range(0, rows):
        convoluted_array = np.convolve(playing_grid[row_index],
                                       np.ones(win_length, dtype=int),
                                       mode="same")  # same key word prevents including first and last index
        max_consecutive = max(abs(convoluted_array))
        if max_consecutive == win_length:
            return True  # The row contains a winning row
        else:
            continue
    return False


# testing
rows = 3
win_length = 3

winning_playing_grid = np.array([
    [1, 1, 1, -1, 1, 1],
    [-1, -1, 1, -1, 1, 1],
    [-1, 1, -1, 1, -1, 1],
    [-1, 1, -1, 1, -1, -1]
])

mean, std = check_for_horizontal_win(playing_grid=winning_playing_grid, rows=rows, win_length=win_length)

print(f"In nanoseconds: Mean: {mean:.2f}, Std: {std:.2f}")









