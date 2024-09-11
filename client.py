# Implementation of the client side for networking.
#
# Only implements a generic client, needs to be altered to work 
# with game data rather than just sending messages between a client and
# server/host.
#
# Currently has an input section just for testing as well.

import socket
import interfaces.interface_headers as ihdrs
from interfaces.interface_game_interaction import GameInteractionInterface


class Client( GameInteractionInterface ):
    
    
    def __init__( self ) -> None:
        """
        Definition: Setting up the host address, host port and client socket.
        """
        
        self.host = socket.gethostname()
        self.host_port = 4347
        self.client_socket = None 
    
    
    def open_connection(self) -> None:
        """
        Definition: Opening the connection and listening for and connecting to the host.
        """
        
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.host_port))
    
    
    def close_connection( self ) -> None:
        """
        Definition: Closing the port.
        """
        
        self.client_socket.close()
        self.client_socket = None 
    
    
    def send_message( self, msg, msg_type: ihdrs.GameEventType = 0) -> None:
        """
        Definition: Sending a message to the server.
        """
        
        self.client_socket.send(msg.encode())  # send message
        
        
    def wait_for_message( self, player_type: ihdrs.GameEventType = 0):
        """
        Definition: Waiting for a message from the server.
        """
        
        data = self.client_socket.recv(1024).decode()  # receive response
        return data
        

def main():
    """
    Definition: Main loop for the client, connects to the server before sending messages,
                eventually closing the connection.
    """
    
    client = Client()
    client.open_connection()
    
    while True:
        
        msg = input(" -> ")
        if msg == "quit":
            break
        
        client.send_message(msg)
        
        data = client.wait_for_message()
        print(f"from server: {data}")
            
    client.close_connection()

    
if __name__ == "__main__":
    main()