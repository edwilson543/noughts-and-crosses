"""Module containing the dimensions of all aspects of the game"""

from dataclasses import dataclass

#  TODO padding and border width
#  Need to align widths of game info panels after padding


@dataclass
class Dimension:
    width: int
    height: int


game_frame = Dimension(width=600, height=450)
game_info_frame = Dimension(width=int(game_frame.width / 2), height=int(game_frame.height / 2))
historic_info_frame = Dimension(width=game_info_frame.width, height=game_info_frame.height)
pop_up_window = Dimension(width=200, height=100)

@dataclass
class FrameDimensions:
    game_frame = game_frame
    game_info_frame = game_info_frame
    historic_info_frame = historic_info_frame
    pop_up_window = pop_up_window
