"""
Module: interface_headers.py
Creation Date: September 7, 2024
Author: Manoj Turaga
Contributors: Manoj Turaga
Sources:

Description:
    This module holds all the global constants and types that are used
    throughout the codebase. Allows use to standardize implementation
    across files
"""
################################################################################
# Imports
################################################################################
from enum import Enum

################################################################################
# Global Variables
################################################################################

# The following constants are used to interact with the view
# and the network. We define these constants here so that
# the entire codebase is restricted to only using these
# constans as message keys
VIEW_PARAM_PLAYER_TYPE = "PLAYER_TYPE"
VIEW_PARAM_NUM_OF_SHIPS = "NUM_OF_SHIPS"
VIEW_PARAM_DIRECTION = "DIRECTION"
VIEW_PARAM_ROW = "ROW"
VIEW_PARAM_COL = "COL"
VIEW_PARAM_IS_ERROR_STATE = "IS_ERROR_STATE"
VIEW_PARAM_BOARD = "BOARD"
VIEW_PARAM_OPPONENT_BOARD = "OPPONENT_BOARD"
VIEW_PARAM_SIZE = "SIZE"
VIEW_PARAM_STATE_MESSAGE = "STATE_MESSAGE"
VIEW_PARAM_WIN = "WIN"
VIEW_PARAM_SHIP_SUNK = "SHIP_SUNK"

# Variables to map to row and column locations to minimize magic
# numbers in the system
ROW_INDEX = 0
COLUMN_INDEX = 1

# Size of the board
NUMBER_OF_ROWS = 10
NUMBER_OF_COLS = 10

# Amount of ships that can be placed onto the board
MIN_NUM_OF_SHIPS = 1
MAX_NUM_OF_SHIPS = 5

# We need a way to make sure we standardize the game coordinates
# to the system coordinates. The Game indicates that rows will
# be numbered 1-10, and columns will be labeled A-J, so define
# a set of mappings that can convert this
PLACEMENT_ROW_TO_SYS_ROW = { 1 : 0, 
                             2 : 1, 
                             3 : 2, 
                             4 : 3, 
                             5 : 4, 
                             6 : 5, 
                             7 : 6, 
                             8 : 7, 
                             9 : 8, 
                             10 : 9 }

PLACEMENT_COL_TO_SYS_COL = { 'A' : 0, 
                             'B' : 1, 
                             'C' : 2, 
                             'D' : 3, 
                             'E' : 4, 
                             'F' : 5, 
                             'G' : 6, 
                             'H' : 7, 
                             'I' : 8, 
                             'J' : 9 }

# Invert the previous mappings to allow for fast reversal
SYS_ROW_TO_PLACMENT_ROW = { val: key for key, val in PLACEMENT_ROW_TO_SYS_ROW.items() }
SYS_COL_TO_PLACMENT_COL = { val: key for key, val in PLACEMENT_COL_TO_SYS_COL.items() }

# Ensure that all possible mappings are accounted for
assert( len( PLACEMENT_ROW_TO_SYS_ROW ) == NUMBER_OF_ROWS )
assert( len( PLACEMENT_COL_TO_SYS_COL ) == NUMBER_OF_COLS )

# Define variables to refer to the state of the coordinate position
GAME_COORD_TYPE_ID_INDEX = "ID"
GAME_COORD_TYPE_STATE_INDEX = "STATE"

# Define these variables here so that we
# how the application know what non active
# ship cells are stored
BASE_CELL = 0
HIT_CELL = -1
MISSED_CELL = -2


################################################################################
# Types
################################################################################

# This type is used to know if the player is
# hosting or joining a game
class PlayerTypeEnum( Enum ):
    PLAYER_TYPE_HOST = 0
    PLAYER_TYPE_JOIN = 1

# This type is used to determine the state of the
# coordinate
class CoordStateType( Enum ):
    COORD_STATE_BASE = 0
    COORD_STATE_MISS = 1
    COORD_STATE_HIT = 2

# This type is used ot determine the type of event that the
# game is currently processing
class GameEventType( Enum ):
    GAME_EVENT_INITIALIZATION = 0
    GAME_EVENT_PLACE_SHIPS = 1
    GAME_EVENT_MAKE_ATTACK = 2
    GAME_EVENT_WAIT_FOR_OPPONENT = 3
    GAME_EVENT_GAME_END = 4

# Typdef the difference between actual coordinates (the input)
# and system coordinates (how it should be stored)
ActualCoordType = tuple[ int, str ]
SystemCoordType = tuple[ int, int ]

# Typedef how the boards will be structured
GameCoordType = dict[ str ]
GameBoardType = list[ list[ GameCoordType ] ]

# Typedef how the boards will be passed between
# the different levels
VisualBoardType = list[ list[ int ] ]



