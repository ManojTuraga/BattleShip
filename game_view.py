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
from os import system, name

from pprint import pprint

import pandas

################################################################################
# Global Variables and Constants
################################################################################
WINDOWS_OS_NAME : str = "nt"
WINDOWS_OS_CLEAR_SCREEN_COMMAND : str = "cls"

NON_WINDOWS_OS_CLEAR_SCREEN_COMMAND : str = "clear"

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
        pass
    
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
        number_of_ships = 0

        # Print the welcome dialog
        self.clear_screen()
        print( "Welcome to Battleship!" )

        # Obtain the type of player is running the game.
        # The types of players that are supported are
        # defined in the in the interface headers, so
        # ensure that the input is is a valid input.
        # Putting it in while loop until the input is
        # valid
        while True:
            print( "Are you hosting or joining a game?" )
            print( "\t0) Host" )
            print( "\t1) Join" )
            player_type = input( "Enter: " )

            if player_type.isnumeric() and int( player_type ) in [ IH.PlayerTypeEnum.PLAYER_TYPE_HOST.value, IH.PlayerTypeEnum.PLAYER_TYPE_JOIN.value ]:
                config_dict[ IH.VIEW_PARAM_PLAYER_TYPE ] = IH.PlayerTypeEnum( int( player_type ) )
                break
            else:
                print( "Error! Invalid Input" )
        
        # Obtain the number of ships that the player will be facing
        # Again ensure that the input is a valid input
        while True:
            number_of_ships = input( "How many ships will you be playing with? (1 - 5): " )

            if number_of_ships.isnumeric() and int( number_of_ships ) in range( IH.MIN_NUM_OF_SHIPS, IH.MAX_NUM_OF_SHIPS + 1 ):
                config_dict[ IH.VIEW_PARAM_NUM_OF_SHIPS ] = int( number_of_ships )
                break
            else:
                print( "Error! Invalid Input" )
        
        # Return the configurations once all the required
        # configurations have been generated
        return config_dict

    def clear_screen( self ):
        """
        Function: Clear Screen

        Inputs: None
        Outputs: Removes characters in standard output window

        Description: This is a helper function that will clear the screen
                     when called. Used to make clean output
        
        Sources: GeeksforGeeks
        """
        if name == WINDOWS_OS_NAME:
            # Execute the windows version of the clear screen command
            system( WINDOWS_OS_CLEAR_SCREEN_COMMAND )

        else:
            # Execute the non windows version of the clear screen command
            system( NON_WINDOWS_OS_CLEAR_SCREEN_COMMAND )

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
    
        # Clear the screen of any existing characters
        self.clear_screen()

        # Print the title of this page and the
        # current state of the grids
        print( "Initialization:\n" )
        self.draw_grid( params )

        # If we were in an error state, then place the
        # only possible error that could occur
        if is_error_state:
            print( f"Error! Invalid Ship Placement!" )

        # Print the size of the sship that we are placing
        print( f"Place ship of size { size }." )

        # This loop is responsible for getting the placement of the ships
        # column. It will continue running until a valid column is selected 
        while True:
            col = input( "Enter the column of the ship's bow (A - J): " ).upper()
            
            if col in IH.PLACEMENT_COL_TO_SYS_COL.keys():
                return_dict[ IH.VIEW_PARAM_COL ] = col
                break
            else:
                print( "Invalid input!" )

        # This loop is responsible for getting the placment of a ship's row.
        # It will contiue running until a valid row is slected
        while True:
            row = input( "Enter the row of the ship's bow (1 - 10): " )

            if row.isnumeric() and int( row ) in IH.PLACEMENT_ROW_TO_SYS_ROW.keys():
                return_dict[ IH.VIEW_PARAM_ROW ] = int( row )
                break
            else:
                print( "Invalid input!" )

        # This loop is responsible for getting the type of placement.
        # It will keep running until a valid placement is entered
        while True:
            direction = input( "Choose direction (H or V): ").upper()

            if direction in [ "H", "V" ]:
                return_dict[ IH.VIEW_PARAM_DIRECTION ] = direction
                break
            else:
                print( "Invalid input!" )

        # Return the configuration back to the calling function
        return return_dict
    
    def _convert_to_view_grid( self, grid : list[ list ] ) -> None:
        """
        Function: Convert to view grid

        Inputs: Grid
        Outputs: In place modification of grid

        Description: This page will take the grid given to it and
                     transform it into the grid that will be
                     displayed
        """
        # Iterate over every cell in the grid
        for i in range( len( grid ) ):
            for j in range( len( grid [ i ] ) ):
                # The following if blocks are responsible for
                # replacing the numeric value in the grid with
                # a corresponding string that represents the number
                # state
                if grid[ i ][ j ] > IH.BASE_CELL:
                    grid[ i ][ j ] = 'S'

                elif grid[ i ][ j ] == IH.BASE_CELL:
                    grid[ i ][ j ] = '~'

                elif grid[ i ][ j ] == IH.HIT_CELL:
                    grid[ i ][ j ] = 'X'

                elif grid[ i ][ j ] == IH.MISSED_CELL:
                    grid[ i ][ j ] = 'O'

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
        
        # Print the title of this page and draw the grids
        # of the player and the opponent on the screen
        self.clear_screen()
        print( "Attack Plan:\n" )
        self.draw_grid( params )

        # If the system is in an Error state, print the only
        # possible error message to the console
        if is_error_state:
            print( f"Error! Already Attacked this Coordinate" )

        # If there is a state message, print it to the
        # console
        if state_message is not None:
            print( state_message )

        print( f"Make an attack!" )

        # The following loop is responsible for getting the column
        # location for the attack, which will keep running until
        # valid column is passed in
        while True:
            col = input( "Enter the column of the attack (A - J): " ).upper()
            
            if col in IH.PLACEMENT_COL_TO_SYS_COL.keys():
                return_dict[ IH.VIEW_PARAM_COL ] = col
                break
            else:
                print( "Invalid input!" )

        # The following loop is responsible for getting the row
        # location for the attack, which will keep running until
        # valid column is passed in
        while True:
            row = input( "Enter the row of the attack (1 - 10): " )

            if row.isnumeric() and int( row ) in IH.PLACEMENT_ROW_TO_SYS_ROW.keys():
                return_dict[ IH.VIEW_PARAM_ROW ] = int( row )
                break
            else:
                print( "Invalid input!" )
        
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
        
        # Print the template of the page to the console
        self.clear_screen()
        print( "Standby:\n" )
        self.draw_grid( params )

        # If the there is a state message, print that state
        # message ot the console
        if state_message is not None:
            print( state_message )

        print( "Waiting for opponent" )

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
        state_message = params[ IH.VIEW_PARAM_STATE_MESSAGE ]
        
        # Print Page template to the console
        self.clear_screen()
        print( "Game Over:\n" )
        self.draw_grid( params )

        # Print the final state message
        print( state_message )

        # Print the Win/Loss message and return dictionary back
        # to the calling function
        if win:
            print( "You Won!" )
        else:
            print( "You Lost!" )

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

        # Convert the boards into something that the view
        # can use
        self._convert_to_view_grid( board )
        self._convert_to_view_grid( opponent_board )
        
        # Convert each of the boards into a pandas dataframe so that
        # printing looks clean
        df_player = pandas.DataFrame( board, list( IH.PLACEMENT_ROW_TO_SYS_ROW.keys() ), list( IH.PLACEMENT_COL_TO_SYS_COL.keys() ) )
        df_opponent = pandas.DataFrame( opponent_board, list( IH.PLACEMENT_ROW_TO_SYS_ROW.keys() ), list( IH.PLACEMENT_COL_TO_SYS_COL.keys() ) )
        
        # Print the boards to the console
        print( "Opponent's Board\n" )
        pprint( df_opponent )
        print( "\nYour Board:\n" )
        pprint( df_player )
        print()