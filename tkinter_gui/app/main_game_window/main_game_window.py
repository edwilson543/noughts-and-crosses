from game.app.game_base_class import NoughtsAndCrossesEssentialParameters
from tkinter_gui.constants.dimensions import MainWindowDimensions
from tkinter_gui.constants.style_and_colours import Colour
from tkinter_gui.app.main_game_window.active_game_frames import ActiveGameFrames
from tkinter_gui.app.main_game_window.historic_info_frame import HistoricInfoFrame
from tkinter_gui.app.main_game_window.main_game_widget_manager import MainWindowWidgetManager
import tkinter as tk


class NoughtsAndCrossesWindow(ActiveGameFrames, HistoricInfoFrame):
    def __init__(self,
                 setup_parameters: NoughtsAndCrossesEssentialParameters,
                 draw_count: int = 0,
                 active_unconfirmed_cell: (int, int) = None,
                 widget_manager=MainWindowWidgetManager()):
        super().__init__(setup_parameters, draw_count, active_unconfirmed_cell, widget_manager)

# TODO same for pop up

    def launch_playing_window(self):
        """Method for launching the main noughts and crosses game play main_window and controlling the game flow"""
        # Define and configure the main_window
        game_window = tk.Tk()
        game_window.title("Noughts and Crosses")
        game_window.configure(background=Colour.main_window.value)
        game_window.rowconfigure(index=0, weight=1)
        game_window.columnconfigure(index=0, weight=1)
        self.widget_manager.main_window = game_window
        self._populate_all_frames_in_main_window()
        game_window.mainloop()

    def _populate_all_frames_in_main_window(self):
        """Method to create all the frames used in the main game main_window and fill the with their components"""
        self._format_background_frame()

        # Frame that contains the playing grid (entire left)
        super().populate_empty_playing_grid_frame()
        self.widget_manager.playing_grid_frame.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=10, pady=10)

        # Frame for the buttons that control the gameplay (top-right)
        super().populate_game_info_frame()
        self.widget_manager.game_info_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # Frame for the labels that says the status across multiple games (bottom-right)
        super().populate_historic_info_frame()
        self.widget_manager.historic_info_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

    def _format_background_frame(self) -> None:
        """
        Method format the background frame, and upload it to the widget manager.
        The background frame contains all other frames in the main game window.
        """
        self.widget_manager.background_frame = tk.Frame(
            master=self.widget_manager.main_window,
            background=Colour.main_frame_background.value,
            borderwidth=3, relief=tk.RIDGE)
        self.widget_manager.background_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.widget_manager.background_frame.rowconfigure(
            index=[0, 1], minsize=MainWindowDimensions.game_info_frame.height, weight=1)
        self.widget_manager.background_frame.columnconfigure(
            index=0, minsize=MainWindowDimensions.game_frame.width, weight=1)
        self.widget_manager.background_frame.columnconfigure(
            index=1, minsize=MainWindowDimensions.game_info_frame.width, weight=0)
