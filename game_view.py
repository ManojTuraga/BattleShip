'''
Module: game_view.py
Date Created: September 10, 2024
Author: Clare Channel
Contributer(s): Clare Channel, Henry Marshall, Manoj Turaga

Inputs: Data provided by Executive Process
Outputs: Outputs Game State to standard output

Description: This module is an implemtation of the game view interface. This
             module will output the state of the game to the console and
             give any interactions back to the executive process

Sources: GeeksforGeeks
'''

import curses
import pandas

################################################################################
# Imports
################################################################################

# Import the general headers and the interface for
# the game view. The view should operate independent
# of the medium used, so as long as the view is
# constrained to the interface, everythign will work
from interfaces import interface_headers as IH
from interfaces import interface_game_view as IGV

# Import system and name from the OS module. We will
# need to be able to clear the screen when executing
# a new command, and this will allow us to start with
# a clean screen
#
# Source: https://www.geeksforgeeks.org/clear-screen-python/

from pprint import pprint

################################################################################
# Global Variables and Constants
################################################################################
TITLE_COLOR_PAIR = 1
SELECTED_COLOR_PAIR = 2
NON_SELECTED_COLOR_PAIR = 3
ERROR_COLOR_PAIR = 4

################################################################################
# Types
################################################################################

# Declare an implementation of the View Interface specified
# in the interfaces directory. As long as all the functions
# specified there are implemented, this will be a valid model
# that we can use
class GameView( IGV.GameViewInterface ):
    def __init__( self ):
        """
        Function: Initialization

        Inputs: None
        Outputs: None

        Description: This is the initialization function for this implentation
                     of the view. This view will utilize standard output, so
                     there will be no special things that need to happen. If
                     an implemenation chooses to do something, this function
                     will have a larger purpose 
        """
        self._screen = curses.initscr()
        self._screen.keypad(True)
        curses.curs_set(False)
        curses.noecho()
        curses.cbreak()
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair( TITLE_COLOR_PAIR, curses.COLOR_BLUE, -1 )
        curses.init_pair( SELECTED_COLOR_PAIR, curses.COLOR_RED, -1 )
        curses.init_pair( NON_SELECTED_COLOR_PAIR, curses.COLOR_WHITE, -1 )
        curses.init_pair( ERROR_COLOR_PAIR, curses.COLOR_RED, -1 )
    
    def get_centered_position( self, size : tuple[int, int] ) -> tuple[int, int]:
        """
        Function: Get Centered Position

        Inputs: The size of the object you are displaying on the screen
        Outputs: The position of the centered object

        Description: Calculates the position required to center an object on the terminal
        """

        window_size = self._screen.getmaxyx()
        return [int(window_size[0]/2 - size[0]/2), int(window_size[1]/2 - size[1]/2)]
    
    def draw_start_page( self, params : dict ) -> dict:
        """
        Function: Draw Start Page

        Inputs: User Input for configuration related stuff 
        Outputs: Dictionary with configuration state

        Description: This page will display the page for getting required
                     information from the user. This includes whether they
                     are hosting or joining a game, the number of ships
                     that they want, and where they want to place the ships
                     ont the board
        """
        # Declare and Initialize Local Variables
        config_dict : dict = dict()
        player_type = IH.PlayerTypeEnum.PLAYER_TYPE_HOST

        player_type = 0

        # Obtain the type of player is running the game.
        # The types of players that are supported are
        # defined in the in the interface headers, so
        # ensure that the input is is a valid input.
        # Putting it in while loop until the input is
        # valid
        while True:
            self.clear_screen()
            # Print the welcome dialog
            welcome_message = "Welcome to Battleship!"
            # Show the welcome message in the middle of the screen
            self._screen.addstr( 1, self.get_centered_position([len(welcome_message), 1])[0], welcome_message, curses.color_pair(TITLE_COLOR_PAIR) )
            question = "Are you hosting or joining a game?"
            self._screen.addstr( 3, self.get_centered_position([len(question), 1])[0], question )
            selections = ["Host", "Join"]
            for [index, selection] in enumerate(selections):
                message = f'{index}) {selection}'
                color = SELECTED_COLOR_PAIR if player_type == index else NON_SELECTED_COLOR_PAIR
                self._screen.addstr( 4 + index, self.get_centered_position([len(message), 1])[0], message, curses.color_pair(color) )

            self._screen.refresh()

            key = self._screen.getch()
            if key == curses.KEY_UP:
                player_type = (player_type - 1) % 2
            elif key == curses.KEY_DOWN:
                player_type = (player_type + 1) % 2
            elif key == curses.KEY_ENTER or key == 10:
                config_dict[ IH.VIEW_PARAM_PLAYER_TYPE ] = IH.PlayerTypeEnum( int( player_type ) )
                break

        ship_index = 0

        # Obtain the number of ships that the player will be facing
        while True:
            self.clear_screen()
            # Print the welcome dialog
            number_of_ships_message = "How many ships will you be playing with?"
            # Show the welcome message in the middle of the screen
            self._screen.addstr( 1, self.get_centered_position([len(number_of_ships_message), 1])[0], number_of_ships_message, curses.color_pair(TITLE_COLOR_PAIR) )
            ship_choices = 5
            centered_pos = self.get_centered_position([ship_choices*2, 1])
            for ship in range(5):
                message = f'{ship+1}'
                color = SELECTED_COLOR_PAIR if ship_index == ship else NON_SELECTED_COLOR_PAIR
                self._screen.addstr( 3, centered_pos[0] + ship*2, message, curses.color_pair(color) )

            self._screen.refresh()

            key = self._screen.getch()
            if key == curses.KEY_LEFT:
                ship_index = (ship_index - 1) % ship_choices
            elif key == curses.KEY_RIGHT:
                ship_index = (ship_index + 1) % ship_choices
            elif key == curses.KEY_ENTER or key == 10:
                config_dict[ IH.VIEW_PARAM_NUM_OF_SHIPS ] = int( ship_index + 1 )
                break
            else:
                try:
                    ship_index = int(curses.keyname(key)) - 1
                except:
                    pass
        
        # Return the configurations once all the required
        # configurations have been generated
        return config_dict

    def clear_screen( self ):
        """
        Function: Clear Screen

        Inputs: None
        Outputs: Removes characters in standard output window

        Description: This is a helper function that will clear the screen
                     when called.
        """
        self._screen.clear()

    def prompt_ship_init( self, params: dict ) -> dict:
        """
        Function: Prompt Ship Initialization

        Inputs: Configuration Inputs
        Outputs: Configuration Outputs

        Description: This page will display the section that allows
                     the user to select the inital placements of a ship
                     with size n
        """
        # Declare and initalize return dictionary
        return_dict = dict()

        # Obtain the required input parameters
        size = params[ IH.VIEW_PARAM_SIZE ]
        is_error_state = params[ IH.VIEW_PARAM_IS_ERROR_STATE ]
        direction = params[ IH.VIEW_PARAM_DIRECTION ]
        row = params[ IH.VIEW_PARAM_ROW ]
        col = params[ IH.VIEW_PARAM_COL ]

        # Get the row and column index from the row and column names
        col_index = IH.PLACEMENT_COL_TO_SYS_COL[col]
        row_index = IH.PLACEMENT_ROW_TO_SYS_ROW[row]

        # Clear the screen of any existing characters
        self.clear_screen()

        # Print the title of this page and the
        # current state of the grids
        place_pieces = "Place pieces"
        self._screen.addstr( 1, self.get_centered_position([len(place_pieces), 1])[0], place_pieces, curses.color_pair(TITLE_COLOR_PAIR) )

        # Draw the grid
        self.draw_grid( params )

        # Draw the new piece on top of the board
        color = ERROR_COLOR_PAIR if is_error_state else TITLE_COLOR_PAIR
        if direction == "H":
            for col_offset in range(size):
                piece_position = self.get_your_board_tile_position(row_index, col_index - col_offset)
                self._screen.addstr( piece_position[0], piece_position[1], "X", curses.color_pair(color) | curses.A_ITALIC )
        else:
            for row_offset in range(size):
                piece_position = self.get_your_board_tile_position(row_index - row_offset, col_index)
                self._screen.addstr( piece_position[0], piece_position[1], "X", curses.color_pair(color) | curses.A_ITALIC )

        self._screen.refresh()

        # Update the position of the new piece based on keyboard events
        key = self._screen.getch()
        if key == curses.KEY_LEFT:
            col_index -= 1
        elif key == curses.KEY_RIGHT:
            col_index += 1
        elif key == curses.KEY_UP:
            row_index -= 1
        elif key == curses.KEY_DOWN:
            row_index += 1
        elif curses.keyname(key) == b'r':
            if direction == "H":
                direction = "V"
            elif direction == "V":
                direction = "H"
        
        # Wrap the row or column around the board to make sure all parts of the piece are in bounds
        if direction == "H":
            col_index = ((col_index + 1 - size) % (IH.NUMBER_OF_COLS + 1 - size)) - 1 + size
        else:
            row_index = ((row_index + 1 - size) % (IH.NUMBER_OF_ROWS + 1 - size)) - 1 + size
        # Wrap around the board and make sure the index is positive
        col_index = (col_index + IH.NUMBER_OF_COLS) % IH.NUMBER_OF_COLS
        row_index = (row_index + IH.NUMBER_OF_ROWS) % IH.NUMBER_OF_ROWS

        return_dict[ IH.VIEW_PARAM_PLACE_SHIP ] = key == curses.KEY_ENTER or key == 10
        return_dict[ IH.VIEW_PARAM_DIRECTION ] = direction
        return_dict[ IH.VIEW_PARAM_ROW ] = IH.SYS_ROW_TO_PLACMENT_ROW[ row_index ]
        return_dict[ IH.VIEW_PARAM_COL ] = IH.SYS_COL_TO_PLACMENT_COL[ col_index ]

        # Return the configuration back to the calling function
        return return_dict

    def prompt_user_attack( self, params : dict ) -> dict:
        """
        Function: Prompt User Attack

        Inputs: Configuration Inputs
        Outputs: Configuration Outputs

        Description: This page will allow the user to select
                     the attack that they want to make on the opponent
        """
        # Declare and Initialize Return Dictionary
        return_dict = dict()

        # Obtained the required parameters from the configuration
        # dictionary
        is_error_state = params[ IH.VIEW_PARAM_IS_ERROR_STATE ]
        state_message = params[ IH.VIEW_PARAM_STATE_MESSAGE ]
        row = params[ IH.VIEW_PARAM_ROW ]
        col = params[ IH.VIEW_PARAM_COL ]

        # Get the row and column index from the row and column names
        col_index = IH.PLACEMENT_COL_TO_SYS_COL[col]
        row_index = IH.PLACEMENT_ROW_TO_SYS_ROW[row]
        
        # Clear the screen of any existing characters
        self.clear_screen()

        # Print the title of this page and the
        # current state of the grids
        place_pieces = "Attack Plan"
        self._screen.addstr( 1, self.get_centered_position([len(place_pieces), 1])[0], place_pieces, curses.color_pair(TITLE_COLOR_PAIR) )

        # Draw the grid
        self.draw_grid( params )

        # If the system is in an Error state, print the only
        # possible error message to the console
        if is_error_state:
            message = "Error! Already Attacked this Coordinate"
            self._screen.addstr( 2, self.get_centered_position([len(message), 1])[0], message, curses.color_pair(ERROR_COLOR_PAIR) )

        # If there is a state message, print it to the
        # console
        if state_message is not None:
            self._screen.addstr( 2, self.get_centered_position([len(state_message), 1])[0], state_message, curses.color_pair(ERROR_COLOR_PAIR) )

        # Draw the new piece on top of the board
        attack_position = self.get_opponent_board_tile_position(row_index, col_index)
        color = ERROR_COLOR_PAIR if is_error_state else TITLE_COLOR_PAIR
        self._screen.addstr( attack_position[0], attack_position[1], "X", curses.color_pair(color) | curses.A_ITALIC )

        self._screen.refresh()

        # Update the position of the new piece based on keyboard events
        key = self._screen.getch()
        if key == curses.KEY_LEFT:
            col_index -= 1
        elif key == curses.KEY_RIGHT:
            col_index += 1
        elif key == curses.KEY_UP:
            row_index -= 1
        elif key == curses.KEY_DOWN:
            row_index += 1

        # Wrap around the board and make sure the index is positive
        col_index = (col_index + IH.NUMBER_OF_COLS) % IH.NUMBER_OF_COLS
        row_index = (row_index + IH.NUMBER_OF_ROWS) % IH.NUMBER_OF_ROWS

        return_dict[ IH.VIEW_PARAM_PLACE_SHIP ] = key == curses.KEY_ENTER or key == 10
        return_dict[ IH.VIEW_PARAM_ROW ] = IH.SYS_ROW_TO_PLACMENT_ROW[ row_index ]
        return_dict[ IH.VIEW_PARAM_COL ] = IH.SYS_COL_TO_PLACMENT_COL[ col_index ]
        
        # Return the dictionary back to the calling function
        return return_dict

    def prompt_wait_page( self, params : dict ) -> dict:
        """
        Function: Prompt Wait Page

        Inputs: Configuration Inputs
        Outputs: Configuration Outputs

        Description: This page will be displayed when the current
                     player needs to wait for something to happen
        """
        # Declare and initialize the return dictionary
        return_dict = dict()

        # Get the state message from the configuration
        state_message = params[ IH.VIEW_PARAM_STATE_MESSAGE ]

        # Clear the screen of any existing characters
        self.clear_screen()

        # Print the title of this page and the
        # current state of the grids
        title = "Standby"
        self._screen.addstr( 1, self.get_centered_position([len(title), 1])[0], title, curses.color_pair(TITLE_COLOR_PAIR) )

        # Draw the grid
        self.draw_grid( params )

        # If there is a state message, print it to the
        # console otherwise set it to the default
        if state_message is None:
            state_message = "Waiting for opponent"
        self._screen.addstr( 2, self.get_centered_position([len(state_message), 1])[0], state_message, curses.color_pair(ERROR_COLOR_PAIR) )

        self._screen.refresh()

        # Return necessary even though nothing is being returned
        return return_dict
    
    def draw_game_over_page( self, params : dict ) -> dict:
        """
        Function: Draw Game Over Page

        Inputs: Configuration Inputs
        Outputs: Configuration Outputs

        Description: This is the page that will be displayed when the game
                     is complete
        """
        # Initialize Return dictionary and win state from the required
        # configration parameters
        return_dict = dict()
        win = params[ IH.VIEW_PARAM_WIN ]

        # Clear the screen of any existing characters
        self.clear_screen()

        # Print the title of this page and the
        # current state of the grids
        title = "Game Over"
        self._screen.addstr( 1, self.get_centered_position([len(title), 1])[0], title, curses.color_pair(TITLE_COLOR_PAIR) )

        # Draw the grid
        self.draw_grid( params )

        # Print the Win/Loss message and return dictionary back
        # to the calling function
        if win:
            message = "You Won!"
            self._screen.addstr( 2, self.get_centered_position([len(message), 1])[0], message, curses.COLOR_GREEN )
        else:
            message = "You Lost!"
            self._screen.addstr( 2, self.get_centered_position([len(message), 1])[0], message, curses.COLOR_RED )

        self._screen.refresh()

        return return_dict

    def draw_grid( self, params : dict ) -> dict:
        """
        Function: Draw Grid

        Inputs: Configuration Inputs
        Outputs: Configuration Outputs

        Description: This function will draw the player board and the opponent
                     board to the console
        """
        # Fetch the player and opponent board from the configuration
        # parameters
        board = params[ IH.VIEW_PARAM_BOARD ]
        opponent_board = params[ IH.VIEW_PARAM_OPPONENT_BOARD ]

        # Print the boards to the console
        opponents_board = "Opponent's Board"
        self._screen.addstr( 3, self.get_centered_position([len(opponents_board), 1])[0], opponents_board, curses.color_pair(TITLE_COLOR_PAIR) )

        self.print_board(opponent_board, self.opponent_board_position())

        your_board = "Your Board"
        self._screen.addstr( 8*2+1, self.get_centered_position([len(your_board), 1])[0], your_board, curses.color_pair(TITLE_COLOR_PAIR) )
        self.print_board(board, self.your_board_position())
    
    def your_board_position( self ) -> tuple[int, int]:
        """
        Function: Your Board Position

        Inputs: Board
        Outputs: Position of the current player's board
        """
        return [10*2, self.get_centered_position([10*2+3, 1])[0]]
    
    def get_your_board_tile_position( self, row_index: int, col_index: int ) -> tuple[int, int]:
        """
        Function: Get Your Board Tile Position

        Inputs: Board, row index, column index
        Outputs: The character position of the tile at that position in your board
        """
        board_position = self.your_board_position()
        return [row_index + board_position[0] + 1, col_index * 2 + board_position[1] + 3]
    
    def opponent_board_position( self ) -> tuple[int, int]:
        """
        Function: Your Opponent Board Position

        Inputs: Board
        Outputs: Position of the opponent's board
        """
        return [5, self.get_centered_position([10*2+3, 1])[0]]
    
    def get_opponent_board_tile_position( self, row_index: int, col_index: int ) -> tuple[int, int]:
        """
        Function: Get Your Opponent Board Tile Position

        Inputs: Board, row index, column index
        Outputs: The character position of the tile at that position in your opponent's board
        """
        board_position = self.opponent_board_position()
        return [row_index + board_position[0] + 1, col_index * 2 + board_position[1] + 3]

    def print_board( self, board: list[list], position: tuple[int, int] ):
        # Print the columns
        for [x, col] in enumerate(IH.PLACEMENT_COL_TO_SYS_COL.keys()):
            self._screen.addstr(position[0], position[1] + 3 + x*2, f"{col}")
        # Print the rows
        for [y, row] in enumerate(IH.PLACEMENT_ROW_TO_SYS_ROW.keys()):
            self._screen.addstr(position[0] + 1 + y, position[1], f"{row}")
        # Print the body of the grid
        for y in range(len(board)):
            for x in range(len(board[y])):
                pos = [position[0] + 1 + y, position[1] + 3 + x * 2]
                if board[ y ][ x ] > IH.BASE_CELL:
                    self._screen.addstr(pos[0], pos[1], 'S')

                elif board[ y ][ x ] == IH.BASE_CELL:
                    self._screen.addstr(pos[0], pos[1], '~')

                elif board[ y ][ x ] == IH.HIT_CELL:
                    self._screen.addstr(pos[0], pos[1], 'X')

                elif board[ y ][ x ] == IH.MISSED_CELL:
                    self._screen.addstr(pos[0], pos[1], 'O')
