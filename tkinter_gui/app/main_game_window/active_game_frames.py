"""Module containing the playing grid and active game info (which containts the master conirmation button)"""

from game.app.game_base_class import NoughtsAndCrosses
from game.app.player_base_class import Player
from game.constants.game_constants import GameValue
from tkinter_gui.app.main_game_window.widget_management import MainWindowWidgetManager
from tkinter_gui.constants.dimensions import FrameDimensions
from tkinter_gui.constants.style_and_colours import Colour, Font, Relief
import tkinter as tk
from math import floor
from functools import partial
import numpy as np
import logging


class NoughtsAndCrossesGameFrames(NoughtsAndCrosses):
    def __init__(self,
                 game_rows_m: int,
                 game_cols_n: int,
                 win_length_k: int,
                 pos_player: Player,
                 neg_player: Player,
                 starting_player: GameValue = GameValue.X,
                 draw_count: int = 0,
                 active_unconfirmed_cell: (int, int) = None,
                 widget_manager=MainWindowWidgetManager()):
        super().__init__(game_rows_m, game_cols_n, win_length_k, pos_player, neg_player, starting_player, draw_count)
        self.active_unconfirmed_cell = active_unconfirmed_cell
        self.widget_manager = widget_manager
        self.min_cell_height = floor(FrameDimensions.game_frame.height / game_rows_m)
        self.min_cell_width = floor(FrameDimensions.game_frame.width / game_cols_n)

    ##########
    # Methods populating / clearing the two frames with the relevant buttons
    ##########
    def populate_game_info_grid(self) -> None:
        """
        Method that populates the game info grid with a confirmation button, and labels that indicate who's turn it is.
        The confirmation button is the master button that processes the game.

        Parameters: None
        Returns: None
        """
        self.widget_manager.game_info_frame.rowconfigure(
            index=[0, 1, 2], minsize=floor(FrameDimensions.game_info_frame.height / 3), weight=1)
        self.widget_manager.game_info_frame.columnconfigure(
            index=[0, 1], minsize=floor(FrameDimensions.game_info_frame.width / 2), weight=1)

        player_turn_label = self.player_turn_label()
        player_turn_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        pos_player_label = self.player_label(pos_player=True)
        pos_player_label.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        neg_player_label = self.player_label(pos_player=False)
        neg_player_label.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

        self.widget_manager.pos_player_confirmation_button = self.confirm_cell_choice_button()
        self.widget_manager.pos_player_confirmation_button.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
        self.widget_manager.neg_player_confirmation_button = self.confirm_cell_choice_button()
        self.widget_manager.neg_player_confirmation_button.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")
        self.initialise_confirmation_buttons()

    def populate_empty_playing_grid(self):
        """
        Loops over the playing grid and creates an analogous grid of selection buttons.
        Note that this is only called once at the start of the game, so all cells are empty.
        """
        self.widget_manager.playing_grid_frame.rowconfigure(
            index=list(range(0, self.game_rows_m)),
            minsize=self.min_cell_height,
            weight=1)
        self.widget_manager.playing_grid_frame.columnconfigure(
            index=list(range(0, self.game_cols_n)),
            minsize=self.min_cell_width,
            weight=1)
        self.widget_manager.playing_grid = np.empty(shape=(self.game_rows_m, self.game_cols_n), dtype=object)
        for row_index in range(0, self.game_rows_m):
            for col_index in range(0, self.game_cols_n):
                available_cell_button = self.available_cell_button(row_index=row_index, col_index=col_index)
                available_cell_button.grid(row=row_index, column=col_index, sticky="nsew", padx=1, pady=1)
                self.widget_manager.playing_grid[row_index, col_index] = available_cell_button

    def clear_playing_grid(self) -> None:
        """
        Method to clear the playing grid at the end of a game and fill it with a new one.
        All buttons and labels are removed, and a grid is populated with only available buttons.
        """
        for row_index in range(0, self.game_rows_m):
            for col_index in range(0, self.game_cols_n):
                self.widget_manager.playing_grid[row_index, col_index].destroy()
                available_cell_button = self.available_cell_button(
                    row_index=row_index, col_index=col_index)
                available_cell_button.grid(row=row_index, column=col_index, sticky="nsew", padx=1, pady=1)
                self.widget_manager.playing_grid[row_index, col_index] = available_cell_button

    ##########
    # Confirmation master button command method and sub-methods
    ##########
    def confirm_cell_choice_button_command(self) -> None:
        """
        Master command that is in effect the game loop.

        Method to:
        1) Disable the confirmation button as it has just been pressed
        2) Confirm the cell selection and carry out the necessary GUI and backend processing
        3) Check if this selection has resulted in a win/ draw and carry out the necessary processing
        4) Switch which player's label is highlighted/raised to indicate that it's their go

        Parameters: None
        Returns: None
        """
        self.confirmation_button_switch()
        self.confirm_cell_selection()
        self.end_of_game_check()
        self.switch_highlighted_confirmation_button()

    def confirmation_button_switch(self):
        """
        Method to switch which player's confirmation button is showing as active.
        Parameters:
        initiation: if this is the game initiation, then
        """
        if self.get_player_turn() == self.pos_player.active_symbol.value:
            self.widget_manager.active_confirmation_button["state"] = tk.DISABLED
            self.widget_manager.active_confirmation_button = self.widget_manager.neg_player_confirmation_button
        else:
            self.widget_manager.active_confirmation_button["state"] = tk.DISABLED
            self.widget_manager.active_confirmation_button = self.widget_manager.pos_player_confirmation_button

    def confirm_cell_selection(self) -> None:
        """
        Method to:
        1) Destroy the in-place unconfirmed cell button
        2) Permanently marks the board as shown in the active unconfirmed cell.
        3) Updates the backend board (the -1s, 0s and 1s) and checks whether a player has won
        4) Sets active_unconfirmed_cell to None
        """
        self.widget_manager.playing_grid[self.active_unconfirmed_cell].destroy()
        occupied_cell_label = self.occupied_cell_label()
        occupied_cell_label.grid(row=self.active_unconfirmed_cell[0], column=self.active_unconfirmed_cell[1],
                                 sticky="nsew")
        self.mark_board(row_index=self.active_unconfirmed_cell[0], col_index=self.active_unconfirmed_cell[1])
        self.active_unconfirmed_cell = None

    def end_of_game_check(self) -> None:
        """
        Method called each time the confirm button is clicked, to:
        1) Determine whether the game has been won, and award the winner a point if so.
        2) Check if the game has reached stalemate (a draw)
        """
        winning_player = self.get_winning_player()
        if winning_player is not None:
            # TODO could launch a TopLevel to see if they want to continue playing, winner or loser starts
            # TODO can also make the winning streak flash and dance
            self.starting_player = self.get_player_turn()
            self.reset_game_board()  # backend
            self.clear_playing_grid()  # frontend

            if winning_player == self.pos_player:
                self.pos_player.award_point()
                self.widget_manager.pos_player_win_count_label.configure(
                    text=self.pos_player.win_count_label_text())
            elif winning_player == self.neg_player:
                self.neg_player.award_point()
                self.widget_manager.neg_player_win_count_label.configure(
                    text=self.neg_player.win_count_label_text())
            else:
                raise ValueError(
                    "winning_player is not None in end_of_game check but neither player is equal to the"
                    "winning player.")
        elif self.check_for_draw():
            self.reset_game_board()  # backend
            self.clear_playing_grid()  # frontend
            self.widget_manager.draw_count_label.configure(text=f"Draws:\n{self.draw_count}")

    ##########
    # Playing grid button commands
    ##########
    def available_cell_button_command(self, row_index: int, col_index: int) -> None:
        """
        Method to update the playing grid to highlight the unconfirmed cell choice, and revert a previous unconfirmed
        choice that has been rejected back to an available cell button.
        """
        logging.info(f"Available cell button clicked at {row_index, col_index}")
        # Activate the confirmation button
        self.widget_manager.active_confirmation_button["state"] = tk.NORMAL

        # Destroy exiting cell and replace with an available cell
        self.replace_existing_unconfirmed_cell(row_index=row_index, col_index=col_index)

        # Destroy existing available cell and replace with an unconfirmed cell button
        self.replace_existing_available_cell(row_index=row_index, col_index=col_index)

    def unconfirmed_cell_choice_button_command(self) -> None:
        """
        Method to define what happens when the unconfirmed cell choice button is clicked.
        An available cell button is inserted in place of the unconfirmed cell choice button.
        Also, the active_unconfirmed_cell is set to None as there is no longer an active unconfirmed cell.

        Purpose:
        1) Two clicks on an empty cell highlights and then un-highlights that cell
        2) To be part of the command when a new available cell is chosen as the active unconfirmed cell (i.e. first have
        to remove the existing unconfirmed cell)
        """

        logging.info(f"Unconfirmed cell choice button clicked at {self.active_unconfirmed_cell}")
        self.replace_existing_unconfirmed_cell(
            row_index=self.active_unconfirmed_cell[0], col_index=self.active_unconfirmed_cell[1])
        self.active_unconfirmed_cell = None
        self.widget_manager.active_confirmation_button["state"] = tk.DISABLED

    def replace_existing_available_cell(self, row_index: int, col_index: int):
        """Method to destroy an existing available cell and replace it with an unconfirmed cell button."""
        # Destroy existing available cell
        self.widget_manager.playing_grid[row_index, col_index].destroy()
        # Replace with unconfirmed cell
        self.active_unconfirmed_cell = (row_index, col_index)
        unconfirmed_cell_choice_button = self.unconfirmed_cell_button()
        unconfirmed_cell_choice_button.grid(row=self.active_unconfirmed_cell[0],
                                            column=self.active_unconfirmed_cell[1],
                                            sticky="nsew", padx=1, pady=1)
        self.widget_manager.playing_grid[self.active_unconfirmed_cell] = unconfirmed_cell_choice_button
        logging.info(f"New unconfirmed cell created at: {self.active_unconfirmed_cell}")

    def replace_existing_unconfirmed_cell(self, row_index: int, col_index: int):
        """Method to destroy the existing unconfirmed cell button and replace it with an available cell button."""
        if self.active_unconfirmed_cell is not None:
            # Destroy existing active unconfirmed cell choice button
            self.widget_manager.playing_grid[self.active_unconfirmed_cell].destroy()

            # Replace destroyed unconfirmed cell choice button with an available cell button
            available_cell_button = self.available_cell_button(
                row_index=self.active_unconfirmed_cell[0],
                col_index=self.active_unconfirmed_cell[1])
            available_cell_button.grid(row=self.active_unconfirmed_cell[0],
                                       column=self.active_unconfirmed_cell[1], sticky="nsew")
            self.widget_manager.playing_grid[self.active_unconfirmed_cell] = available_cell_button
            logging.info(f"New available cell button created at: {row_index, col_index}")

    ##########
    # Labels/ buttons on the playing grid
    ##########

    def occupied_cell_label(self) -> tk.Label:
        """Label widget that shows that a cell is already occupied and displays the relevant marking."""
        text = self.get_player_turn_marking()
        colour = self.get_occupied_cell_colour(marking=text)
        occupied_cell_label = tk.Label(
            master=self.widget_manager.playing_grid_frame,
            text=text,  # X or O
            font=(Font.xo_font.value, floor(self.min_cell_height / 3)),
            background=colour, relief=Relief.occupied_cell.value)
        return occupied_cell_label

    def unconfirmed_cell_button(self) -> tk.Button:
        """Label widget that shows that a cell has temporarily been selected as the player's move."""
        command_func = partial(self.unconfirmed_cell_choice_button_command)
        text = self.get_player_turn_marking()
        unconfirmed_cell_choice_button = tk.Button(
            master=self.widget_manager.playing_grid_frame,
            command=command_func,
            text=text,
            font=(Font.xo_font.value, floor(self.min_cell_height / 3)),
            background=Colour.unconfirmed_cell.value, relief=Relief.unconfirmed_cell.value,
            foreground=Colour.unconfirmed_cell_font.value)
        return unconfirmed_cell_choice_button

    def available_cell_button(self, row_index: int, col_index: int) -> tk.Button:
        """Button widget that shows that a cell is available for selection"""
        command_func = partial(self.available_cell_button_command, row_index, col_index)
        available_cell_button = tk.Button(
            master=self.widget_manager.playing_grid_frame,
            command=command_func,
            background=Colour.available_cell.value, relief=Relief.available_cell.value)
        return available_cell_button

    ##########
    # Buttons and labels relating to the game_info_grid
    ##########
    def confirm_cell_choice_button(self) -> tk.Button:
        """
        Master button that confirms the user's choice and therefore initiates all backend processing.
        Returns: The formatted button object
        """
        command_func = partial(self.confirm_cell_choice_button_command)
        confirm_cell_choice_button = tk.Button(
            master=self.widget_manager.game_info_frame,
            command=command_func,
            state=tk.DISABLED,
            foreground=Colour.info_panels_font.value,
            font=(Font.default_font.value, floor(FrameDimensions.game_info_frame.height / 10)),
            text="Confirm")

        return confirm_cell_choice_button

    def player_turn_label(self) -> tk.Label:
        """
        Method to create a label that says "Player turn" above the coloured labels indicating who's turn it is.
        Returns: The formatted label object
        """
        player_turn_label = tk.Label(master=self.widget_manager.game_info_frame,
                                     text="Player's Turn:",
                                     relief=Relief.players_turn.value,
                                     background=Colour.players_turn_label.value,
                                     font=(Font.default_font.value, floor(FrameDimensions.game_info_frame.height / 10)))
        return player_turn_label

    def player_label(self, pos_player: bool) -> tk.Label:
        """
        Method to create the player label's and show who's turn it is to take a turn at marking the board
        """
        if pos_player:
            player = self.pos_player
        else:
            player = self.neg_player
        x_or_o = GameValue(player.active_symbol).name
        text = f"{player.name}:\n{x_or_o}"
        colour = self.get_occupied_cell_colour(marking=player.active_symbol.name)
        player_label = tk.Label(master=self.widget_manager.game_info_frame,
                                text=text,
                                background=colour,
                                font=(Font.default_font.value, floor(FrameDimensions.game_info_frame.height / 10)),
                                relief=Relief.player_labels.value)
        if pos_player:
            self.widget_manager.pos_player_label = player_label
        else:
            self.widget_manager.neg_player_label = player_label
        return player_label

    # Lower level methods used for game processing
    def initialise_confirmation_buttons(self) -> None:
        """Method that decides which confirmation button should be active at the start of the game."""
        self.widget_manager.pos_player_confirmation_button.configure(
            background=self.get_player_confirmation_button_colour(player=self.pos_player))
        self.widget_manager.neg_player_confirmation_button.configure(
            background=self.get_player_confirmation_button_colour(player=self.neg_player))
        if self.starting_player == self.neg_player.active_symbol.value:
            self.widget_manager.active_confirmation_button = self.widget_manager.neg_player_confirmation_button
        else:
            self.widget_manager.active_confirmation_button = self.widget_manager.pos_player_confirmation_button

    #  Lower level methods used for formatting
    def get_player_turn_marking(self) -> str:
        """Method to extract the player turn from the game baseclass as a 1/-1 and return it as an X or O."""
        turn_int = self.get_player_turn()
        return GameValue(turn_int).name

    @staticmethod
    def get_occupied_cell_colour(marking: str) -> str:
        """Method to take an X or O and then select the relevant colour"""
        if marking == "X":
            return Colour.occupied_cell_x.value
        else:
            return Colour.occupied_cell_o.value

    def switch_highlighted_confirmation_button(self):
        """Method to flick between who's cell is highlighted depending on who's go it is"""
        self.widget_manager.pos_player_confirmation_button.configure(
            background=self.get_player_confirmation_button_colour(player=self.pos_player),
            relief=self.get_player_confirmation_button_relief(player=self.pos_player))
        self.widget_manager.neg_player_confirmation_button.configure(
            background=self.get_player_confirmation_button_colour(player=self.neg_player),
            relief=self.get_player_confirmation_button_relief(player=self.neg_player))

    def get_player_confirmation_button_colour(self, player: Player) -> str:
        """Highlights the player's label if it's their go, otherwise their label is not highlighted."""
        if self.get_player_turn() == player.active_symbol.value:
            return Colour.unconfirmed_cell.value
        else:
            return self.get_occupied_cell_colour(marking=GameValue(player.active_symbol).name)

    def get_player_confirmation_button_relief(self, player: Player):
        """Raises the player's label if it's there go, otherwise their label is sunken."""
        if self.get_player_turn() == player.active_symbol.value:
            return Relief.active_player_confirmation_button.value
        else:
            return Relief.inactive_player_confirmation_button.value
