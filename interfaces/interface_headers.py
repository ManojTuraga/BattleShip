from enum import Enum

class PlayerTypeEnum( Enum ):
    PLAYER_TYPE_HOST = 0
    PLAYER_TYPE_JOIN = 1

class CoordStateType( Enum ):
    COORD_STATE_BASE = 0
    COORD_STATE_MISS = 1
    COORD_STATE_HIT = 2

class GameEventType( Enum ):
    GAME_EVENT_INITIALIZATION = 0
    GAME_EVENT_DRAW_BOARDS = 1
    GAME_EVENT_MAKE_ATTACK = 2
    GAME_EVENT_WAIT_OPPONENT = 3
    GAME_EVENT_CONCEDE = 4
    GAME_EVENT_GAME_END = 5

ShipIDType = str | None

ActualCoordType = tuple[ str, int ]
SystemCoordType = tuple[ int, int ]

GameCoordType = tuple[ ShipIDType, CoordStateType ]
GameBoardType = list[ list[ GameCoordType ] ]


NUMBER_OF_ROWS = 10
NUMBER_OF_COLS = 10