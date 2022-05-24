"""Module to display the window that appears when players are setting up the game."""
from tkinter_gui.constants.dimensions import SetupWindowDimensions


# TODO do properly
class SetupWindow:
    def __init__(self, widget_manager): # TODO type hint...
        self.widget_manager = widget_manager

    def populate_game_parameters_frame(self):
        self.widget_manager.game_parameters_frame.rowconfigure(
            index=[0, 1, 2, 3, 4], weight=1,
            minsize=SetupWindowDimensions.game_parameters_frame_cells.height)
        self.widget_manager.game_parameters_frame.columnconfigure(
            index=[0, 1, 2, 3, 4], weight=1,
            minsize=SetupWindowDimensions.game_parameters_frame_cells.width)