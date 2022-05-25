"""Module containing the dimensions of all aspects of the game"""

from dataclasses import dataclass


#  TODO padding and border width
#  Need to align widths of game info panels after padding


@dataclass(frozen=True)
class Dimension:
    """Dataclass for storing the width and height of an individual frame"""
    width: int
    height: int


##########
# Dimensions for the main main_window and pop up
##########

game_frame = Dimension(width=600, height=450)
game_info_frame = Dimension(width=int(game_frame.width / 2), height=int(game_frame.height / 2))
historic_info_frame = Dimension(width=game_info_frame.width, height=game_info_frame.height)
pop_up_window = Dimension(width=200, height=100)


@dataclass(frozen=True)
class MainWindowDimensions:
    game_frame = game_frame
    game_info_frame = game_info_frame
    historic_info_frame = historic_info_frame
    pop_up_window = pop_up_window


##########
# Dimensions for the setup main_window
##########

game_parameters_frame = Dimension(width=300, height=300)
game_parameters_frame_cells = Dimension(width=int(game_parameters_frame.width/5),
                                        height=int(game_parameters_frame.height/5))
player_info_frame = Dimension(width=300, height=300)


@dataclass(frozen=True)
class SetupWindowDimensions:
    game_parameters_frame = game_parameters_frame
    game_parameters_frame_cells = game_parameters_frame_cells
    player_info_frame = player_info_frame
