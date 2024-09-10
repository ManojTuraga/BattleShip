## View ##

## Visual Guide ##
# Board: 10x10 grid
# Boat space: ^ or <
# Empty space (water): ~
# Missed space: #
# Boat hit: X
# Boat sunk: *

## Variable Declaration
ship_length = [1,2,3,4,5]
player_1_board = [["~"] * 10 for i in range(10)]
player_2_board = [["~"] * 10 for i in range(10)]
player_1_move_board = [["~"] * 10 for i in range(10)]
player_2_move_board = [["~"] * 10 for i in range(10)]
letters_to_numbers = {"A":0, "B":1, "C":2, "D":3, "E":4, "F":5, "G":6, "H":7, "I":8, "J":9}

def print_grid(board):
    #print top of board
    print("   A B C D E F G H I J")
    print("  +-+-+-+-+-+-+-+-+-+-+")

    #print each row of board to make grid
    # print first 9 rows with a space before number so that it lines up with row 10 
    row_num = 1
    if row_num <10:
        for row in board:
            print("%2d|%s|" % (row_num, " ".join(row)))
            row_num += 1
    else:
        print("%d|%s|" % (row_num, " ".join(row)))

    print("  +-+-+-+-+-+-+-+-+-+-+")

#test
#print_grid(player_1_board)
#print_grid(player_2_board)

def place_ships(board):
    #go through each size of ship and place them
    #prompt user to choose between placing horizontally or vertically
    #then ask for starting position

    while True:
        #place_ships == True
        for length in ship_length:
        #loop until ship fits and doesn't overlap
            while True:
                place_ships = True
                print('Place the ship with a length of ' + str(length))
                row, column, placing = user_input(place_ships)
                if check_size_valid(length, row, column, placing):
                    #check if ship overlaps
                        if check_pos_overlap(board, row, column, placing, length) == False:
                            #place ship
                            if placing == "H":
                                for i in range(column, column + length):
                                    board[row][i] = "^"
                            else:
                                for i in range(row, row + length):
                                    board[i][column] = "<"
                            print_grid(player_1_board)
                            #break 


def check_size_valid(ship_length, row, column, placing):
    #if placing horizontal, if the boat does not fit in the spot, return false
    if placing == "H":
        if column + ship_length > 8:
            return False
        else:
            return True
    #if placing vertical , if the boat does not fit in the spot, return false
    else:
        if row + ship_length > 8:
            return False
        else:
            return True


def check_pos_overlap(board, row, column, placing, ship_length):
    #if placing horizontally
    #for the length of the boat in the column (for as many posistions as it will take in the column)
    #check that there are no other boats placed there
    #same goes for vertical check but it checks row instead of column duh
    if placing == "H":
        for i in range(column, column + ship_length):
            if board[row][i] == "<" or "^":
                return True
    else:
        for i in range(row, row + ship_length):
            if board[i][column] == "^" or "<":
                return True
    return False


def user_input(place_ships):
    #user input for placing their ships
    if place_ships == True:
        while True:
            try:
                placing = input("Enter direction to place ship (H or V): ").upper()
                if placing == "H" or placing == "V":
                    break
            except TypeError:
                print("Enter a proper placing, H (horizontal) or V (vertical)")
        while True:
            try:
                row = int(input("Enter the row (1-10) for your ship: "))
                if row <= 10:
                    row = int(row) - 1
                    break
            except ValueError:
                print("Enter a valid row between 1 and 10: ")
        while True:
            try:
                column = input("Enter the column (A-J) for your ship").upper()
                if column in "ABDCEFGHIJ":
                    column = letters_to_numbers[column]
                    break
            except KeyError:
                print("Enter a valid column from A to J: ")
        return row, column, placing
    
    #user input for guessing
    else:
        while True:
            try: 
                row = int(input("Enter the row (1-10) of the ship: "))
                if row <=10:
                    row = int(row) - 1
                    break
            except ValueError:
                print('Enter a valid row between 1 and 10: ')
        while True:
            try: 
                column = input("Enter the column (A-J) of the ship: ").upper()
                if column in 'ABCDEFGHIJ':
                    column = letters_to_numbers[column]
                    break
            except KeyError:
                print('Enter a valid column from A to J: ')
        return row, column 



def ships_hit():
    pass

def turn(board):
    pass
