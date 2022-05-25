from game.app.player_base_class import Player
from tkinter_gui.app.main_game_window.main_game_widget_manager import MainWindowWidgetManager
from tkinter_gui.constants.style_and_colours import Colour, Font, Relief
from tkinter_gui.constants.dimensions import MainWindowDimensions
from math import floor
import tkinter as tk


class HistoricInfoFrame:
    """
    Frame that goes in the bottom right of the main main_window, and stores the players' win counts.
    """

    def __init__(self,
                 pos_player: Player,
                 neg_player: Player,
                 widget_manager=MainWindowWidgetManager()):
        self.pos_player = pos_player
        self.neg_player = neg_player
        self.widget_manager = widget_manager

    def populate_historic_info_grid(self) -> None:
        """Method to populate the historic info grid with the relevant labels"""

        self.widget_manager.historic_info_frame.rowconfigure(
            index=[0, 1], minsize=floor(MainWindowDimensions.historic_info_frame.height / 2), weight=1)
        self.widget_manager.historic_info_frame.columnconfigure(
            index=[0, 1, 2], minsize=floor(MainWindowDimensions.historic_info_frame.width / 2), weight=1)

        game_win_count_label = self.get_game_win_count_label()
        game_win_count_label.grid(row=0, column=0, columnspan=3, sticky="nsew", padx=5, pady=5)

        self.widget_manager.pos_player_win_count_label = self.get_player_win_count_label(player=self.pos_player)
        self.widget_manager.pos_player_win_count_label.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        self.widget_manager.neg_player_win_count_label = self.get_player_win_count_label(player=self.neg_player)
        self.widget_manager.neg_player_win_count_label.grid(row=1, column=2, sticky="nsew", padx=5, pady=5)

        self.widget_manager.draw_count_label = self.get_draw_count_label()
        self.widget_manager.draw_count_label.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)

    def get_game_win_count_label(self) -> tk.Label:
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
        player_win_count_label = tk.Label(
            master=self.widget_manager.historic_info_frame,
            text="Draws:\n0",
            font=(Font.default_font.value, floor(MainWindowDimensions.historic_info_frame.height / 12)),
            background=Colour.game_win_count_label.value,
            foreground=Colour.game_win_count_font.value,
            relief=Relief.player_win_count_label.value
        )
        return player_win_count_label
