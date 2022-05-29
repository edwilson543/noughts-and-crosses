"""Module which subclasses the active game frames to allow minimax to play as one of the players"""

from game.app.game_base_class import NoughtsAndCrossesEssentialParameters
from game.constants.game_constants import BoardMarking
from automation.minimax.minimax_ai import NoughtsAndCrossesMinimax
from tkinter_gui.app.main_game_window.active_game_frames import ActiveGameFrames
from tkinter_gui.app.main_game_window.main_game_widget_manager import MainWindowWidgetManager
from tkinter_gui.constants.game_flow_timing import PauseDuration
from time import sleep


class ActiveGameFramesMinimax(ActiveGameFrames, NoughtsAndCrossesMinimax):
    def __init__(self,
                 setup_parameters: NoughtsAndCrossesEssentialParameters,
                 draw_count: int = 0,
                 active_unconfirmed_cell: (int, int) = None,
                 widget_manager=MainWindowWidgetManager(),
                 player_x_is_minimax: bool = False,
                 player_o_is_minimax: bool = False):
        """
        Parameters:
        ----------
        setup_parameters: The parameters required to fully define the game of N and C
        draw_count: Number of draws in the active game
        active_unconfirmed_cell: The cell the user has selected
        widget_manager: Global widget storage object
        player_x_is_minimax / player_o_is_minimax: T/F depending on whether either player is controlled by the minimax
        algorithm. Either one or neither of the players can be the minimax algorithm.
        """
        super().__init__(setup_parameters, draw_count, active_unconfirmed_cell, widget_manager)
        self.player_x_is_minimax = player_x_is_minimax
        self.player_o_is_minimax = player_o_is_minimax

    def _confirmation_buttons_command(self) -> None:
        """
        Method to override (extend) what happens when the confirmation button is clicked.
        We need this to not just confirm the human user's go, but to initiate the ai player to make their go.
        Note that if there is no ai player, then no functionality us added.
        """
        super()._confirmation_buttons_command()  # First do everything the super class version does
        if (self.get_player_turn(playing_grid=self.playing_grid) == BoardMarking.O.value) and \
                self.player_o_is_minimax:
            self.ai_player_makes_next_move()
        elif (self.get_player_turn(playing_grid=self.playing_grid) == BoardMarking.X.value) and \
                self.player_x_is_minimax:
            self.ai_player_makes_next_move()

    def check_if_ai_goes_first(self):
        """Method to check whether the ai player goes first - otherwise we'll be stuck with nothing happening"""
        if (self.starting_player_value == self.player_o.marking.value) and self.player_o_is_minimax:
            super()._initialise_confirmation_buttons()
            self.ai_player_makes_next_move()
        elif (self.starting_player_value == self.player_x.marking.value) and self.player_x_is_minimax:
            super()._initialise_confirmation_buttons()
            self.ai_player_makes_next_move()

    def ai_player_makes_next_move(self):
        """
        Method to automate the next move - note there is no need to specify who's turn it is , this is all
        known through the minimax implementation.
        By clicking the confirmation button at the end, the ai player hands the turn back to the human player (or the
        other ai player)

        Outcomes:
        _________
        AI makes the next move and all relevant updates are made.
        """
        sleep(PauseDuration.computer_turn.value)
        _, move = super().get_minimax_move()
        super()._available_cell_button_command(row_index=move[0], col_index=move[1])  # simulate cell selection
        super()._confirmation_buttons_command()  # Confirm ai player's choice on the game board
