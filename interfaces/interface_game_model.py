if __name__ == "__main__":
    import interface_headers as ihdrs

else:
    import interfaces.interface_headers as ihdrs

from abc import ABC, abstractmethod

class GameModelInterface( ABC ):
    def __init__( self ) -> None:
        raise AssertionError( "Initialization method not implemented" )
    
    @abstractmethod
    def get_board( self, player_type: ihdrs.PlayerTypeEnum ) -> ihdrs.GameBoardType:
        raise AssertionError( "Get Board method not implemented" )
    
    @abstractmethod
    def update_board( self, player_type: ihdrs.PlayerTypeEnum, new_board: ihdrs.GameBoardType ) -> None:
        raise AssertionError( "Update Board method not implemented" )
    
    @abstractmethod
    def get_coord( self, player_type: ihdrs.PlayerTypeEnum, coord: ihdrs.SystemCoordType ) -> ihdrs.GameBoardType:
        raise AssertionError( "Get Coordinate not implemented" )
    
    @abstractmethod
    def update_coord( self, player_type: ihdrs.PlayerTypeEnum, coord: ihdrs.SystemCoordType, new_val: ihdrs.GameCoordType ) -> None:
        raise AssertionError( "Update Coordinate not implemented" )
        
