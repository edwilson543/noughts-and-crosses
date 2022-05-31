"""Module containing the playing grid and active game info frame (which contains the master confirmation buttons)"""

from game.app.game_base_class import NoughtsAndCrosses, NoughtsAndCrossesEssentialParameters
from game.app.player_base_class import Player
from game.constants.game_constants import BoardMarking
from tkinter_gui.app.main_game_window.main_game_widget_manager import MainWindowWidgetManager
from tkinter_gui.app.game_continuation_window.game_continuation_window import GameContinuationPopUp
from tkinter_gui.constants.dimensions import MainWindowDimensions
from tkinter_gui.constants.style_and_colours import Colour, Font, Relief
import tkinter as tk
from math import floor
from functools import partial
import numpy as np
import logging


# TODO how can the popup be launched in end_of_game_check and still show the playing_grid status?? i.e. before clearing playing_grid
# Just putting it before clearing the playing_grid means the playing_grid doesn't get cleared for some reason
# One way is to have the popup window defined within this module, so that it can have an active game frames attribute


class ActiveGameFrames(NoughtsAndCrosses):
    def __init__(self,
                 setup_parameters: NoughtsAndCrossesEssentialParameters,
                 draw_count: int = 0,
                 active_unconfirmed_cell: (int, int) = None,
                 widget_manager=MainWindowWidgetManager()):
        super().__init__(setup_parameters, draw_count)
        self.active_unconfirmed_cell = active_unconfirmed_cell
        self.widget_manager = widget_manager
        self.min_cell_height = floor(MainWindowDimensions.game_frame.height / setup_parameters.game_rows_m)
        self.min_cell_width = floor(MainWindowDimensions.game_frame.width / setup_parameters.game_cols_n)

    ##########
    # Methods populating and formatting the two active frames with the relevant widgets
    ##########
    # Game info frame
    def populate_game_info_frame(self) -> None:
        """
        Method that populates the game info grid with a confirmation button, and labels that indicate who's turn it is.
        The confirmation button is the master button that processes the game.
        """
        self._create_and_format_game_info_frame()
        self._upload_game_info_widgets_to_widget_manager()

        # Static widget that therefore isn't in the widget manager
        player_turn_label = self._get_player_turn_label()
        player_turn_label.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        # Dynamic widgets already added to the widget manager
        self.widget_manager.player_x_label.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        self.widget_manager.player_o_label.grid(row=1, column=1, padx=5, pady=5, sticky="nsew")

        self.widget_manager.player_x_confirmation_button.grid(row=2, column=0, padx=5, pady=5, sticky="nsew")
        self.widget_manager.player_o_confirmation_button.grid(row=2, column=1, padx=5, pady=5, sticky="nsew")
        self._initialise_confirmation_buttons()

    def _create_and_format_game_info_frame(self) -> None:
        """
        Method to format the game info frame (top-right) of the main playing window,
        and upload it to the widget manager.
        """
        self.widget_manager.game_info_frame = tk.Frame(
            master=self.widget_manager.background_frame, background=Colour.game_buttons_background.value,
            borderwidth=5, relief=tk.SUNKEN)
        self.widget_manager.game_info_frame.rowconfigure(
            index=[0, 1, 2], minsize=floor(MainWindowDimensions.game_info_frame.height / 3), weight=1)
        self.widget_manager.game_info_frame.columnconfigure(
            index=[0, 1], minsize=floor(MainWindowDimensions.game_info_frame.width / 2), weight=1)

    def _upload_game_info_widgets_to_widget_manager(self) -> None:
        """Method that links all of the dynamic widgets in the game info frame into the widget manager"""
        self.widget_manager.player_x_label = self._get_player_label(player=self.player_x)
        self.widget_manager.player_o_label = self._get_player_label(player=self.player_o)

        self.widget_manager.player_x_confirmation_button = self._get_confirm_cell_choice_button()
        self.widget_manager.player_o_confirmation_button = self._get_confirm_cell_choice_button()

    # playing grid frame
    def populate_empty_playing_grid_frame(self) -> None:
        """
        Method to loop through each index of the playing grid and create a GUI grid of selection buttons.
        Note that this is only called once at the start of the game, so all cells are empty - updates are made by
        clicking the buttons.
        """
        self._create_and_format_playing_grid_frame()
        self.widget_manager.playing_grid = np.empty(
            shape=(self.game_rows_m, self.game_cols_n), dtype=object)
        for row_index in range(0, self.game_rows_m):
            for col_index in range(0, self.game_cols_n):
                available_cell_button = self._get_available_cell_button(row_index=row_index, col_index=col_index)
                available_cell_button.grid(row=row_index, column=col_index, sticky="nsew", padx=1, pady=1)
                self.widget_manager.playing_grid[row_index, col_index] = available_cell_button

    def _create_and_format_playing_grid_frame(self) -> None:
        """
        Method to format the playing grid that will be filled with cell buttons and markings, and upload it to the
        widget manager.
        """
        self.widget_manager.playing_grid_frame = tk.Frame(
            master=self.widget_manager.background_frame, background=Colour.game_background.value,
            borderwidth=5, relief=Relief.playing_grid_frame.value)
        self.widget_manager.playing_grid_frame.rowconfigure(
            index=list(range(0, self.game_rows_m)),
            minsize=self.min_cell_height,
            weight=1)
        self.widget_manager.playing_grid_frame.columnconfigure(
            index=list(range(0, self.game_cols_n)),
            minsize=self.min_cell_width,
            weight=1)

    ##########
    # Confirmation master buttons command method and sub-methods
    ##########
    def _confirmation_buttons_command(self) -> None:
        """
        Master command that is in effect the game loop - i.e. clicking one of the confirmation buttons triggers the
        processing to determine what happens next in the game.

        Outcomes:
        1) Disable the confirmation button that has just been pressed (as there is 1 for each player)
        2) Confirm the cell selection and carry out the necessary GUI and backend processing to mark that cell
        3) Check if this selection has resulted in a win/ draw and carry out the necessary processing
        4) Switch which player's label is highlighted/raised to indicate that it's their go

        Parameters: None
        Returns: None
        """
        self._confirmation_button_switch()
        self._confirm_cell_selection()
        self._switch_highlighted_confirmation_button()
        self._end_of_game_check_pop_up()  # TODO re-order 1234 as above

    def _confirmation_button_switch(self):
        """
        Method to switch which player's confirmation button is active - to the player who's turn it is.
        This will disable the player's button who has just gone, and then set the active confirmation button in the
        widget manager to be that of the next player. A click on the playing_grid in an available cell then activates the
        confirmation button corresponding to who's turn it is.
        """
        if self.get_player_turn() == BoardMarking.X.value:
            self.widget_manager.active_confirmation_button["state"] = tk.DISABLED
            self.widget_manager.active_confirmation_button = self.widget_manager.player_o_confirmation_button
        else:
            self.widget_manager.active_confirmation_button["state"] = tk.DISABLED
            self.widget_manager.active_confirmation_button = self.widget_manager.player_x_confirmation_button

    def _confirm_cell_selection(self) -> None:
        """
        Method to:
        1) Destroy the in-place unconfirmed cell button
        2) Permanently marks the playing_grid as shown in the active unconfirmed cell.
        3) Updates the backend playing_grid (the -1s, 0s and 1s) and checks whether a player has won
        4) Sets active_unconfirmed_cell to None
        """
        self.widget_manager.playing_grid[self.active_unconfirmed_cell].destroy()
        occupied_cell_label = self._get_occupied_cell_label()
        occupied_cell_label.grid(row=self.active_unconfirmed_cell[0], column=self.active_unconfirmed_cell[1],
                                 sticky="nsew")
        self.mark_board(row_index=self.active_unconfirmed_cell[0], col_index=self.active_unconfirmed_cell[1])
        self.active_unconfirmed_cell = None
        self.widget_manager.main_window.update()  # So that the cell updates straight away

    def _end_of_game_check_pop_up(self) -> None:
        """
        Method called each time the confirm button is clicked, to:
        0) Reset the game playing_grid to a starting state, with the loser going first
        1) Determine whether the game has been won, and award the winner a point if so.
        2) Check if the game has reached stalemate (a draw)
        3) Produce a pop up asking the user to continue or exit depending if either of these is the case
        """
        winning_player = self.get_winning_player()
        if winning_player is not None:
            # TODO could make the winning streak flash and dance - would need to update the order though so the popup
            # is first, and the search algorithm actually returns the position of the win
            # TODO could give user option to let winner/random go first
            self.reset_game_board()  # backend
            self._clear_playing_grid()  # frontend

            if winning_player == self.player_x:
                self.starting_player_value = BoardMarking.O.value  # Loser starts next game
                self.player_x.award_point()
                self.widget_manager.player_x_win_count_label.configure(
                    text=self.player_x.win_count_label_text())
            elif winning_player == self.player_o:
                self.starting_player_value = BoardMarking.X.value
                self.player_o.award_point()
                self.widget_manager.player_o_win_count_label.configure(
                    text=self.player_o.win_count_label_text())
            else:
                raise ValueError(
                    "winning_player is not None in end_of_game check but neither player is equal to the"
                    "winning player.")
            self._initialise_confirmation_buttons()
            pop_up = GameContinuationPopUp(text=f"{winning_player.name} wins!", widget_manager=self.widget_manager)
            pop_up.launch_continuation_pop_up()

        elif self.check_for_draw():
            self.reset_game_board()  # backend
            self._clear_playing_grid()  # frontend
            self.widget_manager.draw_count_label.configure(text=f"Draws:\n{self.draw_count}")
            self._initialise_confirmation_buttons()
            pop_up = GameContinuationPopUp(text="Game ended in a draw", widget_manager=self.widget_manager)
            pop_up.launch_continuation_pop_up()

    def _clear_playing_grid(self) -> None:
        """
        Method to clear the playing grid at the end of a game and fill it with a new one. (GUI grid only)
        All buttons and labels are removed, and a grid is populated with only available buttons.
        """
        for row_index in range(0, self.game_rows_m):
            for col_index in range(0, self.game_cols_n):
                self.widget_manager.playing_grid[row_index, col_index].destroy()
                available_cell_button = self._get_available_cell_button(
                    row_index=row_index, col_index=col_index)
                available_cell_button.grid(row=row_index, column=col_index, sticky="nsew", padx=1, pady=1)
                self.widget_manager.playing_grid[row_index, col_index] = available_cell_button

    def _initialise_confirmation_buttons(self) -> None:
        """
        Method that decides which confirmation button should be the active confirmation button at the start of a new
        game.
        """
        self.widget_manager.player_x_confirmation_button.configure(
            background=self._get_player_confirmation_button_colour(player=self.player_x))
        self.widget_manager.player_o_confirmation_button.configure(
            background=self._get_player_confirmation_button_colour(player=self.player_o))
        if self.starting_player_value == BoardMarking.X.value:
            self.widget_manager.active_confirmation_button = self.widget_manager.player_x_confirmation_button
        elif self.starting_player_value == BoardMarking.O.value:
            self.widget_manager.active_confirmation_button = self.widget_manager.player_o_confirmation_button
        else:
            raise ValueError(f"Invalid starting_player_value identified in initialise_confirmation_buttons")

    ##########
    # Playing grid button commands
    ##########
    def _available_cell_button_command(self, row_index: int, col_index: int) -> None:
        """
        Method to update the playing grid to highlight the unconfirmed cell choice, and revert a previous unconfirmed
        choice that has been rejected back to an available cell button.
        """
        logging.info(f"Available cell button clicked at {row_index, col_index}")
        # Activate the confirmation button
        self.widget_manager.active_confirmation_button["state"] = tk.NORMAL

        # Destroy exiting cell and replace with an available cell
        self._replace_existing_unconfirmed_cell(row_index=row_index, col_index=col_index)

        # Destroy existing available cell and replace with an unconfirmed cell button
        self._replace_existing_available_cell(row_index=row_index, col_index=col_index)

    def _unconfirmed_cell_choice_button_command(self) -> None:
        """
        Method to define what happens when the unconfirmed cell choice button is clicked.

        1) Two clicks on an empty cell highlights and then un-highlights that cell (An available cell button is
        inserted in place of the unconfirmed cell choice button.)
        2) To be part of the command when a new available cell is chosen as the active unconfirmed cell (i.e. first have
        to remove the existing unconfirmed cell)
        """
        logging.info(f"Unconfirmed cell choice button clicked at {self.active_unconfirmed_cell}")
        self._replace_existing_unconfirmed_cell(
            row_index=self.active_unconfirmed_cell[0], col_index=self.active_unconfirmed_cell[1])
        self.active_unconfirmed_cell = None
        self.widget_manager.active_confirmation_button["state"] = tk.DISABLED

    def _replace_existing_available_cell(self, row_index: int, col_index: int):
        """Method to destroy an existing available cell and replace it with an unconfirmed cell button."""
        # Destroy existing available cell
        self.widget_manager.playing_grid[row_index, col_index].destroy()
        # Replace with unconfirmed cell
        self.active_unconfirmed_cell = (row_index, col_index)
        unconfirmed_cell_choice_button = self._get_unconfirmed_cell_button()
        unconfirmed_cell_choice_button.grid(row=self.active_unconfirmed_cell[0],
                                            column=self.active_unconfirmed_cell[1],
                                            sticky="nsew", padx=1, pady=1)
        self.widget_manager.playing_grid[self.active_unconfirmed_cell] = unconfirmed_cell_choice_button
        logging.info(f"New unconfirmed cell created at: {self.active_unconfirmed_cell}")

    def _replace_existing_unconfirmed_cell(self, row_index: int, col_index: int):
        """Method to destroy the existing unconfirmed cell button and replace it with an available cell button."""
        if self.active_unconfirmed_cell is not None:
            # Destroy existing active unconfirmed cell choice button
            self.widget_manager.playing_grid[self.active_unconfirmed_cell].destroy()

            # Replace destroyed unconfirmed cell choice button with an available cell button
            available_cell_button = self._get_available_cell_button(
                row_index=self.active_unconfirmed_cell[0],
                col_index=self.active_unconfirmed_cell[1])
            available_cell_button.grid(row=self.active_unconfirmed_cell[0],
                                       column=self.active_unconfirmed_cell[1], sticky="nsew")
            self.widget_manager.playing_grid[self.active_unconfirmed_cell] = available_cell_button
            logging.info(f"New available cell button created at: {row_index, col_index}")

    ##########
    # Labels/ buttons on the playing grid
    ##########
    def _get_occupied_cell_label(self) -> tk.Label:
        """
        Label widget that shows that a cell is already occupied and displays the relevant marking.
        Returns: A label which represents a marking on the playing_grid (an X or an O), and also of a different colour.
        """
        text = self._get_player_turn_marking()  # X or O
        colour = self._get_occupied_cell_colour(marking=text)
        occupied_cell_label = tk.Label(
            master=self.widget_manager.playing_grid_frame,
            text=text,
            font=(Font.xo_font.value, floor(self.min_cell_height / 3)),
            background=colour, relief=Relief.occupied_cell.value)
        return occupied_cell_label

    def _get_unconfirmed_cell_button(self) -> tk.Button:
        """
        Label widget that shows that a cell has temporarily been selected as the player's move.
        Returns: A highlighted button to show the user what button they have selected
        """
        text = self._get_player_turn_marking()
        unconfirmed_cell_choice_button = tk.Button(
            master=self.widget_manager.playing_grid_frame,
            command=self._unconfirmed_cell_choice_button_command,
            text=text,
            font=(Font.xo_font.value, floor(self.min_cell_height / 3)),
            background=Colour.unconfirmed_cell.value, relief=Relief.unconfirmed_cell.value,
            foreground=Colour.unconfirmed_cell_font.value)
        return unconfirmed_cell_choice_button

    def _get_available_cell_button(self, row_index: int, col_index: int) -> tk.Button:
        """
        Button widget that shows that a cell is available for selection
        Returns: A button which indicates that the user can click there to select that cell.
        """
        command_func = partial(self._available_cell_button_command, row_index, col_index)
        available_cell_button = tk.Button(
            master=self.widget_manager.playing_grid_frame,
            command=command_func,
            background=Colour.available_cell.value, relief=Relief.available_cell.value)
        return available_cell_button

    ##########
    # Buttons and labels relating to the game_info_grid
    ##########
    def _get_confirm_cell_choice_button(self) -> tk.Button:
        """
        Master button that confirms the user's choice and therefore initiates all backend processing. (Note the callback
        is defined higher up as it's a bigger deal

        Returns: The formatted button object
        """
        confirm_cell_choice_button = tk.Button(
            master=self.widget_manager.game_info_frame,
            command=self._confirmation_buttons_command,
            state=tk.DISABLED,
            foreground=Colour.info_panels_font.value,
            font=(Font.default_font.value, floor(MainWindowDimensions.game_info_frame.height / 10)),
            text="Confirm")
        return confirm_cell_choice_button

    def _get_player_turn_label(self) -> tk.Label:
        """
        Method to create a label that says "Player turn" above the coloured labels indicating who's turn it is.
        Returns: The static label widget that says Player's Turn above each of the player names and confirmation buttons
        """
        player_turn_label = tk.Label(
            master=self.widget_manager.game_info_frame,
            text="Player's Turn:",
            relief=Relief.players_turn.value,
            background=Colour.players_turn_label.value,
            font=(Font.default_font.value, floor(MainWindowDimensions.game_info_frame.height / 10)))
        return player_turn_label

    def _get_player_label(self, player: Player) -> tk.Label:
        """
        Method to create the player label's and show who's turn it is to take a turn at marking the playing_grid
        Parameters: player - indicates which player we are creating the label for, player_x or player_o
        """
        x_or_o = BoardMarking(player.marking).name
        text = f"{player.name}:\n{x_or_o}"
        colour = self._get_occupied_cell_colour(marking=player.marking.name)
        player_label = tk.Label(master=self.widget_manager.game_info_frame,
                                text=text,
                                background=colour,
                                font=(Font.default_font.value, floor(MainWindowDimensions.game_info_frame.height / 10)),
                                relief=Relief.player_labels.value)
        return player_label

    #  Lower level methods used for formatting updates during the game
    def _get_player_turn_marking(self) -> str:
        """Method to extract the player turn from the game baseclass as a 1/-1 and return it as an X or O."""
        turn_int = self.get_player_turn()
        return BoardMarking(turn_int).name

    @staticmethod
    def _get_occupied_cell_colour(marking: str) -> str:
        """Method to take an X or O and then select the relevant colour"""
        if marking == "X":
            return Colour.occupied_cell_x.value
        else:
            return Colour.occupied_cell_o.value

    def _switch_highlighted_confirmation_button(self):
        """Method to flick between who's cell is highlighted depending on who's go it is"""
        self.widget_manager.player_x_confirmation_button.configure(
            background=self._get_player_confirmation_button_colour(player=self.player_x),
            relief=self._get_player_confirmation_button_relief(player=self.player_x))
        self.widget_manager.player_o_confirmation_button.configure(
            background=self._get_player_confirmation_button_colour(player=self.player_o),
            relief=self._get_player_confirmation_button_relief(player=self.player_o))

    # Lowest level methods used in _switch_highlighted_confirmation_button
    def _get_player_confirmation_button_colour(self, player: Player) -> str:
        """Highlights the player's label if it's their go, otherwise their label is not highlighted."""
        if self.get_player_turn() == player.marking.value:
            return Colour.unconfirmed_cell.value
        else:
            return self._get_occupied_cell_colour(marking=BoardMarking(player.marking).name)

    def _get_player_confirmation_button_relief(self, player: Player):
        """Raises the player's label if it's there go, otherwise their label is sunken."""
        if self.get_player_turn() == player.marking.value:
            return Relief.active_player_confirmation_button.value
        else:
            return Relief.inactive_player_confirmation_button.value
