"""Module to display the main_window that appears when players are setting up the game."""
from game.app.game_base_class import NoughtsAndCrossesEssentialParameters
from tkinter_gui.app.game_setup_window.player_info_frame import PlayerInfoFrame
from tkinter_gui.app.game_setup_window.game_parameters_frame import GameParametersFrame
from tkinter_gui.app.game_setup_window.game_setup_widget_manager import GameSetupWidgets
from tkinter_gui.constants.style_and_colours import Colour

import tkinter as tk


class SetupWindow(PlayerInfoFrame, GameParametersFrame):
    def __init__(self,
                 widget_manager: GameSetupWidgets = GameSetupWidgets(),
                 player_x_entry: tk.StringVar = None,
                 player_o_entry: tk.StringVar = None,
                 starting_player_value: tk.IntVar = None,
                 game_rows_m: tk.IntVar = None,
                 game_cols_n: tk.IntVar = None,
                 win_length_k: tk.IntVar = None,
                 setup_parameters: NoughtsAndCrossesEssentialParameters = None):
        super().__init__(widget_manager, player_x_entry, player_o_entry, starting_player_value)
        self.game_rows_m = game_rows_m
        self.game_cols_n = game_cols_n
        self.win_length_k = win_length_k
        self.setup_parameters = setup_parameters

    def launch_setup_window(self) -> None:
        self._create_and_format_setup_window()
        self._add_frames_to_setup_window()
        self._add_confirmation_button_to_setup_window()
        self.widget_manager.setup_window.mainloop()

    def _create_and_format_setup_window(self) -> None:
        """Method to create and format the setup window, adding it to the widget manager"""
        setup_window = tk.Tk()
        setup_window.title("Noughts and Crosses Setup")
        setup_window.configure(background=Colour.setup_window_background.value)
        setup_window.rowconfigure(index=0, weight=1)
        setup_window.columnconfigure(index=[0, 1], weight=1)
        self.widget_manager.setup_window = setup_window

    def _add_frames_to_setup_window(self) -> None:
        """Method that fills the frame up with all their component widgets, and then adds them to the setup window."""
        super().populate_game_parameters_frame()
        super().populate_player_info_frame()

        self.widget_manager.game_parameters_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.widget_manager.player_info_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

    def _add_confirmation_button_to_setup_window(self) -> None:
        """Method that adds the confirmation button to the setup window (and widget manager)."""
        self.widget_manager.confirmation_button = self._get_confirmation_button()
        self.widget_manager.confirmation_button.grid(row=1, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

    def _confirm_all_details_button_command(self) -> None:
        """Method that extracts all of the game and player info, uploads it to a dict and then"""
        # TODO make it so that until players names are included, cannot confirm
        # Can use the trace function on the fields
        self.setup_parameters = NoughtsAndCrossesEssentialParameters(
            game_rows_m=self.game_rows_m.get(),
            game_cols_n=self.game_cols_n.get(),
            win_length_k=self.win_length_k.get(),
            player_x=self.player_x_entry.get(),
            player_o=self.player_o_entry.get(),
            starting_player_value=self.starting_player_value.get()
        )
        print(self.setup_parameters)

    def _get_confirmation_button(self) -> tk.Button:
        """Returns: the formatted confirmation button that links the setup window to the main game window"""
        confirmation_button = tk.Button(
            master=self.widget_manager.setup_window,
            command=self._confirm_all_details_button_command,
            text="Confirm all entries"
        )
        return confirmation_button

SetupWindow().launch_setup_window()
