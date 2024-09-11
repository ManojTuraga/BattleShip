'''
Module: interface_game_presenter.py
Date Created: September 7, 2024
Author: Manoj Turaga
Contributer(s): Manoj Turaga

Inputs: None
Outputs: None

Description: This module is the interface for a presenter. Any presenter that is to be used
             in this codebase needs to inherit from this presenter
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
    from interface_game_view import GameViewInterface

else:
    import interfaces.interface_headers as IH
    from interfaces.interface_game_view import GameViewInterface

################################################################################
# Global Variables
################################################################################

################################################################################
# Types
################################################################################
class GamePresenterInterface( ABC ):
    """
    Description: This is the interface of any presenter that is to be used in this 
                 codebase. An interface is a required set of functions that 
                 must be provided in order for the code to function properly
    """
    def __init__( self, view: GameViewInterface ) -> None:
        """
        Function: Initialization

        Inputs: Instance of view
        Outputs: None

        Description: This function is the initialization function of this interace.
                     We do not say this is an abstract method because python has
                     some issues with declaring __ functions as abstract methods

        Data members: Instance of a view
        """
        raise AssertionError( "Initialization method not implemented" )
    
    @abstractmethod
    def trigger_view_event( self, event, params : dict ) -> dict:
        """
        Function: Trigger View Event

        Inputs: Functions to pass to view trigger
        Outputs: Return from view trigger

        Description: This function is the initialization function of this interace.
                     We do not say this is an abstract method because python has
                     some issues with declaring __ functions as abstract methods
        """
        raise AssertionError( "Trigger View Event function not implemented" )
