from tkinter_gui.game_base_class_user import NoughtsAndCrossesWindow

##########
# To be deleted
from game.constants.game_constants import GameValue
from game.app.player_base_class import Player

player_o = Player(name="Ed", active_symbol=GameValue.O)
player_x = Player(name="Balint", active_symbol=GameValue.X)
##########

if __name__ == "__main__" :
    game = NoughtsAndCrossesWindow(game_rows_m=10, game_cols_n=12, win_length_k=3,
                                   player_x=player_x, player_o=player_o)
    game.playing_grid[2, 2] = -1
    print(game.playing_grid)
    game.launch_playing_window()
