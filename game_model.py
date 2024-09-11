"""
Module: player_model.py
Creation Date: September 2nd, 2024
Author: Manoj Turaga
Contributors: Henry Wallace, Connor Forristal, Manoj Turaga
Sources:

Description:
    This model holds the state data for a particular game instance.
    Models that inherit from the model interface will store the state
    of a players board and the opponents board with functions to get/update
    coordinates

Inputs:
    Actions done to affect the player state
Outputs:
    Current state of the player
"""

################################################################################
# Imports
################################################################################
from interfaces import interface_headers as IH
from interfaces import interface_game_model as IGM

################################################################################
# Global Variables
################################################################################

################################################################################
# Types
################################################################################
class GameModel( IGM.GameModelInterface ):
    def __init__( self ):
        """
        Function: Initialization

        Inputs: None
        Outputs: None

        Description: This is the initialization function of the model. It will
                     create data members to store the state of both the current
                     player and the opponent

        Data members: Instance of a board for the current player and the opponent
        """
        # Initialize Data Members
        self._host_board : IH.GameBoardType = []
        self._join_board : IH.GameBoardType = []

        # Update the both the player and opponent boards.
        # The IDS are defined in the interface because the rest
        # of the program does not need to know about it.
        # We have to create the lists in this fashion to make sure
        # that python does not replicate the same instance of the cell
        for _ in range( 0, IH.NUMBER_OF_ROWS ):
            host_row : list[ IH.GameCoordType ] = []
            join_row : list[ IH.GameCoordType ] = []

            for __ in range( 0, IH.NUMBER_OF_COLS ):
                host_row.append( { IH.GAME_COORD_TYPE_ID_INDEX : IH.BASE_CELL, 
                                   IH.GAME_COORD_TYPE_STATE_INDEX : IH.CoordStateType.COORD_STATE_BASE } )
                join_row.append( { IH.GAME_COORD_TYPE_ID_INDEX : IH.BASE_CELL, 
                                   IH.GAME_COORD_TYPE_STATE_INDEX : IH.CoordStateType.COORD_STATE_BASE } )

            self._host_board.append( host_row )
            self._join_board.append( join_row )
        
    def get_coord( self, player_type : IH.PlayerTypeEnum, coord: IH.SystemCoordType, ) -> IH.GameCoordType:
        """
        Function: Get coordinate from board

        Inputs: The Player we want to get the data from, the location of the data
        Outputs: The data in the cell of the board

        Description: This function is the data getter of this interface. We standardize
                     The return by defining the return type in the interface headers.
                     For those looking to make their own model, make sure your functions
                     return the same types
        """
        # Extract the row and column from the coordinate 
        # passed in
        row = coord[ IH.ROW_INDEX ]
        col = coord[ IH.COLUMN_INDEX ]

        # Determine the board that we need to update based on the
        # player type that we pass in
        board_to_update = self._host_board if player_type == IH.PlayerTypeEnum.PLAYER_TYPE_HOST else self._join_board

        # Return a copy of the cell that is in the coordinate
        # of the board
        return IH.GameCoordType( board_to_update[ row ][ col ] )

    def update_coord( self, player_type : IH.PlayerTypeEnum, coord: IH.SystemCoordType, new_val: IH.GameCoordType ) -> None:
        """
        Function: Update cell in board

        Inputs: The Player we want to get the data from, the location of the data, the new data
        Outputs: None

        Description: This function is the data setter of the cell. We only
                     make it so that we update on a coordinate by coordinate
                     basis so that we don't expose everything to the application
                     that consumes this model
        """
        # Extract the row and column from the coordinate 
        # passed in
        row = coord[ IH.ROW_INDEX ]
        col = coord[ IH.COLUMN_INDEX ]

        # Determine the board that we need to update based on the
        # player type that we pass in
        board_to_update = self._host_board if player_type == IH.PlayerTypeEnum.PLAYER_TYPE_HOST else self._join_board

        # Set the coordinate in the board to have
        board_to_update[ row ][ col ] = new_val

    def is_valid_coord( self, player_type : IH.PlayerTypeEnum, coord: IH.SystemCoordType, event : IH.GameEventType ) -> bool:
        """
        Function: Can action be taken on coordinate

        Inputs: The player's' board, the coordinate to check, under what circumstances we are checking
        Outputs: Boolean value

        Description: This function defines the abstract method to make sure that an action can be taken
                     on a particular coordinate. Depending on the context provided by event,
                     this function can take different logic to know if a particular coordinate
                     is valid
        """
        # Extract the row and column from the coordinate 
        # passed in
        row = coord[ IH.ROW_INDEX ]
        col = coord[ IH.COLUMN_INDEX ]

        # Determine the board that we need to validate based on the
        # player type that we pass in
        board_to_validate = self._host_board if player_type == IH.PlayerTypeEnum.PLAYER_TYPE_HOST else self._join_board

        # Determine the particular cell information of the coordinate
        cell = board_to_validate[ row ][ col ]

        if event == IH.GameEventType.GAME_EVENT_PLACE_SHIPS:
            # If we are in the case of trying to validate that
            # we can place a ship at this coordinate, we need to
            # make sure that the coordinate is a valid position
            # and the cell is empty
            condition = row >= 0 and row < IH.NUMBER_OF_ROWS
            condition = condition and col >= 0 and col < IH.NUMBER_OF_COLS
            condition = condition and cell[ IH.GAME_COORD_TYPE_ID_INDEX ] is IH.BASE_CELL

            return condition
        
        elif event == IH.GameEventType.GAME_EVENT_MAKE_ATTACK:
            # In the event that we are trying to make an attack
            # Just make sure that the coordinate is in the base state
            # It is invalid to attack a coordinate that already had a move
            # made on it
            return cell[ IH.GAME_COORD_TYPE_STATE_INDEX ] == IH.CoordStateType.COORD_STATE_BASE
        else:
            # We raise an error if we try to validate an action on
            # a coordinate with an undefined event
            raise AssertionError( f"There isn't a check for validity given the event { event.name }" )

    def ships_are_alive( self, player_type : IH.PlayerTypeEnum ) -> bool:
        """
        Function: Are there ships still alive?

        Inputs: The player's' board
        Outputs: If there are ships still alive

        Description: This function defines the ablity to check if board
                     still has ships that are alive
        """
        # Get the board that we need to check
        board_to_validate = self._host_board if player_type == IH.PlayerTypeEnum.PLAYER_TYPE_HOST else self._join_board

        for row in board_to_validate:
            for cell in row:
                # If we find that there is a cell that has a ship in it
                # and the ship is still alive, return True
                if cell[ IH.GAME_COORD_TYPE_ID_INDEX ] != IH.BASE_CELL and cell[ IH.GAME_COORD_TYPE_STATE_INDEX ] != IH.CoordStateType.COORD_STATE_HIT:
                    return True

        # Return False if we were not able to find one ship
        # that was still alive
        return False
    
    def ship_is_alive( self, player_type : IH.PlayerTypeEnum, ship_id : int ) -> bool:
        """
        Function: Is the particular ship still have

        Inputs: The player's' board, the ship we are testing
        Outputs: If a particular ship is still alive

        Description: This function defines the ablity to check if a unique ship
                     is still alive
        """
        # Get the board that we need to check
        board_to_validate = self._host_board if player_type == IH.PlayerTypeEnum.PLAYER_TYPE_HOST else self._join_board

        for row in board_to_validate:
            for cell in row:
                # If a particular ship still has an unhit cell, return True
                if cell[ IH.GAME_COORD_TYPE_ID_INDEX ] == ship_id and cell[ IH.GAME_COORD_TYPE_STATE_INDEX ] != IH.CoordStateType.COORD_STATE_HIT:
                    return True

        # Return False if we were not able to find any coordinates
        # that weren't hit for a particular ship
        return False
    
    def get_visual_board( self, player_type : IH.PlayerTypeEnum ) -> IH.VisualBoardType:
        """
        Function: Get the visual board

        Inputs: The player's' board
        Outputs: The visual board 

        Description: This function returns a transformed state of the board
                     so that the entire board is represented as a 2D array
                     of integers
        """
        # Initialization a list that will store the visual board
        return_list : IH.VisualBoardType = list()

        # Determine which board that we are wanting to
        # transform
        board_to_transform = self._host_board if player_type == IH.PlayerTypeEnum.PLAYER_TYPE_HOST else self._join_board

        for row in board_to_transform:
            # For every row that is in the board, create
            # an equivalent row that will hold the corrected
            # ids
            row_list = list()

            for cell in row:
                # Basically, for every cell in the board, we
                # only want to show the ID of the board if 
                # the cell has not been attacked. Otherwise,
                # Display the type of action done on the 
                # Cell
                if cell[ IH.GAME_COORD_TYPE_STATE_INDEX ] == IH.CoordStateType.COORD_STATE_HIT:
                    row_list.append( IH.HIT_CELL )

                elif cell[ IH.GAME_COORD_TYPE_STATE_INDEX ] == IH.CoordStateType.COORD_STATE_MISS:
                    row_list.append( IH.MISSED_CELL )

                elif cell[ IH.GAME_COORD_TYPE_STATE_INDEX ] == IH.CoordStateType.COORD_STATE_BASE:
                    row_list.append( cell[ IH.GAME_COORD_TYPE_ID_INDEX ] )

            # Add the transformed row into the return structure
            return_list.append( row_list )

        # Return the transformed board
        return return_list


################################################################################
# Procedures
################################################################################