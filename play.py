from game.app.game_base_class import NoughtsAndCrossesEssentialParameters
from tkinter_gui.app.main_game_window.main_game_window import PlayingWindow

##########
# To be deleted
from game.constants.game_constants import BoardMarking
from game.app.player_base_class import Player

player_x = Player(name="Ed", marking=BoardMarking.X)
player_o = Player(name="Libby", marking=BoardMarking.O)

setup_parameters = NoughtsAndCrossesEssentialParameters(
    game_rows_m=3,
    game_cols_n=3,
    win_length_k=3,
    player_x=player_x,
    player_o=player_o,
    starting_player_value=BoardMarking.O.value,
)
##########

# TODO Add main_window to see who wants to go first and set this as player first attribute

if __name__ == "__main__" :
    game = PlayingWindow(setup_parameters=setup_parameters)
    game.launch_playing_window()
