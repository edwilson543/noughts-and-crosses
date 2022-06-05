"""Module recording constants relating to game flow timing"""

from enum import Enum


class PauseDuration(Enum):
    computer_turn = 0.5
    win_streak_flash = 0.1
    number_of_flashes = 5  # flash duration = 2 * win_streak_flash * number_of_flashes + processing
