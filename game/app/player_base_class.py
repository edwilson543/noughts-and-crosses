from game.constants.game_constants import GameValue

class Player:
    """Class for the players of the noughts and crosses game."""

    def __init__(self,
                 name: str,
                 active_symbol: GameValue,
                 active_game_win_count: int = 0):
        self.name = name
        self.active_symbol = active_symbol
        self.active_game_win_count = active_game_win_count

    def award_point(self):
        """Method to award the player a point."""
        self.active_game_win_count += 1

    def __eq__(self, other) -> bool:
        """Method to check the equivalence of two players (by active_symbol)"""
        if isinstance(other, Player):
            if other.active_symbol == self.active_symbol:
                return True
            else:
                return False
        else:
            raise TypeError(f"{other} is not of type Player but was compared with {self.name} for equality")