'''
Module: interface_game_model.py
Date Created: September 7, 2024
Author: Manoj Turaga
Contributer(s): Manoj Turaga

Description: This module is just the interface that defines the interaction
             between two instances of the game
'''
################################################################################
# Imports
################################################################################

# Due to Python's importing scheme, need to have
# imports withih this interfaces folder done like this
# so that wee can have both internal and external
# importing schemes
if __name__ == "__main__":
    import interface_headers as IH

else:
    import interfaces.interface_headers as IH

# This interface is an abstract base class so
# import the abstract base class module along
# with necessary decorators
from abc import ABC, abstractmethod

class GameInteractionInterface( ABC ):
    def __init__( self ) -> None:
        """
        Function: Initialization

        Description: This function is the initialization function of this interace.
                     We do not say this is an abstract method because python has
                     some issues with declaring __ functions as abstract methods
        """
        raise AssertionError( "Initialization method not implemented" )
    
    @abstractmethod
    def send_message( self, msg ) -> None:
        """
        Function: Send Message

        Description: This is the interface function to be able to send
                     a message to the other player
        """
        raise AssertionError( "Send Message method not implemented" )
    
    @abstractmethod
    def wait_for_message( self ):
        """
        Function: Wait For Message

        Description: This is the interface function to be able to wait for
                     a message from the player
        """
        raise AssertionError( "Wait for message method not implemented" )
    
    @abstractmethod
    def open_connection( self ) -> None:
        """
        Function: Send Message

        Description: This is the interface function to be able to open a connection
        """
        raise AssertionError( "Open Connection not implemented" )
    
    @abstractmethod
    def close_connection( self ) -> None:
        """
        Function: Close Message

        Description: This is the interface function to be able to close a connection
        """
        raise AssertionError( "Close Connection not implemented" )
        
