from game.constants.game_constants import BoardMarking, StartingPlayer
from tkinter_gui.app.game_setup_window.game_setup_widget_manager import GameSetupWidgets
from tkinter_gui.constants.style_and_colours import Colour, Font, Relief
from tkinter_gui.constants.dimensions import SetupWindowDimensions
from tkinter_gui.constants.game_parameter_constraints import PlayerNameConstraint
import tkinter as tk
from math import floor


class PlayerInfoFrame:
    """Class for the frame that allows users to enter their names and say who should go first."""

    def __init__(self,
                 widget_manager: GameSetupWidgets,
                 player_x_entry: tk.StringVar = None,
                 player_o_entry: tk.StringVar = None,
                 starting_player_value: tk.IntVar = None):
        self.widget_manager = widget_manager
        self.player_x_entry = player_x_entry
        self.player_o_entry = player_o_entry
        self.starting_player_value = starting_player_value

    def populate_player_info_frame(self):
        """Method to add all components of the player info frame to the grid"""
        self._create_and_format_player_info_frame()
        self._upload_active_player_widgets_to_widget_manager()
        self._upload_radio_buttons_to_widget_manager()

        # Player naming - static widgets so not in the widget manager
        player_x_label = self._get_player_label(player_x=True)
        player_o_label = self._get_player_label(player_x=False)
        player_x_label.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        player_o_label.grid(row=0, column=2, columnspan=2, sticky="nsew", padx=5, pady=5)

        # Player naming - dynamic name entry widgets in the widget manager
        self.widget_manager.player_x_entry.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
        self.widget_manager.player_o_entry.grid(row=1, column=2, columnspan=2, sticky="nsew", padx=5, pady=5)

        # Selection as to whether player is played by computer
        # TODO

        # Selection of who goes first - static widget (label)
        starting_player_label = self._get_starting_player_label()
        starting_player_label.grid(row=2, column=1, columnspan=2, sticky="nsew", padx=5, pady=1)

        # Selection of who goes first - dynamic widgets (radio buttons)
        self.widget_manager.random_player_starts_radio.grid(row=3, column=1, columnspan=2, sticky="ew", padx=5, pady=1)
        self.widget_manager.player_x_starts_radio.grid(row=4, column=1, columnspan=2, sticky="ew", padx=5, pady=1)
        self.widget_manager.player_o_starts_radio.grid(row=5, column=1, columnspan=2, sticky="ew", padx=5, pady=1)

    def _create_and_format_player_info_frame(self):
        self.widget_manager.player_info_frame = tk.Frame(
            master=self.widget_manager.setup_window,
            background=Colour.player_info_frame_background.value,
            borderwidth=3, relief=Relief.player_info_frame.value,
        )
        self.widget_manager.player_info_frame.rowconfigure(
            index=[0, 1], minsize=floor(SetupWindowDimensions.player_info_frame.height / 5), weight=1)
        self.widget_manager.player_info_frame.columnconfigure(
            index=[0, 1, 2, 3], minsize=floor(SetupWindowDimensions.player_info_frame.width / 4), weight=1)

    def _upload_active_player_widgets_to_widget_manager(self):
        """
        Method that adds all 'active' widgets in the player info frame to the widget manager
        'active' here means that they contain information that must be extracted somewhere else in the window.
        """
        self.widget_manager.player_x_entry = self._get_player_entry_field(player_x=True)
        self.widget_manager.player_o_entry = self._get_player_entry_field(player_x=False)
        self.widget_manager.player_x_computer_checkbtn = self._get_player_computer_checkbutton()
        self.widget_manager.player_o_computer_checkbtn = self._get_player_computer_checkbutton()

    ##########
    # Player labels, entry and computer check buttons
    ##########
    def _get_player_label(self, player_x: bool) -> tk.Label:
        """
        Method returning the label showing player one / player two.
        Note these are just static labels so don't need to go in the widget manager
        """
        if player_x:
            marking = BoardMarking(1).name
        else:
            marking = BoardMarking(-1).name
        player_label = tk.Label(
            master=self.widget_manager.player_info_frame,
            text="Player: " + f"{marking}",
            background=Colour.player_info_labels.value,
            relief=Relief.player_info_labels.value,
            font=(Font.default_font.value, floor(SetupWindowDimensions.player_info_frame.height / 12)),
            justify=tk.CENTER
        )
        return player_label

    def _get_player_entry_field(self, player_x: bool) -> tk.Entry:
        """Method returning an entry field where players can write their names."""
        if player_x:
            self.player_x_entry = tk.StringVar()
            entry_text = self.player_x_entry
            self.player_x_entry.trace_add(mode="write", callback=self._character_limit)
            self.player_x_entry.trace_add(mode="read", callback=self._min_characters)
        else:
            self.player_o_entry = tk.StringVar()
            entry_text = self.player_o_entry
            self.player_o_entry.trace_add(mode="write", callback=self._character_limit)
            self.player_o_entry.trace_add(mode="read", callback=self._min_characters)
        player_name_entry = tk.Entry(
            master=self.widget_manager.player_info_frame,
            textvariable=entry_text,
            background=Colour.player_name_entry.value,
            relief=Relief.player_name_entry.value,
            font=(Font.default_font.value, floor(SetupWindowDimensions.player_info_frame.height / 12)),
            justify=tk.CENTER
        )
        return player_name_entry

    def _get_player_computer_checkbutton(self) -> tk.Checkbutton:
        """
        Returns: a checkbutton that the user can select in order to indicate that the relevant player should be
        automated by the computer. Both players are given a check-button, which are identical.
        """
        computer_checkbutton = tk.Checkbutton(
            master=self.widget_manager.player_info_frame,
            text="Played by computer",
            offvalue=False, onvalue=True
        )
        #  TODO next. Could even make a command to set the player name to be computer "X"
        return computer_checkbutton

    def _character_limit(self, var, index, mode) -> None:
        """
        Trace callback that gets added to the entry fields' variables, so that players cannot enter a name with length
        greater than the max player length.
        Parameters:
        var - name of the tkinter variable the trace will be added to
        index - index of the tkinter variable in case it's an array
        mode - mode to trace the variable in i.e. read, write, etc.
        These are really just placeholders for the automatic positional args that get added by trace_add - could just
        use an *args but this makes it clearer what is going on.
        """
        if len(self.player_x_entry.get()) > PlayerNameConstraint.max_name_length.value:
            self.player_x_entry.set(self.player_x_entry.get()[:PlayerNameConstraint.max_name_length.value])
        if len(self.player_o_entry.get()) > PlayerNameConstraint.max_name_length.value:
            self.player_o_entry.set(self.player_o_entry.get()[:PlayerNameConstraint.max_name_length.value])

    def _min_characters(self, var, index, mode) -> None:
        """
        Trace callback that gets added to the entry fields' variables, to disable the confirmation button
        until they enter a name of sufficient end.

        Parameters:
        var - name of the tkinter variable the trace will be added to
        index - index of the tkinter variable in case it's an array
        mode - mode to trace the variable in i.e. read, write, etc.
        These are really just placeholders for the automatic positional args that get added by trace_add - could just
        use an *args but this makes it clearer what is going on.
        """
        if self.widget_manager.confirmation_button is not None:
            if (len(self.player_x_entry.get()) < PlayerNameConstraint.min_name_length.value) or \
                    (len(self.player_o_entry.get()) < PlayerNameConstraint.min_name_length.value):
                self.widget_manager.confirmation_button["state"] = tk.DISABLED
            if (len(self.player_x_entry.get()) >= PlayerNameConstraint.min_name_length.value) and \
                    (len(self.player_o_entry.get()) >= PlayerNameConstraint.min_name_length.value):
                self.widget_manager.confirmation_button["state"] = tk.NORMAL

    ##########
    # Starting player radio buttons
    ##########
    def _get_starting_player_label(self) -> tk.Label:
        """Method that returns the label saying "choose starting player" above the radio buttons"""
        starting_player_label = tk.Label(
            master=self.widget_manager.player_info_frame,
            text="Choose who goes first",
            background=Colour.starting_player_label.value,
            relief=Relief.starting_player_label.value,
            font=(Font.default_font.value, floor(SetupWindowDimensions.player_info_frame.height / 20)))
        return starting_player_label

    def _upload_radio_buttons_to_widget_manager(self) -> None:
        self.starting_player_value = tk.IntVar(value=StartingPlayer.RANDOM.value)
        player_x_starts = tk.Radiobutton(
            master=self.widget_manager.player_info_frame,
            text="Player X", variable=self.starting_player_value,
            value=StartingPlayer.PLAYER_X.value,
            background=Colour.starting_player_radio.value,
            relief=Relief.starting_player_radio.value,
            font=(Font.default_font.value, floor(SetupWindowDimensions.player_info_frame.height / 20)))
        self.widget_manager.player_x_starts_radio = player_x_starts
        player_o_starts = tk.Radiobutton(
            master=self.widget_manager.player_info_frame,
            text="Player O", variable=self.starting_player_value,
            value=StartingPlayer.PLAYER_O.value,
            background=Colour.starting_player_radio.value,
            relief=Relief.starting_player_radio.value,
            font=(Font.default_font.value, floor(SetupWindowDimensions.player_info_frame.height / 20)))
        self.widget_manager.player_o_starts_radio = player_o_starts
        random_player_starts = tk.Radiobutton(
            master=self.widget_manager.player_info_frame,
            text="Random", variable=self.starting_player_value,
            value=StartingPlayer.RANDOM.value,
            background=Colour.starting_player_radio.value,
            relief=Relief.starting_player_radio.value,
            font=(Font.default_font.value, floor(SetupWindowDimensions.player_info_frame.height / 20)))
        self.widget_manager.random_player_starts_radio = random_player_starts
