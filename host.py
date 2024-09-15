'''
Module: host.py
Date Created: September 10, 2024
Author: Connor Forristal
Contributer(s):

Description: This module implements a network interaction for the host side
             of the game

Inputs: Messages to Send
Outputs: Messages to Receive

Sources: DigitalOcean
'''

# Prefacing: The following code is an implementation of logic that is sourced
# form https://www.digitalocean.com/community/tutorials/python-socket-programming-server-client.
# This site details how one would use default python libraries and we just applied it to our
# own project

################################################################################
# Imports
################################################################################
import socket
import interfaces.interface_headers as IH
from interfaces.interface_game_interaction import GameInteractionInterface
    
################################################################################
# Types
################################################################################
class Host( GameInteractionInterface ):
    def __init__( self ) -> None:
        """
        Definition: Setting up the host address, host port and client socket.
        """
        
        # Declare the members of this class. For now, we will be using
        # networking protocols on the same host. Can easily be modified
        # to do networking across multiple hosts
        self.host = socket.gethostname()
        self.host_port = 5014
        self.client_socket = None 
        
        
    def open_connection( self ) -> None:
        """
        Definition: Opening the connection and listening for a client connection.
        """
        
        # Create and bind a socket to the host ip and port
        host_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        host_socket.bind((self.host, self.host_port))

        # Listen for connections from a client
        host_socket.listen(1)
        
        # Store the client socket once a connection is established
        self.client_socket, _ = host_socket.accept()


    def close_connection( self ) -> None:
        """
        Definition: Closing the port.
        """
        
        # Close the connection to the client socket
        self.client_socket.close()
        self.client_socket = None 
    
    
    def send_message( self, msg ) -> None:
        """
        Definition: Sending a message to the client.
        """
        
        # Send an encoded string on the socket
        self.client_socket.send(msg.encode())
    
    
    def wait_for_message( self ) -> str:
        """
        Definition: Waiting for a message from the client.
        """
        
        # Decode the encoded string and return to calling function
        data = self.client_socket.recv(1024).decode()
        return data