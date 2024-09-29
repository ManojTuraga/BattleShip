import random
from interfaces import interface_headers as IH

class AI:
    def __init__(self,  difficulty: str, num_ships: int):
        """
        Initialize the AI with the specified difficulty level.
        """
        self.difficulty = difficulty
        self.num_ships = num_ships
        self.board = [[0 for _ in range(IH.NUMBER_OF_COLS)] for _ in range(IH.NUMBER_OF_ROWS)]
        self.opponent_board = [[0 for _ in range(IH.NUMBER_OF_COLS)] for _ in range(IH.NUMBER_OF_ROWS)]
        self.last_hit = None
        self.possible_targets = []


    def place_ships(self):
        ships_placed = 0

        for ship_length in range(1,self.num_ships+1):
            # Randomly determine ship length (you can modify this logic to have fixed-length ships)

            # Randomly choose direction: 0 for horizontal, 1 for vertical
            direction = random.choice([0, 1])

            if direction == 0:  # Horizontal placement
                row = random.randint(0, IH.NUMBER_OF_ROWS - 1)
                col = random.randint(0, IH.NUMBER_OF_COLS - ship_length)  # Ensure ship fits horizontally
            else:  # Vertical placement
                row = random.randint(0, IH.NUMBER_OF_ROWS - ship_length)
                col = random.randint(0, IH.NUMBER_OF_COLS - 1)  # Ensure ship fits vertically

            # Check if the space is free to place the ship
            can_place = True
            for i in range(ship_length):
                if direction == 0:  # Horizontal
                    if self.board[row][col + i] != 0:  # Check if space is occupied
                        can_place = False
                        break
                else:  # Vertical
                    if self.board[row + i][col] != 0:  # Check if space is occupied
                        can_place = False
                        break

            # Place the ship if it's a valid placement
            if can_place:
                for i in range(ship_length):
                    if direction == 0:  # Horizontal
                        self.board[row][col + i] = 1  # Mark ship's position
                    else:  # Vertical
                        self.board[row + i][col] = 1  # Mark ship's position
                ships_placed += 1
            # Implement ship placement logic here
        self.print_board()
    
    def print_board(self):
        """
        Print the current state of the board.
        """
        for row in self.board:
            print(' '.join(str(cell) for cell in row))
        print()  # Add an empty line for better readability

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