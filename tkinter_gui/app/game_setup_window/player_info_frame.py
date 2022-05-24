from tkinter_gui.app.game_setup_window.game_setup_widget_manager import GameSetupWidgets
from game.constants.game_constants import GameValue
import tkinter as tk
from tkinter import ttk

class PlayerInfoFrame:
    """Class for the frame that allows users to enter their names and say who should go first."""
    def __init__(self, widget_manager: GameSetupWidgets):
        self.widget_manager = widget_manager

    def populate_player_info_frame(self):
        pass

    def _configure_player_info_frame(self):
        pass

    def _upload_widgets_to_widget_manager(self):
        pass

    ##########
    # Player labels and entry
    ##########
    def get_player_label(self, marking: GameValue) -> tk.Label:
        """Method returning the label showing player one / player two"""
        pass

    def get_player_entry_field(self) -> tk.Entry:
        """Method returning an entry field where players can write their names."""
        pass

    ##########
    # Starting player radio buttons
    ##########
    def get_all_radio_buttons(self) -> ttk.Radiobutton:
        pass
