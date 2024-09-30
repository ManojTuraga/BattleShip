'''
Module: main.py
Date Created: September 10, 2024
Author: Manoj Turaga
Contributer(s): Manoj Turaga, Henry Marshall, Connor Forristal

Inputs: User Input
Outputs: Outputs an instance of the battle ship game

Description: This module is the launching point for the Battleship program. The
             goal of this game is to sink all of your opponents ships before
             they sink yours
'''
################################################################################
# Imports
################################################################################
import game_view as GV
import game_presenter as GP
import game_model as GM
import client as GC
import host as GH
from AI import AI


from interfaces import interface_headers as IH

import json
################################################################################
# Global Variables
################################################################################
################################################################################
# Procedures
################################################################################
def get_ending_coordinate( start_coordinate, dir, amount : IH.SystemCoordType ) -> IH.SystemCoordType:
    """
    Function: Get Ending Coordinate

    Inputs: Starting coordinate, calulation direction, amount to move
    Output: Ending Coordinate

    Description: This is a helper function that computes the predicted
                 ending coordinate given a starting coordinate and
                 the orientation of ship with the size of the ship
    """
    # Depending on the direction passed, compute the ending
    # coordinate by subtracting the amount from the a particular
    # index in the starting coordinate
    if dir == "V":
        return ( start_coordinate[ 0 ] - amount + 1, start_coordinate[ 1 ] )
    
    if dir == "H":
        return ( start_coordinate[ 0 ], start_coordinate[ 1 ] - amount + 1 )


def main():
    """
    Function: Main

    Inputs: None
    Output: Battleship Game

    Description: This is the main function, which serves as the launching
                 point of the program. This main function will server as
                 the executive process that will control the flow of the
                 battleship game
    """
    # Initializes Instances of the Model, View, and presenter, as
    # well as the variable to hold the connection state
    model = GM.GameModel()
    presenter = GP.GamePresenter( GV.GameView() )
    connection = None
    # The host player will always have the first move
    # Suggest improvement, make RNG?
    turn = IH.PlayerTypeEnum.PLAYER_TYPE_HOST
    # Initialize dictionaries to store the function parameters
    # that we are passing into the presenter, as well as storing
    # the return
    function_parameters = dict()
    function_returns = dict()
    # Initialize variables to store the type of player and the
    # opponent are
    player_type = IH.PlayerTypeEnum.PLAYER_TYPE_HOST
    oppenent_type = IH.PlayerTypeEnum.PLAYER_TYPE_HOST
    # Trigger the initialization event of the presenter to
    # obtain configuration related items, including the number
    # of ships and whether the player is a host or joining player
    function_returns = presenter.trigger_view_event( IH.GameEventType.GAME_EVENT_INITIALIZATION, {} )
    player_type = function_returns[ IH.VIEW_PARAM_PLAYER_TYPE ]
    number_of_ships = function_returns[ IH.VIEW_PARAM_NUM_OF_SHIPS ]
    # Make the opponent be the opposite type of the player
    # create the correct networking state for the current
    # player

    if player_type == IH.PlayerTypeEnum.PLAYER_TYPE_JOIN:
        oppenent_type = IH.PlayerTypeEnum.PLAYER_TYPE_HOST
        connection = GC.Client()
    else:
        oppenent_type = IH.PlayerTypeEnum.PLAYER_TYPE_JOIN
        connection = GH.Host()
        # Prompt for AI selection
        function_returns = presenter.trigger_view_event(IH.GameEventType.GAME_EVENT_AI_SELECTION, {})
        ai_selection = function_returns[IH.VIEW_PARAM_AI_SELECTION]



        if ai_selection:
            # Prompt for AI difficulty
            function_returns = presenter.trigger_view_event(IH.GameEventType.GAME_EVENT_AI_DIFFICULTY, {})
            ai_difficulty = function_returns[IH.VIEW_PARAM_AI_DIFFICULTY]
            # function_parameters[IH.VIEW_PARAM_AI_DIFFICULTY] = ai_difficulty
            ai_opponent = AI(ai_difficulty, number_of_ships)
            ai_opponent.place_ships()
            opponent_type = IH.PlayerTypeEnum.PLAYER_TYPE_AI
    # Initially set the error state of the view to be false
    # as well as setting the initial size of the ship to be
    # the minimum possible number of ships
    function_parameters[ IH.VIEW_PARAM_IS_ERROR_STATE ] = False
    size = IH.MIN_NUM_OF_SHIPS

    direction = "H"
    row = 1
    col = 'A'
    # This loop will continue executing until we have placed
    # all the ships onto the board
    while size <= number_of_ships:
        # Set the size, and the visual boards of the current
        # player and opponent as inputs into the presenter
        function_parameters[ IH.VIEW_PARAM_SIZE ] = size
        function_parameters[ IH.VIEW_PARAM_BOARD ] = model.get_visual_board( player_type )
        function_parameters[ IH.VIEW_PARAM_OPPONENT_BOARD ] = model.get_visual_board( oppenent_type )
        function_parameters[ IH.VIEW_PARAM_DIRECTION ] = direction
        function_parameters[ IH.VIEW_PARAM_ROW ] = row
        function_parameters[ IH.VIEW_PARAM_COL ] = col
        # Trigger the presenter to display the configuration page.
        # On page exit, ensure to reset the error state so that
        # the same errors are not displayed again 
        return_val = presenter.trigger_view_event( IH.GameEventType.GAME_EVENT_PLACE_SHIPS, function_parameters )
        function_parameters[ IH.VIEW_PARAM_IS_ERROR_STATE ] = False
        # Obtain the direction of the ship's orientation and pack
        # the row and column into a coordinate structure
        direction = return_val[ IH.VIEW_PARAM_DIRECTION ]
        row = return_val[ IH.VIEW_PARAM_ROW ]
        col = return_val[ IH.VIEW_PARAM_COL ]
        start_coordinate = ( row, col )
        
        # Convert the coordinate returned by the presenter
        # into system coordinates and compute the ending coordinate
        # based on the values returned by configuration
        start_coordinate_sys = ( IH.PLACEMENT_ROW_TO_SYS_ROW[ start_coordinate[ IH.ROW_INDEX ] ], IH.PLACEMENT_COL_TO_SYS_COL[ start_coordinate[ IH.COLUMN_INDEX ] ] )
        end_coordinate_sys = get_ending_coordinate( start_coordinate_sys, direction, size )
        # Here we are creating a set of all the coordinates
        # that the ship is predicted to take, We use a set
        # to make sure that there are no repeat coordinates
        boat_coords = { ( row, col ) 
                        for row in range( start_coordinate_sys[ IH.ROW_INDEX ], end_coordinate_sys[ IH.ROW_INDEX ] - 1, -1 )
                        for col in range( start_coordinate_sys[ IH.COLUMN_INDEX ], end_coordinate_sys[ IH.COLUMN_INDEX ] - 1, -1 ) }
        # If we find that at least one of the coordinates
        # is not a valid coordinate, we will trigger the error
        # state in the presenter
        for coord in boat_coords:
            if not model.is_valid_coord( player_type, coord, IH.GameEventType.GAME_EVENT_PLACE_SHIPS ):
                function_parameters[ IH.VIEW_PARAM_IS_ERROR_STATE ] = True
        
        # If the presenter is not supposed to be in an
        # error state, we will update the model with the ship
        # selections
        if return_val[ IH.VIEW_PARAM_PLACE_SHIP ] and not function_parameters[ IH.VIEW_PARAM_IS_ERROR_STATE ]:
            for coord in boat_coords:
                new_state = { IH.GAME_COORD_TYPE_ID_INDEX : size, IH.GAME_COORD_TYPE_STATE_INDEX: IH.CoordStateType.COORD_STATE_BASE }
                model.update_coord( player_type, coord, new_state )
            # Increment the size only if we are able to
            # successfully place a ship
            size += 1
   # if opponent_type == IH.PlayerTypeEnum.PLAYER_TYPE_AI:
      #  ai_opponent.place_ships()
    # Re initialize function parameters to have the most
    # up to date data remove any messages that could
    # have been triggered due to previous steps
    function_parameters[ IH.VIEW_PARAM_BOARD ] = model.get_visual_board( player_type )
    function_parameters[ IH.VIEW_PARAM_OPPONENT_BOARD ] = model.get_visual_board( oppenent_type )
    function_parameters[ IH.VIEW_PARAM_IS_ERROR_STATE ] = False
    function_parameters[ IH.VIEW_PARAM_STATE_MESSAGE ] = None
    # Trigger the presenter to display the wait page
    # as well as open the network connection

    if opponent_type != IH.PlayerTypeEnum.PLAYER_TYPE_AI:
        presenter.trigger_view_event( IH.GameEventType.GAME_EVENT_WAIT_FOR_OPPONENT, function_parameters )
        connection.open_connection()
    # Initialize a variable to handle whether
    # the game should end or not
    game_over = False
    
    win = False
    # Execute the following loop while the game
    # can still be played
    # can still be played
    while not game_over:
        function_parameters[IH.VIEW_PARAM_BOARD] = model.get_visual_board(player_type)
        function_parameters[IH.VIEW_PARAM_OPPONENT_BOARD] = model.get_visual_board(opponent_type)
        # The following code logic is executed if it is not
        # the current player's turn
        if player_type != turn:
            if opponent_type == IH.PlayerTypeEnum.PLAYER_TYPE_AI:
                attack_coord = ai_opponent.make_attack()
                row, col = attack_coord
                cell = model.get_coord(player_type, (row, col))
                # If the coordinate is a ship coordinate, and it is not hit already,
                # make sure that it is in the hit state. Otherwise, the opponent missed
                if cell[IH.GAME_COORD_TYPE_ID_INDEX] > IH.BASE_CELL and cell[IH.GAME_COORD_TYPE_STATE_INDEX] != IH.CoordStateType.COORD_STATE_HIT:
                    cell[IH.GAME_COORD_TYPE_STATE_INDEX] = IH.CoordStateType.COORD_STATE_HIT
                    function_parameters[IH.VIEW_PARAM_STATE_MESSAGE] = "Hit!"
                else:
                    cell[IH.GAME_COORD_TYPE_STATE_INDEX] = IH.CoordStateType.COORD_STATE_MISS
                    function_parameters[IH.VIEW_PARAM_STATE_MESSAGE] = "Miss!"

                model.update_coord(player_type, (row, col), cell)
                # Determine if the result of this attack caused the opponent to win
                if not model.ships_are_alive(player_type):
                    game_over = True
                    win = False
                # Update the AI's knowledge of the opponent's board
                ai_opponent.update_opponent_board((row, col), cell[IH.GAME_COORD_TYPE_STATE_INDEX])
                # Make it so the user is now the active player
                turn = player_type

            else:
                # Trigger the presenter's wait for event page and reset
                # the error state and the status state after the call
                presenter.trigger_view_event(IH.GameEventType.GAME_EVENT_WAIT_FOR_OPPONENT, function_parameters)
                function_parameters[IH.VIEW_PARAM_STATE_MESSAGE] = None
                function_parameters[IH.VIEW_PARAM_IS_ERROR_STATE] = False
                
                # Wait until we get a response from the opponent and
                # load the data as a dictionary. Along with that,
                # initialize a variable to store the response that
                # will be sent back
                data = connection.wait_for_message()
                data = json.loads(data)
                response = dict()
                
                # Unpack the data into coordinates and get the current
                # state of the coordinate on the board
                coord = (data[IH.VIEW_PARAM_ROW], data[IH.VIEW_PARAM_COL])
                cell = model.get_coord(player_type, coord)
                # If the coordinate is a ship coordinate, and it is not hit already,
                # make sure that it is in the hit state. Otherwise, the opponent missed
                if cell[IH.GAME_COORD_TYPE_ID_INDEX] > IH.BASE_CELL and cell[IH.GAME_COORD_TYPE_STATE_INDEX] != IH.CoordStateType.COORD_STATE_HIT:
                    response[IH.GAME_COORD_TYPE_STATE_INDEX] = IH.CoordStateType.COORD_STATE_HIT.value
                    cell[IH.GAME_COORD_TYPE_STATE_INDEX] = IH.CoordStateType.COORD_STATE_HIT
                else:
                    response[IH.GAME_COORD_TYPE_STATE_INDEX] = IH.CoordStateType.COORD_STATE_MISS.value
                # Update the player's model with the new data for the attack
                model.update_coord(player_type, coord, cell)
                # Determine if the result of this attack caused the opponent to win
                response[IH.VIEW_PARAM_WIN] = not model.ships_are_alive(player_type)
                response[IH.VIEW_PARAM_SHIP_SUNK] = not model.ship_is_alive(player_type, cell[IH.GAME_COORD_TYPE_ID_INDEX])
                response[IH.VIEW_PARAM_SIZE] = cell[IH.GAME_COORD_TYPE_ID_INDEX]
                #connection.send_message(json.dumps(response))
                
                # Update the state message to allow the presenter to display this
                # message on the next page load
                if cell[IH.GAME_COORD_TYPE_STATE_INDEX] == IH.CoordStateType.COORD_STATE_HIT:
                    function_parameters[IH.VIEW_PARAM_STATE_MESSAGE] = "Hit!"
                else:
                    function_parameters[IH.VIEW_PARAM_STATE_MESSAGE] = "Miss!"
                # If Ship was sunk, indicate as a status message that the ship was sunk
                if response[IH.VIEW_PARAM_SHIP_SUNK]:
                    function_parameters[IH.VIEW_PARAM_STATE_MESSAGE] += " Ship Sunk!"
                # Make it so the user is now the active player
                turn = player_type
                # If the result of the other player's attack caused your board to be destroyed,
                # close the connection and indicate that you lost
                if response[IH.VIEW_PARAM_WIN]:
                    game_over = True
                    win = False

        else:
            if opponent_type == IH.PlayerTypeEnum.PLAYER_TYPE_AI:  # Replace this with your actual condition to check for AI
                # Trigger the presenter to display the attack page
                # Player's turn to attack
                function_parameters[IH.VIEW_PARAM_ROW] = row
                function_parameters[IH.VIEW_PARAM_COL] = col
                while True:
                    function_parameters[IH.VIEW_PARAM_ROW] = row
                    function_parameters[IH.VIEW_PARAM_COL] = col
                    attack = None
                    attack = presenter.trigger_view_event(IH.GameEventType.GAME_EVENT_MAKE_ATTACK, function_parameters)
                    row, col = attack[IH.VIEW_PARAM_ROW], attack[IH.VIEW_PARAM_COL]
                    attack_sys = (IH.PLACEMENT_ROW_TO_SYS_ROW[row], IH.PLACEMENT_COL_TO_SYS_COL[col])

                    if ai_opponent.is_valid_coord(attack_sys):
                        if attack[IH.VIEW_PARAM_PLACE_SHIP]:
                            if opponent_type == IH.PlayerTypeEnum.PLAYER_TYPE_AI:
                                # Player attacks AI
                                hit_result = ai_opponent.check_ship_at(attack_sys)  # Check if there's a ship at the attack coordinates
                                if hit_result == 1:
                                    result_state = IH.CoordStateType.COORD_STATE_HIT
                                    function_parameters[IH.VIEW_PARAM_STATE_MESSAGE] = f"You hit AI's ship at {attack_sys}!"
                                    break
                                else:
                                    result_state= IH.CoordStateType.COORD_STATE_MISS
                                    function_parameters[IH.VIEW_PARAM_STATE_MESSAGE] = f"You missed at {attack_sys}."
                                    break

                ai_opponent.update_coord(attack_sys, IH.CoordStateType.COORD_STATE_HIT, is_opponent=True)

                ai_opponent.update_ai_board((row, col), result_state)
                # Check if the AI has any ships left
                if not ai_opponent.ships_are_alive():
                    game_over = True
                    win = True
                

            else:
                # Trigger the presenter to display the attack page
                attack = None
                

                function_parameters[IH.VIEW_PARAM_ROW] = row
                function_parameters[IH.VIEW_PARAM_COL] = col
                attack = presenter.trigger_view_event(IH.GameEventType.GAME_EVENT_MAKE_ATTACK, function_parameters)
                row = attack[IH.VIEW_PARAM_ROW]
                col = attack[IH.VIEW_PARAM_COL]
                # Remove any messages or errors that are currently displayed on the page
                function_parameters[IH.VIEW_PARAM_STATE_MESSAGE] = None
                function_parameters[IH.VIEW_PARAM_IS_ERROR_STATE] = False
                # Get the system coordinates from the attack
                attack_sys = (IH.PLACEMENT_ROW_TO_SYS_ROW[attack[IH.VIEW_PARAM_ROW]], IH.PLACEMENT_COL_TO_SYS_COL[attack[IH.VIEW_PARAM_COL]])
                # The following block of code is only executed if the attack is valid
                if model.is_valid_coord(opponent_type, attack_sys, IH.GameEventType.GAME_EVENT_MAKE_ATTACK):
                    cell = model.get_coord(opponent_type, attack_sys)
                    if cell[IH.GAME_COORD_TYPE_ID_INDEX] > IH.BASE_CELL and cell[IH.GAME_COORD_TYPE_STATE_INDEX] != IH.CoordStateType.COORD_STATE_HIT:
                        cell[IH.GAME_COORD_TYPE_STATE_INDEX] = IH.CoordStateType.COORD_STATE_HIT
                        function_parameters[IH.VIEW_PARAM_STATE_MESSAGE] = "Hit!"
                    else:
                        cell[IH.GAME_COORD_TYPE_STATE_INDEX] = IH.CoordStateType.COORD_STATE_MISS
                        function_parameters[IH.VIEW_PARAM_STATE_MESSAGE] = "Miss!"

                    model.update_coord(opponent_type, attack_sys, cell)
                    # Determine if the result of this attack caused the opponent to win
                    if not model.ships_are_alive(opponent_type):
                        game_over = True
                        win = True
                    # Send the attack result to the opponent
                    response = {
                        IH.VIEW_PARAM_ROW: attack[IH.VIEW_PARAM_ROW],
                        IH.VIEW_PARAM_COL: attack[IH.VIEW_PARAM_COL],
                        IH.GAME_COORD_TYPE_STATE_INDEX: cell[IH.GAME_COORD_TYPE_STATE_INDEX].value,
                        IH.VIEW_PARAM_WIN: game_over,
                        IH.VIEW_PARAM_SHIP_SUNK: not model.ship_is_alive(opponent_type, cell[IH.GAME_COORD_TYPE_ID_INDEX]),
                        IH.VIEW_PARAM_SIZE: cell[IH.GAME_COORD_TYPE_ID_INDEX]
                    }

                    connection.send_message(json.dumps(response)) 
                    # Make it so the opponent is now the active player
                    turn = opponent_type

                else:
                    function_parameters[IH.VIEW_PARAM_IS_ERROR_STATE] = True

    else:
        # Once the Game is over, display the game over page
        function_parameters[IH.VIEW_PARAM_BOARD] = model.get_visual_board(player_type)
        function_parameters[IH.VIEW_PARAM_OPPONENT_BOARD] = model.get_visual_board(opponent_type)
        function_parameters[IH.VIEW_PARAM_WIN] = win
        presenter.trigger_view_event(IH.GameEventType.GAME_EVENT_GAME_END, function_parameters)
        pass

    '''
    while not game_over:
        function_parameters[ IH.VIEW_PARAM_BOARD ] = model.get_visual_board( player_type )
        function_parameters[ IH.
        VIEW_PARAM_OPPONENT_BOARD ] = model.get_visual_board( oppenent_type )
        # The following code logic is executed if it is not
        # the current players turn
        if player_type != turn:
            
            # Trigger the presenter's wait for event page and reset
            # the error state and the status state after the call
            presenter.trigger_view_event( IH.GameEventType.GAME_EVENT_WAIT_FOR_OPPONENT, function_parameters )
            function_parameters[ IH.VIEW_PARAM_STATE_MESSAGE ] = None
            function_parameters[ IH.VIEW_PARAM_IS_ERROR_STATE ] = False
            
            # Wait until we get a response from the opponent and
            # load the data as a dictionary. Along with that,
            # initialize a variable to store the response that
            # will be sent back
            data = connection.wait_for_message()
            data = json.loads( data )
            response = dict()
            
            # Unpack the data into coordinates and get the current
            # state of the coordinate on the board
            coord = ( data[ IH.VIEW_PARAM_ROW ], data[ IH.VIEW_PARAM_COL ] )
            cell = model.get_coord( player_type, coord )
            # If the coordinate is a ship coordinate, and it is not hit already,
            # make sure that it is in the hit state. Otherwise, the the opponent
            # missed 
            if cell[ IH.GAME_COORD_TYPE_ID_INDEX ] > IH.BASE_CELL and cell[ IH.GAME_COORD_TYPE_STATE_INDEX ] != IH.CoordStateType.COORD_STATE_HIT:
                response[ IH.GAME_COORD_TYPE_STATE_INDEX ] = IH.CoordStateType.COORD_STATE_HIT.value
                cell[ IH.GAME_COORD_TYPE_STATE_INDEX ] = IH.CoordStateType.COORD_STATE_HIT

            else:
                response[ IH.GAME_COORD_TYPE_STATE_INDEX ] =  IH.CoordStateType.COORD_STATE_MISS.value
                cell[ IH.GAME_COORD_TYPE_STATE_INDEX ] = IH.CoordStateType.COORD_STATE_MISS
            # Update the player's model with the new data for the attack
            model.update_coord( player_type, coord, cell )
            # Determine if the result of this attack cause the opponent
            # to win and send the message
            response[ IH.VIEW_PARAM_WIN ] = not model.ships_are_alive( player_type )
            response[ IH.VIEW_PARAM_SHIP_SUNK ] = not model.ship_is_alive( player_type, cell[ IH.GAME_COORD_TYPE_ID_INDEX ] )
            response[ IH.VIEW_PARAM_SIZE ] = cell[ IH.GAME_COORD_TYPE_ID_INDEX ]
            connection.send_message( json.dumps( response ) )
            
            # Update the state message to allow the presenter to display this
            # message on the next page load
            if cell[ IH.GAME_COORD_TYPE_STATE_INDEX ] == IH.CoordStateType.COORD_STATE_HIT:
                function_parameters[ IH.VIEW_PARAM_STATE_MESSAGE ] = f"The opponent's move at row={ IH.SYS_ROW_TO_PLACMENT_ROW[ coord[ 0 ] ] }, col={ IH.SYS_COL_TO_PLACMENT_COL[ coord[ 1 ] ] } hit!"

            else:
                function_parameters[ IH.VIEW_PARAM_STATE_MESSAGE ] = f"The opponent's move at row={ IH.SYS_ROW_TO_PLACMENT_ROW[ coord[ 0 ] ] }, col={ IH.SYS_COL_TO_PLACMENT_COL[ coord[ 1 ] ] } missed!"
            # If Ship was sunk, indictate as a status message that the ship was sunk
            if response[ IH.VIEW_PARAM_SHIP_SUNK ]:
                function_parameters[ IH.VIEW_PARAM_STATE_MESSAGE ] += f"\nShip of size { cell[ IH.GAME_COORD_TYPE_ID_INDEX ] } was sunk!"
            # Make it so the user is now the active
            # player
            turn = player_type
            # If the result of the other player's attack
            # caused your board to be destoryed, close
            # the connection and indicate that you lost
            if response[ IH.VIEW_PARAM_WIN ]:
                connection.close_connection()
                game_over = True
                win = False

        else:
            # Trigger the presenter to display the attack page
            attack = None

            function_parameters[ IH.VIEW_PARAM_ROW ] = row
            function_parameters[ IH.VIEW_PARAM_COL ] = col
            attack = presenter.trigger_view_event( IH.GameEventType.GAME_EVENT_MAKE_ATTACK, function_parameters )
            row = attack[ IH.VIEW_PARAM_ROW ]
            col = attack[ IH.VIEW_PARAM_COL ]
            # Remove any messages or errors that are currently
            # displayed on the page
            function_parameters[ IH.VIEW_PARAM_STATE_MESSAGE ] = None
            function_parameters[ IH.VIEW_PARAM_IS_ERROR_STATE ] = False
            # Get the system coordinates from the attack
            attack_sys = ( IH.PLACEMENT_ROW_TO_SYS_ROW[ attack[ IH.VIEW_PARAM_ROW ] ], IH.PLACEMENT_COL_TO_SYS_COL[ attack[ IH.VIEW_PARAM_COL ] ] )
            # The following block of code is only executed if the attack is valid
            if model.is_valid_coord( oppenent_type, attack_sys, IH.GameEventType.GAME_EVENT_MAKE_ATTACK ):
                # Check if the user wants to place attack at this location
                if attack[ IH.VIEW_PARAM_PLACE_SHIP ]:
                    # Get a reference to the cell of the coordinate
                    # that you are attacking
                    cell = model.get_coord( oppenent_type, attack_sys )
                    
                    # Pack the attack's location into the a json
                    # structure and send it to the other player
                    data = dict()
                    data[ IH.VIEW_PARAM_ROW ] = attack_sys[ IH.ROW_INDEX ]
                    data[ IH.VIEW_PARAM_COL ] = attack_sys[ IH.COLUMN_INDEX ]
                    connection.send_message( json.dumps( data ) )
                    # Obtain the response from the other player
                    response = json.loads( connection.wait_for_message() )
                    
                    model.update_coord( oppenent_type, attack_sys, { IH.GAME_COORD_TYPE_ID_INDEX: cell[ IH.GAME_COORD_TYPE_ID_INDEX ], 
                                                                    IH.GAME_COORD_TYPE_STATE_INDEX: IH.CoordStateType( response[ IH.GAME_COORD_TYPE_STATE_INDEX ] ) } )
                    
                    # Update the state message to allow the presenter to display this
                    # message on the next page load
                    if IH.CoordStateType( response[ IH.GAME_COORD_TYPE_STATE_INDEX ] ) == IH.CoordStateType.COORD_STATE_HIT:
                        function_parameters[ IH.VIEW_PARAM_STATE_MESSAGE ] = f"Your move at row={ attack[ IH.VIEW_PARAM_ROW ] }, col={ attack[ IH.VIEW_PARAM_COL ] } hit!"

                    else:
                        function_parameters[ IH.VIEW_PARAM_STATE_MESSAGE ] = f"Your move at row={ attack[ IH.VIEW_PARAM_ROW ] }, col={ attack[ IH.VIEW_PARAM_COL ] } missed!"

                    if response[ IH.VIEW_PARAM_SHIP_SUNK ]:
                        function_parameters[ IH.VIEW_PARAM_STATE_MESSAGE ] += f"\nShip of size { response[ IH.VIEW_PARAM_SIZE ] } was sunk!"
                    # If the result of the attack ended the opponenet
                    # Indicate that you won the game!
                    if response[ IH.VIEW_PARAM_WIN ]:
                        connection.close_connection()
                        game_over = True
                        win = True

                    turn = oppenent_type

            else:
                # We are only in an error state if the
                # user attempted to attack a coordinate
                # that has already been hit. Allow the user
                # to keep inputting until they get it right
                function_parameters[ IH.VIEW_PARAM_IS_ERROR_STATE ] = True
    
    else:
        # Once the Game is over, display the game over page
        function_parameters[ IH.VIEW_PARAM_BOARD ] = model.get_visual_board( player_type )
        function_parameters[ IH.VIEW_PARAM_OPPONENT_BOARD ] = model.get_visual_board( oppenent_type )
        function_parameters[ IH.VIEW_PARAM_WIN ] = win
        presenter.trigger_view_event( IH.GameEventType.GAME_EVENT_GAME_END, function_parameters )
        pass
    '''

if __name__ == "__main__":
    main()