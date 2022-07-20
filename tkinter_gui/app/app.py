"""
Module to define the controller that links the different windows together in an event loop - this represents
the complete GUI of the application.
"""

# Local application GUI imports
from tkinter_gui.app.main_game_window.main_game_window import PlayingWindow
from tkinter_gui.app.game_setup_window.game_setup_window import SetupWindow
from tkinter_gui.app.game_continuation_window.game_continuation_window import GameContinuationPopUp


class NoughtsAndCrossesApp:
    def __init__(self):
        self.setup_window = SetupWindow()
        self.playing_window = None
        self.game_continuation_top_level = GameContinuationPopUp()
        self.player_x_is_minimax = False
        self.player_o_is_minimax = False

    def main_game_loop(self):
        """
        Method to control the main game loop of the noughts and crosses game.
        The simple game flow is:
        1) User sets the parameters for the game and enters their name etc. in the setup window.
        2) Confirming their details closes the setup window, having set these parameters globally in the
        self.setup_window object
        3) A game is launched using these parameters.
        4) Once one of the players has won, the game win counts by player are updated and a pop up is launched
        5) The pop up determines whether the game continues or not
        6) If it continues, a new game is launched
        """
        self.setup_game()
        self.keep_launching_new_games()

    def setup_game(self):
        """
        Method to launch the setup window and then store the user define parameters.
        Although the setup window is destroyed the attribute values can still be accessed through the object
        carrying the window (self.setup_window)
        """
        self.setup_window.launch_setup_window()
        self.playing_window = PlayingWindow(
            setup_parameters=self.setup_window.setup_parameters,
            player_x_is_minimax=self.setup_window.player_x_is_minimax,
            player_o_is_minimax=self.setup_window.player_o_is_minimax)

    def keep_launching_new_games(self):
        """
        Method to keep launching new games as long as the user wants to keep playing.
        Information is transferred between distinct components of the game and from
        """
        while True:
            self.playing_window.launch_playing_window()
            self.playing_window.historic_info_frame.draw_count = self.playing_window.active_game_frames.draw_count
            self.playing_window.active_game_frames.starting_player_value = \
                self.playing_window.active_game_frames.game_continuation_top_level.starting_player_value.get()
