from tkinter_gui.app.main_game_window.main_game_window import PlayingWindow
from tkinter_gui.app.game_setup_window.game_setup_window import SetupWindow


class NoughtsAndCrossesApp(SetupWindow):
    def __init__(self, setup_parameters=None, player_x_is_minimax=None, player_o_is_minimax=None):
        super().__init__(setup_parameters)
        self.player_x_is_minimax = False
        self.player_o_is_minimax = False

    def launch_game(self):
        self.launch_setup_window()
        playing_window = PlayingWindow(
            setup_parameters=self.setup_parameters,
            player_x_is_minimax=self.player_x_is_minimax,
            player_o_is_minimax=self.player_o_is_minimax
        )
        playing_window.launch_playing_window()





