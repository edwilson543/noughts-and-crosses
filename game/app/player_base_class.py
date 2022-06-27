"""Module to define the Player base class - there are two player objects active in any noughts and crosses game."""

# Local application imports
from game.constants.game_constants import BoardMarking


class Player:
    """
    Class for the players of the noughts and crosses game.

    Instance attributes:
    __________
    name - evidently the player's name, as a string
    mark_value - determines whether the player is carrying 1 or -1 (X or O) as their playing_grid marking
    active_game_win_count - accumulates the player's wins in a game session.
    """

    def __init__(self,
                 name: str,
                 marking: BoardMarking,
                 active_game_win_count: int = 0):
        self.name = name
        self.marking = marking
        self.active_game_win_count = active_game_win_count

    def award_point(self):
        """Method to award the player a point, by adding one to their win count."""
        self.active_game_win_count += 1

    def get_win_count_label_text(self):
        """Method giving the text and win count for the player's win count label"""
        text = f"{self.name}:\n{self.active_game_win_count}"
        return text
