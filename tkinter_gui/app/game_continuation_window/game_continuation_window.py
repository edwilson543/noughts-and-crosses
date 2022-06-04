"""Module containing the class that produces the top up when a player has won or there is a draw"""

from game.constants.game_constants import StartingPlayer, BoardMarking
from game.app.player_base_class import Player
from tkinter_gui.app.main_game_window.main_game_widget_manager import MainWindowWidgetManager
from tkinter_gui.constants.dimensions import MainWindowDimensions
from tkinter_gui.constants.style_and_colours import Colour, Relief, Font
from dataclasses import dataclass
from math import floor
import tkinter as tk
import sys


@dataclass
class GameContinuationWidgets:
    """
    Dataclass for storing widgets that need to be globally accessible.
    This is only use in this module, hence why it's defined here and not in its own module.
    """
    pop_up_window: tk.Toplevel = None
    player_x_starts_next_game_radio: tk.Radiobutton = None
    player_o_starts_next_game_radio: tk.Radiobutton = None
    random_player_starts_next_game_radio: tk.Radiobutton = None


class GameContinuationPopUp:
    def __init__(self,
                 winner: Player | None = None,
                 draw: bool = False,
                 main_game_window_widget_manager: MainWindowWidgetManager = None,
                 starting_player_value: tk.IntVar = None):
        self.winner = winner
        self.draw = draw
        self.main_game_window_widget_manager = main_game_window_widget_manager
        self.starting_player_value = starting_player_value
        self.continuation_widget_manager = GameContinuationWidgets()

    def launch_continuation_pop_up(self):
        """Method to launch the pop up main_window"""
        self._create_and_format_pop_up_window()
        self._populate_pop_up_window()
        self.continuation_widget_manager.pop_up_window.mainloop()

    def _populate_pop_up_window(self):
        """Method to fill up the game_continuation_top_level main_window with all the relevant components"""
        self._upload_next_starting_player_radio_buttons_to_widget_manager()

        game_outcome_label = self._get_game_outcome_label()
        game_outcome_label.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

        continue_game_button = self._get_continue_game_button()
        continue_game_button.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        exit_game_button = self._get_exit_game_button()
        exit_game_button.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)

        # Starting player selection widgets for the next game
        starting_player_label = self._get_starting_player_label()
        starting_player_label.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=2, pady=2)
        self.continuation_widget_manager.random_player_starts_next_game_radio.grid(
            row=3, column=0, columnspan=2, sticky="nsew", padx=2, pady=2)
        self.continuation_widget_manager.player_x_starts_next_game_radio.grid(
            row=4, column=0, columnspan=2, sticky="nsew", padx=2, pady=2)
        self.continuation_widget_manager.player_o_starts_next_game_radio.grid(
            row=5, column=0, columnspan=2, sticky="nsew", padx=2, pady=2)

    def _create_and_format_pop_up_window(self):
        """
        Method to create the pop up TopLevel and set the relative dimensions of the grid cells in the
        pop up window.
        """
        self.continuation_widget_manager.player_x_starts_next_game_radio = 5

        self.continuation_widget_manager.pop_up_window = tk.Toplevel(
            master=self.main_game_window_widget_manager.main_window, background=Colour.pop_up_window_background.value)
        self.continuation_widget_manager.pop_up_window.resizable(width=False, height=False)
        self.continuation_widget_manager.pop_up_window.rowconfigure(
            index=[0, 1], minsize=MainWindowDimensions.pop_up_window.height / 4, weight=1)
        self.continuation_widget_manager.pop_up_window.rowconfigure(
            index=[2, 3, 4, 5], minsize=MainWindowDimensions.pop_up_window.height / 8, weight=1)
        self.continuation_widget_manager.pop_up_window.columnconfigure(
            index=[0, 1], minsize=MainWindowDimensions.pop_up_window.width / 2, weight=1)

    # Labels and buttons
    def _get_game_outcome_label(self) -> tk.Label:
        """Method to display the outcome of the game"""
        if isinstance(self.winner, Player):
            text = f"{self.winner.name} wins!"
        else:
            text = f"Game ended in a draw"
        game_outcome_label = tk.Label(
            master=self.continuation_widget_manager.pop_up_window,
            text=text,
            background=Colour.game_outcome_label.value,
            foreground=Colour.game_outcome_label_font.value,
            font=(Font.default_font.value, floor(MainWindowDimensions.pop_up_window.height / 5)),
            relief=Relief.game_outcome_label.value
        )
        return game_outcome_label

    def _get_continue_game_button(self) -> tk.Button:
        """Method to create the continue game button in the pop up"""
        game_continuation_button = tk.Button(
            master=self.continuation_widget_manager.pop_up_window,
            command=self._continue_game_button_command,
            text="Play Again",
            background=Colour.game_continuation_exit_buttons.value,
            foreground=Colour.game_continuation_exit_buttons_font.value,
            font=(Font.default_font.value, floor(MainWindowDimensions.pop_up_window.height / 5)),
            relief=Relief.game_continuation_exit_buttons.value
        )
        return game_continuation_button

    def _get_exit_game_button(self) -> tk.Button:
        """Method to create the exit game button in the pop up"""
        exit_game_button = tk.Button(
            master=self.continuation_widget_manager.pop_up_window,
            command=self._exit_game_button_command,
            text="Exit Game",
            background=Colour.game_continuation_exit_buttons.value,
            foreground=Colour.game_continuation_exit_buttons_font.value,
            font=(Font.default_font.value, floor(MainWindowDimensions.pop_up_window.height / 5)),
            relief=Relief.game_continuation_exit_buttons.value
        )
        return exit_game_button

    # Continuation/ exit button commands
    def _continue_game_button_command(self) -> None:
        """Method that just shuts the pop_up_window main_window"""
        self.continuation_widget_manager.pop_up_window.destroy()
        self.main_game_window_widget_manager.main_window.destroy()

    @staticmethod
    def _exit_game_button_command() -> None:
        """Method that ends the game by exiting the application."""
        sys.exit()

    ##########
    # Starting player radio buttons for the next round
    ##########
    def _get_starting_player_label(self) -> tk.Label:
        """Method that returns the label saying "choose starting player" above the radio buttons"""
        starting_player_label = tk.Label(
            master=self.continuation_widget_manager.pop_up_window,
            text="Choose who starts the next game",
            background=Colour.starting_player_label.value,
            relief=Relief.starting_player_label.value,
            font=(Font.default_font.value, floor(MainWindowDimensions.pop_up_window.height / 8)))
        return starting_player_label

    def _upload_next_starting_player_radio_buttons_to_widget_manager(self) -> None:
        """
       Method to create the radio buttons that are used for the user to select which player should the next game.
       These are not returned but just uploaded straight to the widget manager, because there are 3 of them which it
       makes sense to just create in a batch as below.
       """
        self.starting_player_value = tk.IntVar()
        self._set_loser_to_go_first_as_default()  # sets the above value to be loser or random if draw

        player_x_starts = tk.Radiobutton(
            master=self.continuation_widget_manager.pop_up_window,
            text="Player X", variable=self.starting_player_value,
            value=StartingPlayer.PLAYER_X.value,
            background=Colour.starting_player_radio.value,
            relief=Relief.starting_player_radio.value,
            font=(Font.default_font.value, floor(MainWindowDimensions.pop_up_window.height / 8)))
        self.continuation_widget_manager.player_x_starts_next_game_radio = player_x_starts

        player_o_starts = tk.Radiobutton(
            master=self.continuation_widget_manager.pop_up_window,
            text="Player O", variable=self.starting_player_value,
            value=StartingPlayer.PLAYER_O.value,
            background=Colour.starting_player_radio.value,
            relief=Relief.starting_player_radio.value,
            font=(Font.default_font.value, floor(MainWindowDimensions.pop_up_window.height / 8)))
        self.continuation_widget_manager.player_o_starts_next_game_radio = player_o_starts

        random_player_starts = tk.Radiobutton(
            master=self.continuation_widget_manager.pop_up_window,
            text="Random", variable=self.starting_player_value,
            value=StartingPlayer.RANDOM.value,
            background=Colour.starting_player_radio.value,
            relief=Relief.starting_player_radio.value,
            font=(Font.default_font.value, floor(MainWindowDimensions.pop_up_window.height / 8)))
        self.continuation_widget_manager.random_player_starts_next_game_radio = random_player_starts

    def _set_loser_to_go_first_as_default(self):
        """
        Method which selects the losing player's radio button as the default for when starting the new game.
        The user can change the starting player to whoever, as above.
        """
        if isinstance(self.winner, Player) and self.winner.marking == BoardMarking.X:
            self.starting_player_value.set(value=StartingPlayer.PLAYER_O.value)
        elif isinstance(self.winner, Player) and self.winner.marking == BoardMarking.O:
            self.starting_player_value.set(value=StartingPlayer.PLAYER_X.value)
        elif self.draw:
            self.starting_player_value.set(value=StartingPlayer.RANDOM.value)
        else:
            raise ValueError("No valid game outcome used to instantiate the GameContinuationWindow")
