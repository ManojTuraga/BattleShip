"""
Module: player_model.py
Creation Date: September 2nd, 2024
Author: Manoj Turaga
Contributors:
Sources:

Description:
    This model controls the behavior of a player instance, which includes a single player's board,
    the ships on the board, and the overall state of the player

Inputs:
    Actions done to affect the player state
Outputs:
    Current state of the player
"""

####
# General Imports
####

from headers import *

def _convert_placement_to_coords( coord: tuple[ int, str ] ):
        row = coord[ 0 ]
        col = coord[ 1 ]

        return ( PLACEMENT_ROW_TO_SYS_ROW[ row ], PLACEMENT_COL_TO_SYS_COL[ col ] )

class Player:
    def __init__( self, ship_placements : dict[ str, list:[ tuple[ int, str ] ] ] = None ):
        '''

        '''

        # Create the instance of the board, which will be an
        # N x M array initialized to None
        self._board = [ [ { "ID"    : None,
                            "STATE" : CoordState.BASE } ] * NUMBER_OF_COLS ] * NUMBER_OF_ROWS

        # If the ship_placements variable is not None, that means that
        # this player is the active player, so we need to set the ships
        # on the board
        if ship_placements is not None:
            self._place_ships_on_board( ship_placements )
                
    def _place_ships_on_board( self, ship_placements ):
        for ship_id, ship_placement in ship_placements:
            for ship_coordinate in ship_placement:
                sys_row, sys_col = _convert_placement_to_coords( ship_coordinate )
                
                if self._board[ sys_row ][ sys_col ][ "ID" ] != None:
                    raise IndexError( "Ship Placement conflicts with another placement" )
                
                self._board[ sys_row ][ sys_col ][ "ID" ] = ship_id