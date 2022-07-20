"""Module to display the main_window that appears when players are setting up the game."""

# Standard library imports
from math import floor
import sys
import tkinter as tk

# Local application imports
from game.app.game_base_class import NoughtsAndCrossesEssentialParameters
from game.app.player_base_class import Player
from game.constants.game_constants import BoardMarking

# Local application GUI imports
from tkinter_gui.app.game_setup_window.player_info_frame import PlayerInfoFrame
from tkinter_gui.app.game_setup_window.game_parameters_frame import GameParametersFrame
from tkinter_gui.app.game_setup_window.game_setup_widget_manager import GameSetupWidgets
from tkinter_gui.constants.style_and_colours import Colour, Font, Relief
from tkinter_gui.constants.dimensions import SetupWindowDimensions


class SetupWindow:
    def __init__(self,
                 setup_parameters: NoughtsAndCrossesEssentialParameters = None,
                 widget_manager: GameSetupWidgets = GameSetupWidgets()):
        self.setup_parameters = setup_parameters
        self.widget_manager = widget_manager
        self.game_parameters_frame = GameParametersFrame(widget_manager=self.widget_manager)
        self.player_info_frame = PlayerInfoFrame(widget_manager=self.widget_manager)
        self.player_x_is_minimax = False
        self.player_o_is_minimax = False

    def launch_setup_window(self) -> None:
        """Method that is called to launch the game setup window"""
        self._create_and_format_setup_window()
        self._add_frames_to_setup_window()
        self._add_confirmation_button_to_setup_window()
        self.widget_manager.setup_window.update()  # Updates geometry attached window so can use winfo_width/height
        self.widget_manager.setup_window.minsize(
            width=self.widget_manager.setup_window.winfo_width(),
            height=self.widget_manager.setup_window.winfo_height())
        self.widget_manager.setup_window.mainloop()

    def _create_and_format_setup_window(self) -> None:
        """Method to create and format the setup window, adding it to the widget manager"""
        setup_window = tk.Tk()
        setup_window.protocol("WM_DELETE_WINDOW", sys.exit)  # Avoids future game loop code executing
        setup_window.title("Noughts and Crosses Setup")
        setup_window.configure(background=Colour.setup_window_background.value)
        setup_window.rowconfigure(index=0, weight=1)
        setup_window.columnconfigure(index=[0, 1], weight=1)
        self.widget_manager.setup_window = setup_window

    def _add_frames_to_setup_window(self) -> None:
        """Method that fills the frame up with all their component widgets, and then adds them to the setup window."""
        self.game_parameters_frame.populate_game_parameters_frame()
        self.player_info_frame.populate_player_info_frame()

        self.widget_manager.game_parameters_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.widget_manager.player_info_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

    # Additional components to be added to the setup window
    def _add_confirmation_button_to_setup_window(self) -> None:
        """Method that adds the confirmation button to the setup window (and widget manager)."""
        self.widget_manager.confirmation_button = self._get_confirmation_button()
        self.widget_manager.confirmation_button.grid(row=1, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

    def _confirm_all_details_button_command(self) -> None:
        """Method that extracts all of the game and player info, uploads it to a dict and then"""
        self.setup_parameters = NoughtsAndCrossesEssentialParameters(
            game_rows_m=self.game_parameters_frame.game_rows_m.get(),
            game_cols_n=self.game_parameters_frame.game_cols_n.get(),
            win_length_k=self.game_parameters_frame.win_length_k.get(),
            player_x=Player(name=self.player_info_frame.player_x_entry.get(), marking=BoardMarking.X),
            player_o=Player(name=self.player_info_frame.player_o_entry.get(), marking=BoardMarking.O),
            starting_player_value=self.player_info_frame.starting_player_value.get()
        )
        self.player_x_is_minimax = self.player_info_frame.player_x_is_minimax.get()
        self.player_o_is_minimax = self.player_info_frame.player_o_is_minimax.get()
        self.widget_manager.setup_window.destroy()

    def _get_confirmation_button(self) -> tk.Button:
        """Returns: the formatted confirmation button that links the setup window to the main game window"""
        confirmation_button = tk.Button(
            master=self.widget_manager.setup_window,
            command=self._confirm_all_details_button_command,
            text="Confirm all entries",
            background=Colour.confirmation_button.value,
            state=tk.DISABLED,
            font=(Font.default_font.value, floor(SetupWindowDimensions.game_parameters_frame_cells.height/4)),
            relief=Relief.confirmation_button.value
        )
        return confirmation_button
