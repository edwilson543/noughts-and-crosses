"""Module which subclasses the active game frames to allow minimax to play as one of the players"""

# Standard library imports
from time import sleep
import tkinter as tk
from typing import Tuple

# Local application imports
from game.app.game_base_class import NoughtsAndCrossesEssentialParameters
from game.constants.game_constants import BoardMarking
from automation.minimax.minimax_ai import NoughtsAndCrossesMinimax

# Local applications GUI imports
from tkinter_gui.app.main_game_window.active_game_frames import ActiveGameFrames
from tkinter_gui.app.main_game_window.main_game_widget_manager import MainWindowWidgetManager
from tkinter_gui.constants.game_flow_timing import PauseDuration


class ActiveGameFramesMinimax(ActiveGameFrames, NoughtsAndCrossesMinimax):
    def __init__(self,
                 setup_parameters: NoughtsAndCrossesEssentialParameters,
                 draw_count: int = 0,
                 active_unconfirmed_cell: Tuple[int, int] = None,
                 widget_manager=MainWindowWidgetManager(),
                 player_x_is_minimax: bool = False,
                 player_o_is_minimax: bool = False):
        """
        Parameters:
        ----------
        setup_parameters: The parameters required to fully define the game of N and C
        draw_count: Number of draws in the active game
        active_unconfirmed_cell: The cell the user has selected
        main_game_window_widget_manager: Global widget storage object
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
        if self._whole_board_search() or self.check_for_draw():
            # TODO this is a fix for the fact that when a game involving minimax is completed, and the game was
            #  terminated after minimax's go, before starting the next game, the elifs below (previously if/elif) were
            #  called, because they did not know the game was over and a new game was starting. Perhaps a better way
            return
        elif (self.get_player_turn() == BoardMarking.O.value) and self.player_o_is_minimax:
            self._minimax_player_makes_next_move()
        elif (self.get_player_turn() == BoardMarking.X.value) and self.player_x_is_minimax:
            self._minimax_player_makes_next_move()
        else:  # Minimax's turn is over, so witch buttons back on
            self._switch_back_on_available_cell_buttons_after_minimax_turn()

    def check_if_minimax_goes_first(self):
        """Method to check whether the ai player goes first - otherwise we'll be stuck with nothing happening"""
        if (self.starting_player_value == self.player_o.marking.value) and self.player_o_is_minimax:
            self._minimax_player_makes_next_move()
        elif (self.starting_player_value == self.player_x.marking.value) and self.player_x_is_minimax:
            self._minimax_player_makes_next_move()

    def _minimax_player_makes_next_move(self):
        """
        Method to automate the next move - note there is no need to specify who's turn it is , this is all
        known through the minimax implementation.
        By clicking the confirmation button at the end, the ai player hands the turn back to the human player (or the
        other ai player)

        Outcomes:
        _________
        AI makes the next move and all relevant updates are made.
        """
        self._switch_off_all_available_cell_buttons()
        _, move = super().get_minimax_move_iterative_deepening()
        sleep(PauseDuration.computer_turn.value)
        super()._available_cell_button_command(row_index=move[0], col_index=move[1])  # simulate cell selection
        self._confirmation_buttons_command()  # Confirm ai player's choice on the game board

    def _switch_back_on_available_cell_buttons_after_minimax_turn(self):
        """
        Undoes the _switch_off_available_cell_buttons_during_minimax_turn method above.
        Note however that following minimax's turn there is one less available cell button.
        """
        for widget in self.widget_manager.playing_grid.flat:
            if isinstance(widget, tk.Button):
                widget["state"] = tk.NORMAL
