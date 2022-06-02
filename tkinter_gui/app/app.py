from game.app.game_base_class import NoughtsAndCrossesEssentialParameters
from tkinter_gui.app.main_game_window.main_game_window import PlayingWindow
from tkinter_gui.app.game_setup_window.game_setup_window import SetupWindow
from tkinter_gui.app.game_continuation_window.game_continuation_window import GameContinuationPopUp


class NoughtsAndCrossesApp:
    def __init__(self):
        self.setup_window = SetupWindow()
        self.playing_window = None
        #  TODO can set the default argument for PlayingWindow setup_parameters to be None
        self.pop_up: None
        self.player_x_is_minimax = False
        self.player_o_is_minimax = False
        #  TODO we maybe want a widget manager here

    def launch_game(self):
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
        self.setup_window.launch_setup_window()
        self.playing_window = PlayingWindow(
            setup_parameters=self.setup_window.setup_parameters,
            player_x_is_minimax=self.setup_window.player_x_is_minimax,
            player_o_is_minimax=self.setup_window.player_o_is_minimax
        )
        # Although the setup window is destroyed the attribute values remain
        while True:
            self.playing_window.launch_playing_window()
            # TODO can now add the following features:
            # First refactor the end of the game method
            # Flashing win streak
            # User is given the option for who starts the next game (take from setup)

