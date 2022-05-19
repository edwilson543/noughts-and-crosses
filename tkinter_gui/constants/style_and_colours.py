from enum import Enum

class GameColour(Enum):
    window = "black"
    background = "black"
    game_background = "#d1c7c7"
    game_buttons_background = "#b2d1f7"
    game_status_background = "#78f599"
    empty_entry_cell = "#ffe3b0"
    occupied_cell = "#fcd286"
    unconfirmed_cell_colour = "#ee82fa"


class Font(Enum):
    xo_font = "Times New Roman"
