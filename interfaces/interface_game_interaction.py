if __name__ == "__main__":
    import interface_headers as ihdrs

else:
    import interfaces.interface_headers as ihdrs


from abc import ABC, abstractmethod

class GameInteractionInterface( ABC ):
    @abstractmethod
    def __init__( self ) -> None:
        raise AssertionError( "Initialization method not implemented" )
    
    @abstractmethod
    def send_message( self, msg_type: ihdrs.GameEventType, msg ) -> None:
        raise AssertionError( "Send Message method not implemented" )
    
    @abstractmethod
    def wait_for_message( self, player_type: ihdrs.GameEventType ):
        raise AssertionError( "Wait for message method not implemented" )
    
    @abstractmethod
    def open_connection( self ) -> None:
        raise AssertionError( "Open Connection not implemented" )
    
    @abstractmethod
    def close_connection( self ) -> None:
        raise AssertionError( "Close Connection not implemented" )
        
