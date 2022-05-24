from tkinter_gui.app.game_setup_window.game_setup_widget_manager import GameSetupWidgets
from tkinter_gui.constants.game_parameter_constraints import GameSizeParameters
from tkinter_gui.constants.dimensions import SetupWindowDimensions
from tkinter_gui.constants.style_and_colours import Colour, Font, Relief

from tkinter import ttk
import tkinter as tk
from math import floor


class GameParametersFrame:
    """
    Class that fills the game parameters (left-hand) frame on the setup menu.
    The purpose of this frame is for the user to define the structure of the game they would like to play.
    """

    def __init__(self,
                 widget_manager: GameSetupWidgets,
                 game_rows_m: tk.IntVar = None,
                 game_cols_n: tk.IntVar = None,
                 win_length_k: tk.IntVar = None):
        self.widget_manager = widget_manager
        self.game_rows_m = game_rows_m
        self.game_cols_n = game_cols_n
        self.win_length_k = win_length_k

    def populate_game_parameters_frame(self) -> None:
        """Method that inserts all the labels/ scales into the game parameters frame"""
        self._configure_game_parameters_frame()
        self._upload_widgets_to_widget_manager()

        self.widget_manager.game_rows_scale.grid(row=1, column=0, rowspan=3, sticky="ns", padx=5, pady=5)
        self.widget_manager.game_cols_scale.grid(row=4, column=1, columnspan=3, sticky="ew", padx=5, pady=5)
        self.widget_manager.win_length_scale.grid(row=0, column=1, columnspan=3, sticky="ew", padx=5, pady=5)
        self.widget_manager.game_rows_label.grid(row=2, column=1, columnspan=3, sticky="nsew", padx=5, pady=5)
        self.widget_manager.game_cols_label.grid(row=3, column=1, columnspan=3, sticky="nsew", padx=5, pady=5)
        self.widget_manager.win_length_label.grid(row=1, column=1, columnspan=3, sticky="nsew", padx=5, pady=5)

    def _configure_game_parameters_frame(self):
        """Method to format the game parameters frame"""
        self.widget_manager.game_parameters_frame = tk.Frame(
            master=self.widget_manager.setup_window,
            background=Colour.game_parameters_frame_background.value,
            borderwidth=3
        )
        self.widget_manager.game_parameters_frame.rowconfigure(
            index=[0, 1, 2, 3, 4], weight=1,
            minsize=SetupWindowDimensions.game_parameters_frame_cells.height)
        self.widget_manager.game_parameters_frame.columnconfigure(
            index=[0, 1, 2, 3], weight=1,
            minsize=SetupWindowDimensions.game_parameters_frame_cells.width)

    def _upload_widgets_to_widget_manager(self) -> None:
        """Method that adds all labels represented in this class to the widget manager"""
        self.widget_manager.game_rows_scale = self.get_game_rows_scale()
        self.widget_manager.game_cols_scale = self.get_game_cols_scale()
        self.widget_manager.win_length_scale = self.get_win_length_scale()
        self.widget_manager.game_rows_label = self.get_game_rows_label()
        self.widget_manager.game_cols_label = self.get_game_cols_label()
        self.widget_manager.win_length_label = self.get_win_length_label()

    ##########
    # Scale objects in the game parameters frame
    ##########
    def get_game_rows_scale(self) -> ttk.Scale:
        """Method to produce the ttk scale object used by the user to select the number of rows to play with."""
        self.game_rows_m = tk.IntVar(value=GameSizeParameters.default_rows.value)
        game_rows_scale = tk.Scale(
            master=self.widget_manager.game_parameters_frame,
            from_=GameSizeParameters.min_rows.value,
            to=GameSizeParameters.max_rows.value,
            orient=tk.VERTICAL,
            variable=self.game_rows_m,
            command=self.game_rows_scale_command,
            background=Colour.row_scale_background.value,
            trough=Colour.row_scale_trough.value,
            showvalue=False,
        )
        return game_rows_scale

    def get_game_cols_scale(self) -> ttk.Scale:
        """Method to produce the ttk scale object used by the user to select the number of columns to play with."""
        self.game_cols_n = tk.IntVar(value=GameSizeParameters.default_cols.value)
        game_cols_scale = tk.Scale(
            master=self.widget_manager.game_parameters_frame,
            from_=GameSizeParameters.min_cols.value,
            to=GameSizeParameters.max_cols.value,
            orient=tk.HORIZONTAL,
            variable=self.game_cols_n,
            command=self.game_cols_scale_command,
            background=Colour.col_scale_background.value,
            trough=Colour.col_scale_trough.value,
            showvalue=False,
        )
        return game_cols_scale

    def get_win_length_scale(self) -> ttk.Scale:
        """Method to produce the ttk scale object used by the user to select the required win length to play with."""
        self.win_length_k = tk.IntVar(value=GameSizeParameters.default_cols.value)
        win_length_scale = tk.Scale(
            master=self.widget_manager.game_parameters_frame,
            from_=GameSizeParameters.min_win_length.value,
            to=GameSizeParameters.default_win_length.value,  # Placeholder
            orient=tk.HORIZONTAL,
            variable=self.win_length_k,
            command=self.win_length_scale_command,
            background=Colour.win_scale_background.value,
            trough=Colour.win_scale_trough.value,
            showvalue=False,
        )
        return win_length_scale

    ##########
    # Commands for when the scales are moved
    ##########
    def game_rows_scale_command(self, event) -> None:
        """
        When the rows scale is pulled, the label is updated to show the relevant value.
        The win length is also updated accordingly, so that win length can never be longer than both rows and the cols.
        """
        # Update rows label
        value = self.game_rows_m.get()
        text = f"Rows: {value}"
        self.widget_manager.game_rows_label.configure(text=text)
        # Update win length if needed
        self.widget_manager.win_length_scale.configure(to=max(self.game_rows_m.get(), self.game_cols_n.get()))
        self.win_length_k.set(value=min(self.win_length_k.get(), max(self.game_rows_m.get(), self.game_cols_n.get())))
        self.win_length_scale_command(event=event)

    def game_cols_scale_command(self, event) -> None:
        """
        When the cols scale is pulled, the label is updated to show the relevant value
        The win length is also updated accordingly, so that win length can never be longer than both rows and the cols.
        """
        # Update cols label
        value = self.game_cols_n.get()
        text = f"Cols: {value}"
        self.widget_manager.game_cols_label.configure(text=text)
        # Update win length if needed
        self.widget_manager.win_length_scale.configure(to=max(self.game_rows_m.get(), self.game_cols_n.get()))
        self.win_length_k.set(value=min(self.win_length_k.get(), max(self.game_rows_m.get(), self.game_cols_n.get())))
        self.win_length_scale_command(event=event)

    def win_length_scale_command(self, event) -> None:
        """When the cols scale is pulled, the label is updated to show the relevant value"""
        win_length = self.win_length_k.get()
        text = f"Win length: {win_length}"
        self.widget_manager.win_length_label.configure(text=text)

    ##########
    # Labels displaying the value of the associate scale
    ##########
    def get_game_rows_label(self) -> ttk.Label:
        """Returns: A label showing the current number of rows to be played with."""
        game_rows_label = ttk.Label(
            master=self.widget_manager.game_parameters_frame,
            text=f"Rows: {GameSizeParameters.default_rows.value}",
            relief=Relief.row_col_win_labels.value,
            anchor=tk.CENTER,
            font=(Font.default_font.value, floor(SetupWindowDimensions.game_parameters_frame_cells.height / 4)),
            background=Colour.row_scale_trough.value
        )
        return game_rows_label

    def get_game_cols_label(self) -> ttk.Label:
        """Returns: A label showing the current number of cols to be played with."""
        game_cols_label = ttk.Label(
            master=self.widget_manager.game_parameters_frame,
            text=f"Columns: {GameSizeParameters.default_cols.value}",
            relief=Relief.row_col_win_labels.value,
            anchor=tk.CENTER,
            font=(Font.default_font.value, floor(SetupWindowDimensions.game_parameters_frame_cells.height / 4)),
            background=Colour.col_scale_background.value,
        )
        return game_cols_label

    def get_win_length_label(self) -> ttk.Label:
        """Returns: A label showing the current win length to be played with."""
        win_length_label = ttk.Label(
            master=self.widget_manager.game_parameters_frame,
            text=f"Win length: {GameSizeParameters.default_win_length.value}",
            relief=Relief.row_col_win_labels.value,
            anchor=tk.CENTER,
            font=(Font.default_font.value, floor(SetupWindowDimensions.game_parameters_frame_cells.height / 4)),
            background=Colour.win_scale_background.value
        )
        return win_length_label

# window = tk.Tk()
# frame = GameParametersFrame(widget_manager=GameSetupWidgets())
# frame.widget_manager.game_parameters_frame = tk.Frame(master=window)
# frame.populate_game_parameters_frame()
# frame.widget_manager.game_parameters_frame.pack()
# window.mainloop()