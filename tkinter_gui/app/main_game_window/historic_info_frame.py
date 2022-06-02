from game.app.game_base_class import NoughtsAndCrossesEssentialParameters
from game.app.player_base_class import Player
from tkinter_gui.app.main_game_window.main_game_widget_manager import MainWindowWidgetManager
from tkinter_gui.constants.style_and_colours import Colour, Font, Relief
from tkinter_gui.constants.dimensions import MainWindowDimensions
from math import floor
import tkinter as tk


class HistoricInfoFrame:
    """
    Frame that goes in the bottom right of the main main_window, and stores the players' win counts. and the draw count
    """
    def __init__(self,
                 setup_parameters: NoughtsAndCrossesEssentialParameters,
                 draw_count: int = 0,
                 widget_manager=MainWindowWidgetManager()):
        self.draw_count = draw_count
        self.player_x = setup_parameters.player_x
        self.player_o = setup_parameters.player_o
        self.widget_manager = widget_manager

    def populate_historic_info_frame(self) -> None:
        """Method to populate the historic info grid with the relevant labels"""
        self._create_and_format_historic_info_frame()
        self._upload_historic_info_frame_widgets_to_widget_manager()

        # Static widget that isn't in the widget manager
        game_win_count_label = self._get_game_win_count_label()
        game_win_count_label.grid(row=0, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)

        # Dynamic widgets already added to the widget manager
        self.widget_manager.player_x_win_count_label.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        self.widget_manager.player_o_win_count_label.grid(row=1, column=2, sticky="nsew", padx=5, pady=5)
        self.widget_manager.draw_count_label.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)

    def _create_and_format_historic_info_frame(self) -> None:
        """Method that formats the historic info frame and uploads it to the widget manager."""
        self.widget_manager.historic_info_frame = tk.Frame(
            master=self.widget_manager.background_frame, background=Colour.game_status_background.value,
            borderwidth=5, relief=tk.SUNKEN)
        self.widget_manager.historic_info_frame.rowconfigure(
            index=[0, 1], minsize=floor(MainWindowDimensions.historic_info_frame.height / 2), weight=1)
        self.widget_manager.historic_info_frame.columnconfigure(
            index=[0, 1, 2], minsize=floor(MainWindowDimensions.historic_info_frame.width / 2), weight=1)

    def _upload_historic_info_frame_widgets_to_widget_manager(self) -> None:
        """Method that uploads the player win count and draw count labels to the widget manager."""
        self.widget_manager.player_x_win_count_label = self.get_player_win_count_label(player=self.player_x)
        self.widget_manager.player_o_win_count_label = self.get_player_win_count_label(player=self.player_o)
        self.widget_manager.draw_count_label = self.get_draw_count_label()

    def _get_game_win_count_label(self) -> tk.Label:
        """
        Returns: A static label widget displaying the widget that goes above the player win count and draw count
        labels.
        """
        game_win_count_label = tk.Label(
            master=self.widget_manager.historic_info_frame,
            text="Game Win Count:",
            font=(Font.default_font.value, floor(MainWindowDimensions.historic_info_frame.height / 12)),
            background=Colour.game_win_count_label.value,
            foreground=Colour.game_win_count_font.value,
            relief=Relief.game_win_count_label.value
        )
        return game_win_count_label

    def get_player_win_count_label(self, player: Player) -> tk.Label:
        """
        Parameters: player - The player who's win count this label will be for.
        Returns: A label which counts the wins for the passed player.
        """
        player_win_count_label = tk.Label(
            master=self.widget_manager.historic_info_frame,
            text=player.win_count_label_text(),
            font=(Font.default_font.value, floor(MainWindowDimensions.historic_info_frame.height / 12)),
            background=Colour.game_win_count_label.value,
            foreground=Colour.game_win_count_font.value,
            relief=Relief.player_win_count_label.value
        )
        return player_win_count_label

    def get_draw_count_label(self) -> tk.Label:
        """Returns: The label that will display how many draws have been reached in the current game"""
        player_win_count_label = tk.Label(
            master=self.widget_manager.historic_info_frame,
            text=f"Draws:\n{self.draw_count}",
            font=(Font.default_font.value, floor(MainWindowDimensions.historic_info_frame.height / 12)),
            background=Colour.game_win_count_label.value,
            foreground=Colour.game_win_count_font.value,
            relief=Relief.player_win_count_label.value
        )
        return player_win_count_label
