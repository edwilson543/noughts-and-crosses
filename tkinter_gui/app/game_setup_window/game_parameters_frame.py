from tkinter_gui.app.game_setup_window.game_setup_widget_manager import GameSetupWidgets
from tkinter_gui.constants.game_parameter_constraints import GameParameterConstraint
from tkinter_gui.constants.dimensions import SetupWindowDimensions
from tkinter_gui.constants.style_and_colours import Colour, Font, Relief

import tkinter as tk
from math import floor


class GameParametersFrame:
    """
    Class that fills the game setup_parameters (left-hand) frame on the setup menu.
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
        """Method that inserts all the labels/ scales into the game setup_parameters frame"""
        self._create_and_format_game_parameters_frame()
        self._upload_game_parameter_widgets_to_widget_manager()

        self.widget_manager.game_rows_scale.grid(row=1, column=0, rowspan=3, sticky="ns", padx=5, pady=5)
        self.widget_manager.game_cols_scale.grid(row=4, column=1, columnspan=4, sticky="ew", padx=5, pady=5)
        self.widget_manager.win_length_scale.grid(row=0, column=1, columnspan=4, sticky="ew", padx=5, pady=5)
        self.widget_manager.game_rows_label.grid(row=2, column=1, columnspan=4, sticky="nsew", padx=5, pady=5)
        self.widget_manager.game_cols_label.grid(row=3, column=1, columnspan=4, sticky="nsew", padx=5, pady=5)
        self.widget_manager.win_length_label.grid(row=1, column=1, columnspan=4, sticky="nsew", padx=5, pady=5)

    def _create_and_format_game_parameters_frame(self):
        """Method to format the game setup_parameters frame"""
        self.widget_manager.game_parameters_frame = tk.Frame(
            master=self.widget_manager.setup_window,
            background=Colour.game_parameters_frame_background.value,
            borderwidth=3, relief=Relief.game_parameters_frame.value
        )
        self.widget_manager.game_parameters_frame.rowconfigure(
            index=[0, 1, 2, 3, 4], weight=1,
            minsize=SetupWindowDimensions.game_parameters_frame_cells.height)
        self.widget_manager.game_parameters_frame.columnconfigure(
            index=[0, 1, 2, 3, 4], weight=1,
            minsize=SetupWindowDimensions.game_parameters_frame_cells.width)

    def _upload_game_parameter_widgets_to_widget_manager(self) -> None:
        """Method that adds all labels represented in this class to the widget manager"""
        self.widget_manager.game_rows_scale = self._get_game_rows_scale()
        self.widget_manager.game_cols_scale = self._get_game_cols_scale()
        self.widget_manager.win_length_scale = self._get_win_length_scale()
        self.widget_manager.game_rows_label = self._get_game_rows_label()
        self.widget_manager.game_cols_label = self._get_game_cols_label()
        self.widget_manager.win_length_label = self._get_win_length_label()

    ##########
    # Scale objects in the game setup_parameters frame
    ##########
    def _get_game_rows_scale(self) -> tk.Scale:
        """Method to produce the ttk scale object used by the user to select the number of rows to play with."""
        self.game_rows_m = tk.IntVar(value=GameParameterConstraint.default_rows.value)
        game_rows_scale = tk.Scale(
            master=self.widget_manager.game_parameters_frame,
            from_=GameParameterConstraint.min_rows.value,
            to=GameParameterConstraint.max_rows.value,
            orient=tk.VERTICAL,
            variable=self.game_rows_m,
            command=self._game_rows_scale_command,
            background=Colour.row_scale_background.value,
            trough=Colour.row_scale_trough.value,
            showvalue=False,
        )
        return game_rows_scale

    def _get_game_cols_scale(self) -> tk.Scale:
        """Method to produce the ttk scale object used by the user to select the number of columns to play with."""
        self.game_cols_n = tk.IntVar(value=GameParameterConstraint.default_cols.value)
        game_cols_scale = tk.Scale(
            master=self.widget_manager.game_parameters_frame,
            from_=GameParameterConstraint.min_cols.value,
            to=GameParameterConstraint.max_cols.value,
            orient=tk.HORIZONTAL,
            variable=self.game_cols_n,
            command=self._game_cols_scale_command,
            background=Colour.col_scale_background.value,
            trough=Colour.col_scale_trough.value,
            showvalue=False,
        )
        return game_cols_scale

    def _get_win_length_scale(self) -> tk.Scale:
        """Method to produce the ttk scale object used by the user to select the required win length to play with."""
        self.win_length_k = tk.IntVar(value=GameParameterConstraint.default_cols.value)
        win_length_scale = tk.Scale(
            master=self.widget_manager.game_parameters_frame,
            from_=GameParameterConstraint.min_win_length.value,
            to=GameParameterConstraint.default_win_length.value,  # Placeholder
            orient=tk.HORIZONTAL,
            variable=self.win_length_k,
            command=self._win_length_scale_command,
            background=Colour.win_scale_background.value,
            trough=Colour.win_scale_trough.value,
            showvalue=False,
        )
        return win_length_scale

    ##########
    # Commands for when the scales are moved
    ##########
    def _game_rows_scale_command(self, event) -> None:
        """
        When the rows scale is pulled, the label is updated to show the relevant value.
        The win length is also updated accordingly, so that win length can never be longer than both rows and the cols.
        Parameters:
        event - positional argument that represents the event of the slider moving
        """
        # Update rows label
        value = self.game_rows_m.get()
        text = f"Rows: {value}"
        self.widget_manager.game_rows_label.configure(text=text)
        # Update win length if needed
        self.widget_manager.win_length_scale.configure(to=max(self.game_rows_m.get(), self.game_cols_n.get()))
        self.win_length_k.set(value=min(self.win_length_k.get(), max(self.game_rows_m.get(), self.game_cols_n.get())))
        self._win_length_scale_command(event=event)

    def _game_cols_scale_command(self, event) -> None:
        """
        When the cols scale is pulled, the label is updated to show the relevant value
        The win length is also updated accordingly, so that win length can never be longer than both rows and the cols.
        Parameters:
        event - positional argument that represents the event of the slider moving
        """
        # Update cols label
        value = self.game_cols_n.get()
        text = f"Cols: {value}"
        self.widget_manager.game_cols_label.configure(text=text)
        # Update win length if needed
        self.widget_manager.win_length_scale.configure(to=max(self.game_rows_m.get(), self.game_cols_n.get()))
        self.win_length_k.set(value=min(self.win_length_k.get(), max(self.game_rows_m.get(), self.game_cols_n.get())))
        self._win_length_scale_command(event=event)

    def _win_length_scale_command(self, event) -> None:
        """
        When the cols scale is pulled, the label is updated to show the relevant value
        Parameters:
        event - positional argument that represents the event of the slider moving
        """
        win_length = self.win_length_k.get()
        text = f"Win length: {win_length}"
        self.widget_manager.win_length_label.configure(text=text)

    ##########
    # Labels displaying the value of the associate scale
    ##########
    def _get_game_rows_label(self) -> tk.Label:
        """Returns: A label showing the current number of rows to be played with."""
        game_rows_label = tk.Label(
            master=self.widget_manager.game_parameters_frame,
            text=f"Rows: {GameParameterConstraint.default_rows.value}",
            relief=Relief.row_col_win_labels.value,
            anchor=tk.CENTER,
            font=(Font.default_font.value, floor(SetupWindowDimensions.game_parameters_frame_cells.height / 3)),
            background=Colour.row_scale_trough.value
        )
        return game_rows_label

    def _get_game_cols_label(self) -> tk.Label:
        """Returns: A label showing the current number of cols to be played with."""
        game_cols_label = tk.Label(
            master=self.widget_manager.game_parameters_frame,
            text=f"Columns: {GameParameterConstraint.default_cols.value}",
            relief=Relief.row_col_win_labels.value,
            anchor=tk.CENTER,
            font=(Font.default_font.value, floor(SetupWindowDimensions.game_parameters_frame_cells.height / 3)),
            background=Colour.col_scale_background.value,
        )
        return game_cols_label

    def _get_win_length_label(self) -> tk.Label:
        """Returns: A label showing the current win length to be played with."""
        win_length_label = tk.Label(
            master=self.widget_manager.game_parameters_frame,
            text=f"Win length: {GameParameterConstraint.default_win_length.value}",
            relief=Relief.row_col_win_labels.value,
            anchor=tk.CENTER,
            font=(Font.default_font.value, floor(SetupWindowDimensions.game_parameters_frame_cells.height / 3)),
            background=Colour.win_scale_background.value
        )
        return win_length_label
