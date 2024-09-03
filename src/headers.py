####
# General Imports
####
from enum import Enum

class CoordState( Enum ):
    BASE = 0
    HIT = 1
    MISS = 2

# As the per the requirements of the game, the board will need
# to have 10 rows and 10 columns, define these variables to
# not have any magic numbers in the code
NUMBER_OF_ROWS = 10
NUMBER_OF_COLS = 10

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

# Define variables to refer to the state of the coordinate position

# Ensure that all possible mappings are accounted for
assert( len( PLACEMENT_ROW_TO_SYS_ROW ) == NUMBER_OF_ROWS )
assert( len( PLACEMENT_COL_TO_SYS_COL ) == NUMBER_OF_COLS )