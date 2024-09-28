'''
Module: interface_game_view.py
Date Created: September 7, 2024
Author: Manoj Turaga
Contributer(s): Manoj Turaga, Clare Channel, Henry Marshall

Inputs: None
Outputs: None

Description: This module is the interface for a view. Any view that is to be used
             in this codebase needs to inherit from this view interface
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
class GameViewInterface( ABC ):
    def __init__( self ):
        """
        Function: Initialization

        Inputs: None
        Outputs: None

        Description: This function is the initialization function of this interace.
                     We do not say this is an abstract method because python has
                     some issues with declaring __ functions as abstract methods
        """
        raise AssertionError( "Initialization method not implemented" )
    
    @abstractmethod
    def draw_start_page( self, params: dict ) -> dict:
        """
        Function: Draw Start Page

        Inputs: Configuration inputs
        Outputs: Configuration outputs

        Description: This function is the interface function for drawing
                     the start page
        """
        raise AssertionError( "Draw Start Page function not implemented" )
    
    @abstractmethod
    def prompt_ship_init( self, params: dict ) -> dict:
        """
        Function: Prompt Ship Initialization

        Inputs: Configuration inputs
        Outputs: Configuration outputs

        Description: This function is the interface function for getting
                     the initial ship placements from the user
        """
        raise AssertionError( "Draw Start Page function not implemented" )
    
    @abstractmethod
    def prompt_user_attack( self, params : dict ) -> dict:
        """
        Function: Prompt User Attack

        Inputs: Configuration inputs
        Outputs: Configuration outputs

        Description: This function is the interface function for getting
                     the user's attack
        """
        raise AssertionError( "Prompt User Attack function not implemented" )
    
    @abstractmethod
    def prompt_wait_page( self, params : dict ) -> dict:
        """
        Function: Prompt Wait Page

        Inputs: Configuration inputs
        Outputs: Configuration outputs

        Description: This function is the interface function for drawing
                     the wait page
        """
        raise AssertionError( "Prompt Wait Page function not implemented" )
    
    @abstractmethod
    def draw_game_over_page( self, params : dict ) -> dict:
        """
        Function: Draw Game Over Page

        Inputs: Configuration inputs
        Outputs: Configuration outputs

        Description: This function is the interface function for drawing
                     the game over
        """
        raise AssertionError( "Draw Game Over Page function not implemented" )
    
    @abstractmethod
    def draw_grid( self, params: dict ) -> dict:
        """
        Function: Draw Grid

        Inputs: Configuration inputs
        Outputs: Configuration outputs

        Description: This function is the interface function for drawing
                     the grid onto the page
        """
        raise AssertionError( "Draw Grid Function not implemented" )\
    
    @abstractmethod
    def prompt_ai_selection(self, params: dict) -> dict:
        """
        Function: Prompt AI Selection

        Inputs: Configuration inputs
        Outputs: Configuration outputs

        Description: This function is the interface function for selecting
                    whether to play with AI or not.
        """
        raise AssertionError("Prompt AI Selection function not implemented")

    @abstractmethod
    def prompt_ai_difficulty(self, params: dict) -> dict:
        """
        Function: Prompt AI Difficulty

        Inputs: Configuration inputs
        Outputs: Configuration outputs

        Description: This function is the interface function for selecting
                    the difficulty level of the AI.
        """
        raise AssertionError("Prompt AI Difficulty function not implemented")