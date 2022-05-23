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


# TODO look through and remove references to master frame - they are almost always not needed

class NoughtsAndCrossesGameFrames(NoughtsAndCrosses):
    def __init__(self,
                 game_rows_m: int,
                 game_cols_n: int,
                 win_length_k: int,
                 pos_player: Player,
                 neg_player: Player,
                 starting_player: GameValue = GameValue.X,
                 active_unconfirmed_cell: (int, int) = None,
                 widget_manager=MainWindowWidgetManager()):
        super().__init__(game_rows_m, game_cols_n, win_length_k, pos_player, neg_player, starting_player)
        self.active_unconfirmed_cell = active_unconfirmed_cell
        self.widget_manager = widget_manager
        self.min_cell_height = floor(FrameDimensions.game_frame.height / game_rows_m)
        self.min_cell_width = floor(FrameDimensions.game_frame.width / game_cols_n)

    ##########
    # Methods populating the two frames with the relevant buttons
    ##########
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

    def populate_game_info_grid(self) -> None:
        """
        Method that populates the game info grid with a confirmation button, and indication of who's turn it is.

        Parameters:
        ----------
        mater_frame: The frame that this grid will be packed into
        playing_grid_frame: The playing grid frame - the confirmation button must be able to communicate with the
        info grid.

        Returns: None

        """
        self.widget_manager.game_info_frame.rowconfigure(
            index=[0, 1, 2], minsize=floor(FrameDimensions.game_info_frame.height / 3))
        self.widget_manager.game_info_frame.columnconfigure(
            index=[0, 1, 2], minsize=floor(FrameDimensions.game_info_frame.width / 3))

        confirm_cell_choice_button = self.confirm_cell_choice_button()
        confirm_cell_choice_button.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")

        player_turn_label = self.player_turn_label()
        player_turn_label.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky="nsew")

        pos_player_label = self.player_label(pos_player=True)
        pos_player_label.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        neg_player_label = self.player_label(pos_player=False)
        neg_player_label.grid(row=1, column=2, padx=5, pady=5, sticky="nsew")

        # TODO add remaining features and format

    def clear_playing_grid(self) -> None:
        """Method to clear the playing grid at the end of a game and fill it with a new one"""
        for row_index in range(0, self.game_rows_m):
            for col_index in range(0, self.game_cols_n):
                self.widget_manager.playing_grid[row_index, col_index].destroy()
                available_cell_button = self.available_cell_button(
                    row_index=row_index, col_index=col_index)
                available_cell_button.grid(row=row_index, column=col_index, sticky="nsew", padx=1, pady=1)
                self.widget_manager.playing_grid[row_index, col_index] = available_cell_button

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
    # Commands for buttons on the playing grid
    ##########
    def available_cell_button_command(self, row_index: int, col_index: int) -> None:
        """
        Method to update the playing grid to highlight the unconfirmed cell choice, and revert a previous unconfirmed
        choice that has been rejected back to a button.

        Note this all needs to be contained within one method so that it can be added as the command function for the
        available_cell_button.
        """
        logging.info(f"Available cell button clicked at {row_index, col_index}")
        # Activate the confirmation button
        self.widget_manager.confirmation_button["state"] = tk.NORMAL

        logging.info(f"Existing active unconfirmed cell: {self.active_unconfirmed_cell}")
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

        # Set new unconfirmed cell to be the index, and place an unconfirmed cell choice button in it
        self.active_unconfirmed_cell = (row_index, col_index)
        unconfirmed_cell_choice_button = self.unconfirmed_cell_button()
        unconfirmed_cell_choice_button.grid(row=self.active_unconfirmed_cell[0],
                                            column=self.active_unconfirmed_cell[1],
                                            sticky="nsew", padx=1, pady=1)
        self.widget_manager.playing_grid[self.active_unconfirmed_cell] = unconfirmed_cell_choice_button
        logging.info(f"New unconfirmed cell created at: {self.active_unconfirmed_cell}")

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

        # Destroy existing unconfirmed cell choice button
        self.widget_manager.playing_grid[self.active_unconfirmed_cell].destroy()

        # Replace destroyed unconfirmed cell choice button with an available cell choice button
        available_cell_button = self.available_cell_button(
            row_index=self.active_unconfirmed_cell[0],
            col_index=self.active_unconfirmed_cell[1])
        available_cell_button.grid(row=self.active_unconfirmed_cell[0],
                                   column=self.active_unconfirmed_cell[1], sticky="nsew")
        self.widget_manager.playing_grid[self.active_unconfirmed_cell] = available_cell_button
        logging.info(f"New available cell button created at {self.active_unconfirmed_cell}")

        # Indicate that there is now no active unconfirmed cell and disable confirmation button
        self.active_unconfirmed_cell = None
        self.widget_manager.confirmation_button["state"] = tk.DISABLED

    ##########
    # Buttons and labels relating to the game_info_grid
    ##########

    def confirm_cell_choice_button(self) -> tk.Button:
        """
        Master button that confirms the user's choice and therefore initiates all backend processing.

        Parameters:
        __________
        None

        Returns:
        __________
        The formatted button
        """
        command_func = partial(self.confirm_cell_choice_button_command)
        confirm_cell_choice_button = tk.Button(
            master=self.widget_manager.game_info_frame,
            command=command_func,
            state=tk.DISABLED,
            background=Colour.unconfirmed_cell.value,
            foreground=Colour.info_panels_font.value,
            font=(Font.default_font.value, floor(FrameDimensions.game_info_frame.height / 10)),
            text="Confirm\nSelection")

        self.widget_manager.confirmation_button = confirm_cell_choice_button
        return confirm_cell_choice_button

    def player_turn_label(self) -> tk.Label:
        """
        Method to create a label that says "Player turn" above the coloured labels indicating who's turn it is.
        """
        player_turn_label = tk.Label(master=self.widget_manager.game_info_frame,
                                     text="Player's Turn:",
                                     relief=Relief.players_turn.value,
                                     background=Colour.players_turn_label.value,
                                     font=(Font.default_font.value, floor(FrameDimensions.game_info_frame.height / 10)))
        return player_turn_label

    def player_label(self, pos_player: bool) -> tk.Label:
        """
        Method to create the player label's and show who's turn it is to mark the board
        """
        if pos_player:
            player = self.pos_player
        else:
            player = self.neg_player
        x_or_o = GameValue(player.active_symbol).name
        text = f"{player.name}:\n{x_or_o}"
        colour = self.get_player_label_colour(player=player)
        relief = self.get_player_label_relief(player=player)
        player_label = tk.Label(master=self.widget_manager.game_info_frame,
                                text=text,
                                background=colour,
                                font=(Font.default_font.value, floor(FrameDimensions.game_info_frame.height / 10)),
                                relief=relief)
        if pos_player:
            self.widget_manager.pos_player_label = player_label
        else:
            self.widget_manager.neg_player_label = player_label
        return player_label

    ##########
    # Command function for the confirmation button in the game info grid
    ##########

    def confirm_cell_choice_button_command(self) -> None:
        """
        Master command to initiate all backend processing

        Method to:
        1) Permanently marks the board as shown in the active unconfirmed cell.
        2) Updates the backend board (the -1s, 0s and 1s) and checks whether a player has won
        3) Sets active_unconfirmed_cell to None
        4) Switch which player's label is highlighted/raised

        Parameters: None

        Returns: None
        """

        # Reset the cell choice button to disabled
        self.widget_manager.confirmation_button["state"] = tk.DISABLED

        # Permanently mark the board as shown in the active unconfirmed cell
        occupied_cell_label = self.occupied_cell_label()
        occupied_cell_label.grid(row=self.active_unconfirmed_cell[0], column=self.active_unconfirmed_cell[1],
                                 sticky="nsew")
        self.mark_board(row_index=self.active_unconfirmed_cell[0], col_index=self.active_unconfirmed_cell[1])
        self.active_unconfirmed_cell = None

        # Check for a win of the game
        winning_player = self.get_winning_player()
        if winning_player is not None:
            # TODO (longer) launch a TopLevel to see if they want to continue playing
            self.reset_game_board()  # backend
            self.clear_playing_grid()  # frontend
            # Reset the game and award the player a point
            if winning_player == self.pos_player:
                self.pos_player.award_point()
                self.widget_manager.pos_player_win_count_label.configure(
                    text=f"{self.pos_player.name}:\n{self.pos_player.active_game_win_count}"
                )
            # TODO each time the button is clicked, check whether a win has been achieved
            # And then update the win count labels accordingly and reset the board (both front and backend)
            pass

        # Switch which player's label is highlighted
        pos_player_label = self.widget_manager.pos_player_label
        neg_player_label = self.widget_manager.neg_player_label

        pos_player_label.configure(background=self.get_player_label_colour(player=self.pos_player),
                                   relief=self.get_player_label_relief(player=self.pos_player))
        neg_player_label.configure(background=self.get_player_label_colour(player=self.neg_player),
                                   relief=self.get_player_label_relief(player=self.neg_player))

    # Lower level methods used for formatting
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

    def get_player_label_colour(self, player: Player) -> str:
        """Highlights the player's label if it's there go, otherwise their label is not highlighted."""
        if self.get_player_turn() == player.active_symbol.value:
            return Colour.unconfirmed_cell.value
        else:
            return self.get_occupied_cell_colour(marking=GameValue(player.active_symbol).name)

    def get_player_label_relief(self, player: Player):
        """Raises the player's label if it's there go, otherwise their label is sunken."""
        if self.get_player_turn() == player.active_symbol.value:
            return Relief.active_player_label.value
        else:
            return Relief.inactive_player_label.value
