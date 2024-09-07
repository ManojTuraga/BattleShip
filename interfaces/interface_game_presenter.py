if __name__ == "__main__":
    import interface_headers as ihdrs
    from interface_game_view import GameViewInterface

else:
    import interfaces.interface_headers as ihdrs
    from interfaces.interface_game_view import GameViewInterface

from abc import ABC, abstractmethod

class GamePresenterInterface( ABC ):
    def __init__( self, view: GameViewInterface ) -> None:
        raise AssertionError( "Initialization method not implemented" )
    
    # Update interface functions when function signatures are made
    # see the interface header file for more info. Every event
    # should have a function that corresponds to it
    @abstractmethod
    def print_board( self ) -> None:
        raise AssertionError( "Print Board method not implemented" )
    
    @abstractmethod
    def convert_to_sys_coords( self, game_coords: ihdrs.ActualCoordType ) -> ihdrs.SystemCoordType:
        raise AssertionError( "Convert To System Coordinates not implemented" )
    
    @abstractmethod
    def convert_to_actual_coords( self, sys_coords: ihdrs.SystemCoordType ) -> ihdrs.ActualCoordType:
        raise AssertionError( "convert to actual coordinates not implemented" )
