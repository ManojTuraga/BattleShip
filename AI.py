import random
from interfaces import interface_headers as IH

class AI:
    def __init__(self, difficulty: str):
        """
        Initialize the AI with the specified difficulty level.
        """
        self.difficulty = difficulty
        self.board = [[0 for _ in range(IH.NUMBER_OF_COLS)] for _ in range(IH.NUMBER_OF_ROWS)]
        self.opponent_board = [[0 for _ in range(IH.NUMBER_OF_COLS)] for _ in range(IH.NUMBER_OF_ROWS)]
        self.last_hit = None
        self.possible_targets = []

    def place_ships(self):
        """
        Place ships randomly on the board.
        """
        # Implement ship placement logic here
        pass

    def make_attack(self):
        """
        Make an attack based on the difficulty level.
        """
        if self.difficulty == "Easy":
            return self._easy_attack()
        elif self.difficulty == "Medium":
            return self._medium_attack()
        elif self.difficulty == "Hard":
            return self._hard_attack()

    def _easy_attack(self):
        """
        Easy difficulty: Fire randomly every turn.
        """
        while True:
            row = random.randint(0, IH.NUMBER_OF_ROWS - 1)
            col = random.randint(0, IH.NUMBER_OF_COLUMNS - 1)
            if self.opponent_board[row][col] == 0:
                return (row, col)

    def _medium_attack(self):
        """
        Medium difficulty: Fire randomly until it hits a ship, then fire in orthogonally adjacent spaces.
        """
        if self.last_hit:
            # Implement logic to fire in adjacent spaces
            pass
        else:
            return self._easy_attack()

    def _hard_attack(self):
        """
        Hard difficulty: Knows where all ships are and lands a hit every turn.
        """
        for row in range(IH.NUMBER_OF_ROWS):
            for col in range(IH.NUMBER_OF_COLUMNS):
                if self.opponent_board[row][col] == 0:
                    return (row, col)

    def update_opponent_board(self, coord, result):
        """
        Update the opponent's board with the result of the attack.
        """
        row, col = coord
        self.opponent_board[row][col] = result
        if result == IH.CoordStateType.COORD_STATE_HIT:
            self.last_hit = coord
            self.possible_targets.extend(self._get_adjacent_coords(coord))

    def _get_adjacent_coords(self, coord):
        """
        Get orthogonally adjacent coordinates.
        """
        row, col = coord
        adjacent_coords = []
        if row > 0:
            adjacent_coords.append((row - 1, col))
        if row < IH.NUMBER_OF_ROWS - 1:
            adjacent_coords.append((row + 1, col))
        if col > 0:
            adjacent_coords.append((row, col - 1))
        if col < IH.NUMBER_OF_COLUMNS - 1:
            adjacent_coords.append((row, col + 1))
        return adjacent_coords