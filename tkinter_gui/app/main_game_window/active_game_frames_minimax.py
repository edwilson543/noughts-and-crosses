"""Module which subclasses the active game frames to allow minimax to play as one of the players"""

from game.app.game_base_class import NoughtsAndCrossesEssentialParameters
from game.app.game_base_class import Player
from automation.minimax.minimax_ai import NoughtsAndCrossesMinimax
from tkinter_gui.app.main_game_window.active_game_frames import ActiveGameFrames
from tkinter_gui.app.main_game_window.main_game_widget_manager import MainWindowWidgetManager


class ActiveGameFramesMinimax(ActiveGameFrames, NoughtsAndCrossesMinimax):
    def __init__(self,
                 setup_parameters: NoughtsAndCrossesEssentialParameters,
                 draw_count: int = 0,
                 active_unconfirmed_cell: (int, int) = None,
                 widget_manager=MainWindowWidgetManager(),
                 maximising_player: Player = None):
        """
        :param setup_parameters: The parameters required to fully define the game of N and C
        :param draw_count: Number of draws in the active game
        :param active_unconfirmed_cell: The cell the user has selected
        :param widget_manager: Global widget storage object
        :param maximising_player: The player that the minimax AI will be playing as - by default this is none,
        meaning that it's just an ordinary 2 human game.
        """
        super().__init__(setup_parameters, draw_count, active_unconfirmed_cell, widget_manager)
        self.maximising_player = maximising_player

    def _confirmation_buttons_command(self) -> None:
        """
        Method to override (extend) what happens when the confirmation button is clicked.
        We need this to not just confirm the human user's go, but to initiate the ai player to make their go.
        Note that if there is no maximising_player, then this just does the exact same as the normal 2 human version.
        """
        super()._confirmation_buttons_command()  # First do everything the super class version does
        if self.maximising_player is not None:
            _, move = super().get_minimax_move()
            super()._available_cell_button_command(row_index=move[0], col_index=move[1])  # simulate cell selection
            super()._confirmation_buttons_command()  # Confirm ai player's choice on the game board

