'''
Module: interface_game_model.py
Date Created: September 7, 2024
Author: Manoj Turaga
Contributer(s): Manoj Turaga

Inputs: None
Outputs: None

Description: This module is the interface for a model. Any model that is to be used
             In this codebase needs to inherit from this model
'''
################################################################################
# Imports
################################################################################

# This interface is an abstract base class so
# import the abstract base class module along
# with necessary decorators
from abc import ABC, abstractmethod

# Due to Python's importing scheme, need to have
# imports withih this interfaces folder done like this
# so that wee can have both internal and external
# importing schemes
if __name__ == "__main__":
    import interface_headers as IH

else:
    import interfaces.interface_headers as IH


################################################################################
# Global Variables
################################################################################

################################################################################
# Types
################################################################################

class GameModelInterface( ABC ):
    """
    Description: This is the interface of any model that is to be used in this 
                 codebase. An interface is a required set of functions that 
                 must be provided in order for the code to function properly
    """
    def __init__( self ) -> None:
        """
        Function: Initialization

        Inputs: None
        Outputs: None

        Description: This function is the initialization function of this interace.
                     We do not say this is an abstract method because python has
                     some issues with declaring __ functions as abstract methods

        Data members: Instance of a board for the current player and the opponent
        """
        raise AssertionError( "Initialization method not implemented" )
    
    @abstractmethod
    def get_coord( self, player_type : IH.PlayerTypeEnum, coord: IH.SystemCoordType ) -> IH.GameBoardType:
        """
        Function: Get coordinate from board

        Inputs: The Player we want to get the data from, the location of the data
        Outputs: The data in the cell of the board

        Description: This function is the data getter of this interface. We only get
                     coordinate information only because the application that consumes
                     this model does not need to know everything stored in the model
        """
        raise AssertionError( "Get Board method not implemented" )
    
    @abstractmethod
    def update_coord( self, player_type : IH.PlayerTypeEnum, coord: IH.SystemCoordType, new_val: IH.GameCoordType ) -> None:
        """
        Function: Update cell in the board

        Inputs: The Player we want to set the data to, the location of the data, the new data
        Outputs: None

        Description: This function is the data setter of this interface. We only get
                     coordinate information only because the application that consumes
                     this model does not need to know everything stored in the model
        """
        raise AssertionError( "Update Coordinate not implemented" )
    
    @abstractmethod
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
        raise AssertionError( "Is Valid Coordinate is not implemented" )
    
    @abstractmethod
    def ships_are_alive( self, player_type : IH.PlayerTypeEnum ) -> bool:
        """
        Function: Are there ships still alive?

        Inputs: The player's' board
        Outputs: If there are ships still alive

        Description: This function defines the interface to check if board
                     still has ships that are alive
        """
        raise AssertionError( "Ships Are Alive is not implemented" )
    
    @abstractmethod
    def ship_is_alive( self, player_type : IH.PlayerTypeEnum, ship_id : int ) -> bool:
        """
        Function: Is the particular ship still alive

        Inputs: The player's' board, the ship we want to check
        Outputs: If the shjp is still alive

        Description: This function defines the interface to check if a particular
                     ship is still alive
        """
        raise AssertionError( "Ship is Alive is not implemented" )
        
    @abstractmethod
    def get_visual_board( self, player_type : IH.PlayerTypeEnum ) -> IH.VisualBoardType:
        """
        Function: Get the visual board

        Inputs: The player's' board
        Outputs: The visual board 

        Description: This function defines the interface to transform
                     a board into a visual representation that can be
                     consumed by presenter
        """
        raise AssertionError( "Get Visual Board is not implemented" )