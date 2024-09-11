# Implementation of the server/host side for networking.
#
# Only implements a generic server/host, needs to be altered to work 
# with game data rather than just sending messages between a client and
# server/host.
#
# Currently has an input section just for testing as well.

import socket
import interfaces.interface_headers as ihdrs
from interfaces.interface_game_interaction import GameInteractionInterface
    
class Host( GameInteractionInterface ):
   
    
    def __init__( self ) -> None:
        """
        Definition: Setting up the host address, host port and client socket.
        """
        
        self.host = socket.gethostname()
        self.host_port = 4347
        self.client_socket = None 
        
        
    def open_connection( self ) -> None:
        """
        Definition: Opening the connection and listening for a client connection.
        """
        
        host_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        host_socket.bind((self.host, self.host_port))
        host_socket.listen(1)
        
        self.client_socket, _ = host_socket.accept()


    def close_connection( self ) -> None:
        """
        Definition: Closing the port.
        """
        
        self.client_socket.close()
        self.client_socket = None 
    
    
    def send_message( self, msg, msg_type: ihdrs.GameEventType = 0 ) -> None:
        """
        Definition: Sending a message to the client.
        """
        
        self.client_socket.send(msg.encode())
    
    
    def wait_for_message( self, player_type: ihdrs.GameEventType = 0 ) -> str:
        """
        Definition: Waiting for a message from the client.
        """
        
        data = self.client_socket.recv(1024).decode()
        return data 
            

def main():
    """
    Definition: Main loop for the server, starts up the host connection and will wait for a 
                message from the client until it closes the connection.
    """
    
    server = Host()
    server.open_connection()
    
    while True:
        data = server.wait_for_message()
        
        if not data:
            break
        
        print(f"from client: {data}")
        
        msg = input(" -> ")
        server.send_message(msg)
    
    server.close_connection()

    
if __name__ == "__main__":
    main()