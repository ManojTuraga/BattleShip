if __name__ == "__main__":
    import interface_headers as ihdrs

else:
    import interfaces.interface_headers as ihdrs
    
from abc import ABC, abstractmethod

class GameViewInterface( ABC ):
    def __init__( self ):
        raise AssertionError( "Initialization method not implemented" )
    
    @abstractmethod
    def draw_start_page( self ):
        raise AssertionError( "Draw Start Page function not implemented" )
    
    # Update interface functions when function signatures are made
    # see the interface header file for more info. Every event
    # should have a function that corresponds to it
    # TODO Manoj: If going CLI, don't quite know what the function
    # signatures need yet, feel free to figure these out
    @abstractmethod
    def draw_grid( self, grid : ihdrs.GameBoardType  ) -> None:
        raise AssertionError( "Draw Grid Function not implemented" )