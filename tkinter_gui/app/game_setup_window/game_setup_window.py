"""Module to display the main_window that appears when players are setting up the game."""
from tkinter_gui.constants.dimensions import SetupWindowDimensions


# TODO do properly
class SetupWindow:
    def __init__(self, widget_manager): # TODO type hint...
        self.widget_manager = widget_manager

    def pack(self):
        self.widget_manager.game_parameters_frame.grid()