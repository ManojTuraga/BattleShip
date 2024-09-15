'''
Module: client.py
Date Created: September 10, 2024
Author: Connor Forristal
Contributer(s):

Description: This module implements a network interaction for the client side
             of the game
'''
################################################################################
# Imports
################################################################################
import socket
import interfaces.interface_headers as IH
from interfaces.interface_game_interaction import GameInteractionInterface

################################################################################
# Types
################################################################################
class Client( GameInteractionInterface ):
    
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
        Definition: Opening the connection and listening for and connecting to the host.
        """
        
        # Create a client socket and connect to the host socket
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.host_port))
    
    def close_connection( self ) -> None:
        """
        Definition: Closing the port.
        """
        
        # Close the client socket
        self.client_socket.close()
        self.client_socket = None 

    def send_message( self, msg ) -> None:
        """
        Definition: Sending a message to the server.
        """
        
        # Send an encoded string to the host
        self.client_socket.send(msg.encode())
        
        
    def wait_for_message( self ):
        """
        Definition: Waiting for a message from the server.
        """
        
        # Decode the encoded string sent by the host
        data = self.client_socket.recv(1024).decode()
        return data