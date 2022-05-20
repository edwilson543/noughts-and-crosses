from tkinter_gui.app.main_game_window.main_game_window import NoughtsAndCrossesWindow

##########
# To be deleted
from game.constants.game_constants import GameValue
from game.app.player_base_class import Player

pos_player = Player(name="Ed", active_symbol=GameValue.O)
neg_player = Player(name="Balint", active_symbol=GameValue.X)
##########

# TODO Add window to see who wants to go first and set this as player first attribute

if __name__ == "__main__" :
    game = NoughtsAndCrossesWindow(game_rows_m=6, game_cols_n=6, win_length_k=3,
                                   neg_player=neg_player, pos_player=pos_player, starting_player=GameValue.X.value)
    game.playing_grid[2, 2] = -1
    print(game.playing_grid)
    game.launch_playing_window()
