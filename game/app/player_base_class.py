from game.constants.game_constants import BoardMarking


class Player:
    """
    Class for the players of the noughts and crosses game.

    Parameters:
    Name - evidently the player's name
    Mark_value - whether they are carrying 1 or -1 as their playing_grid marking
    Active_game_win_count - accumulates the player's wins in an active game.
    """

    def __init__(self,
                 name: str,
                 marking: BoardMarking,
                 active_game_win_count: int = 0):
        self.name = name
        self.marking = marking
        self.active_game_win_count = active_game_win_count

    def award_point(self):
        """Method to award the player array point."""
        self.active_game_win_count += 1

    def __eq__(self, other) -> bool:
        """Method to check the equivalence of two players (by marking)"""
        if isinstance(other, Player):  # Note the nested if as otherwise an error trying other.marking
            if (other.marking == self.marking) and (other.name == self.name):
                return True
        else:
            return False

    def get_win_count_label_text(self):
        """Method giving the winner for the player's win count label"""
        text = f"{self.name}:\n{self.active_game_win_count}"
        return text
