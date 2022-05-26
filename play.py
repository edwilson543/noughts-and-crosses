from tkinter_gui.app.main_game_window.main_game_window import NoughtsAndCrossesWindow

##########
# To be deleted
from game.constants.game_constants import BoardMarking
from game.app.player_base_class import Player

pos_player = Player(name="Ed", active_symbol=BoardMarking.O)
neg_player = Player(name="Libby", active_symbol=BoardMarking.X)
##########

# TODO Add main_window to see who wants to go first and set this as player first attribute

if __name__ == "__main__" :
    game = NoughtsAndCrossesWindow(game_rows_m=3, game_cols_n=3, win_length_k=3,
                                   neg_player=neg_player, pos_player=pos_player, starting_player=BoardMarking.X.value)
    game.launch_playing_window()
