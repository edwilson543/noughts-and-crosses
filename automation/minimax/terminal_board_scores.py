""""Module stating the value of a win / loss / draw to the maximising player"""

from enum import Enum


class TerminalScore(Enum):
    MAX_WIN = 1000
    DRAW = 0
    MAX_LOSS = -1000
