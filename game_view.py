## Battlehsip View Class ##
#Prints boards and ships, obtains user inputs
#takes in opponent data to be used in game

## Visual Guide ##
# Board: 10x10 grid
# Boat space: ^ (V) or < (V)
# Empty space (water): ~
# Missed space: #
# Boat hit: X


class BattleshipView:
    def __init__(self):
        self.board_size = 10
        self.columns = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        self.rows = list(range(1, 11))
        self.board = [['~' for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.opponent_board = [['~' for _ in range(self.board_size)] for _ in range(self.board_size)]
        self.ship_sizes = {
            1: 'Destroyer (1 cells)',
            2: 'Submarine (2 cells)',
            3: 'Cruiser (3 cells)',
            4: 'Battleship (4 cells)',
            5: 'Carrier (5 cells)'
        }

    def print_grids(self):
        # prints boards side by side
        print("Your Board" + " " * 22 + "Opponent's Board")
        print("   " + " ".join(self.columns) + " " * 9 + "   " + " ".join(self.columns))
        for i in range(self.board_size):
            player_row = f"{i + 1:2} " + " ".join(self.board[i])
            opponent_row = f"{i + 1:2} " + " ".join(self.opponent_board[i])
            print(f"{player_row}      {opponent_row}")

    def convert_to_index(self, coordinate):
        # converts coordinates into index for boards (ex. B7)
        column = self.columns.index(coordinate[0].upper())
        row = int(coordinate[1:]) - 1
        return row, column

    def place_ship(self, size):
        # promts player to place ship of desired size
        while True:
            self.print_grids()
            print(f"Place ship of size {size}.")
            coordinate = input("Enter the starting coordinate (e.g., A5): ")
            direction = input("Choose direction (H or V): ").upper()

            try:
                row, column = self.convert_to_index(coordinate)
            except (ValueError, IndexError):
                print("Invalid coordinate.Please try again.")
                continue

            # Place ship horizontally or vertically
            # goes through each "box" in the given direction until length is reached
            # checks to make sure each box is currently water (available)
            if direction == 'H':
                if column + size > self.board_size:
                    print("Invalid placement. Please try again.")
                    continue
                if any(self.board[row][column + i] != '~' for i in range(size)):
                    print("Invalid placement. Please try again.")
                    continue
                for i in range(size):
                    self.board[row][column + i] = '<'
            elif direction == 'V':
                if row + size > self.board_size:
                    print("Invalid placement. Please try again.")
                    continue
                if any(self.board[row + i][column] != '~' for i in range(size)):
                    print("Invalid placement. Please try again.")
                    continue
                for i in range(size):
                    self.board[row + i][column] = '^'
            else:
                print("Invalid direction. Please try again.")
                continue
            break

    def num_of_ships(self):
        # asks user how many ships they want to place
        while True:
            try:
                num_ships = int(input("How many ships would you like to place? (1-5): "))
                if num_ships < 1 or num_ships > 5:
                    print("Enter a number from 1 to 5.")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter a number from 1 to 5.")

        # calls place_ship so it can use data
        for i in range(1, num_ships + 1):
            print(f"Placing {self.ship_sizes[i]}")
            self.place_ship(i + 1)

    def turn(self, opponent_data):
        # players turn to fire a shot
        while True:
            self.print_grids()
            shot = input("Enter the coordinate to fire at (ex., B7): ")

            try:
                row, column = self.convert_to_index(shot)
            except (ValueError, IndexError):
                print("Invalid coordinate. Please try again.")
                continue

            if self.opponent_board[row][column] in ['X', '#']:
                print("Cannot fire at coordinate again. Please try again.")
            else:
                # Call the opponent data callback to determine hit or miss
                hit = opponent_data(row, column)
                if hit:
                    self.opponent_board[row][column] = 'X'  # Hit
                    print("Hit!")
                else:
                    self.opponent_board[row][column] = '#'  # Miss
                    print("Miss!")
                break

    def check_victory(self, board):
        # check if all ships on one side have been sunk
        for row in board:
            if '^' or '<' in row:
                return False  # there are still ships
        return True  # all ships are sunk       

    def connect(self):
        # placeholder for opponent connection
        input("Press Enter to connect to another player...")

    def start_game(self, opponent_data_callback):
        # starts game and runs loop
        print("Welcome to Battleship!")
        self.connect()
        self.place_ships()

        # main loop
        game_over = False
        while not game_over:
            # players turn
            print("\nYour turn to fire!")
            self.take_turn(opponent_data_callback) #uses opponent data for hit/miss

            # check for victory
            if self.check_victory(self.opponent_board):
                print("Congratulations, you've sunk all the opponent's ships! You win!")
                game_over = True
                break

            # if not victory then next person goes
            print("\nOpponent's turn to fire!")

            # opponent shot
            opponent_shot_result = self.receive_opponent_shot()

            if opponent_shot_result == 'hit':
                print("Opponent hit your ship!")
            elif opponent_shot_result == 'miss':
                print("Opponent missed!")
            else:
                print("Invalid shot. Opponent will go again.")

            # check opponent victory
            if self.check_victory(self.board):
                print("All your ships have been sunk. Opponent wins!")
                game_over = True
                break


# calling in opponents data
def opponent_data(row, col):
    # this is just tester data
    # this is where the opponent data will be called into the game
    opponent_ships = [
        (1, 2), (1, 3), (1, 4), (4, 5), (6, 7),  
    ]
    return (row, col) in opponent_ships


if __name__ == "__main__":
    game = BattleshipView()
    game.start_game(opponent_data)
