"""Module containing the class that produces the top up when a player has won or there is a draw"""

from tkinter_gui.app.main_game_window.main_game_widget_manager import MainWindowWidgetManager
from tkinter_gui.constants.dimensions import MainWindowDimensions
from tkinter_gui.constants.style_and_colours import Colour, Relief, Font
from math import floor
import tkinter as tk

# TODO could add in check buttons for who then goes first - loser, winner, random


class GameContinuationPopUp:
    def __init__(self,
                 text: str,
                 widget_manager: MainWindowWidgetManager,
                 pop_up_window: tk.Toplevel = None):
        self.text = text
        self.widget_manager = widget_manager
        self.pop_up_window = pop_up_window

    def launch_continuation_pop_up(self):
        """Method to launch the pop up main_window"""
        pop_up = tk.Toplevel(self.widget_manager.main_window, background=Colour.pop_up_window_background.value)
        pop_up.resizable(width=False, height=False)
        self.pop_up_window = pop_up
        self._populate_pop_up_window()
        pop_up.mainloop()

    def _populate_pop_up_window(self):
        """Method to fill up the pop_up main_window with all the relevant components"""
        self.pop_up_window.rowconfigure(index=[0, 1], minsize=MainWindowDimensions.pop_up_window.height / 2, weight=1)
        self.pop_up_window.columnconfigure(index=[0, 1], minsize=MainWindowDimensions.pop_up_window.width / 2, weight=1)

        game_outcome_label = self._get_game_outcome_label()
        game_outcome_label.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)

        continue_game_button = self._get_continue_game_button()
        continue_game_button.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        exit_game_button = self._get_exit_game_button()
        exit_game_button.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)

    # Labels and buttons
    def _get_game_outcome_label(self) -> tk.Label:
        """Method to display the outcome of the game"""
        game_outcome_label = tk.Label(
            master=self.pop_up_window,
            text=self.text,
            background=Colour.game_outcome_label.value,
            foreground=Colour.game_outcome_label_font.value,
            font=(Font.default_font.value, floor(MainWindowDimensions.pop_up_window.height / 6)),
            relief=Relief.game_outcome_label.value
        )
        return game_outcome_label

    def _get_continue_game_button(self) -> tk.Button:
        """Method to create the continue game button in the pop up"""
        game_continuation_button = tk.Button(
            master=self.pop_up_window,
            command=self._continue_game_button_command,
            text="Play Again",
            background=Colour.game_continuation_exit_buttons.value,
            foreground=Colour.game_continuation_exit_buttons_font.value,
            font=(Font.default_font.value, floor(MainWindowDimensions.pop_up_window.height / 6)),
            relief=Relief.game_continuation_exit_buttons.value
        )
        return game_continuation_button

    def _get_exit_game_button(self) -> tk.Button:
        """Method to create the exit game button in the pop up"""
        exit_game_button = tk.Button(
            master=self.pop_up_window,
            command=self._exit_game_button_command,
            text="Exit Game",
            background=Colour.game_continuation_exit_buttons.value,
            foreground=Colour.game_continuation_exit_buttons_font.value,
            font=(Font.default_font.value, floor(MainWindowDimensions.pop_up_window.height / 6)),
            relief=Relief.game_continuation_exit_buttons.value
        )
        return exit_game_button

    # Button commands
    def _continue_game_button_command(self):
        """Method that just shuts the pop_up_window main_window"""
        self.pop_up_window.destroy()

    def _exit_game_button_command(self):
        """Method that ends the game by shutting the main main_window"""
        self.widget_manager.main_window.destroy()
