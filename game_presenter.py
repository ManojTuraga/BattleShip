'''
Module: game_presenter.py
Date Created: September 10, 2024
Author: Ceres Botkin
Contributer(s): Ceres Botkin, Manoj Turaga

Inputs: Data provided by the View
Outputs: Outputs Data to the view

Description: This module is an implemtation of the game view interface. This
             module will output the state of the game to the console and
             update the data in the model
'''

################################################################################
# Imports
################################################################################

# Import the general headers and the interface for
# the game view. We also need to import the
# interface of view and model because the presenter will
# consume them and utilize it
from interfaces import interface_headers as IH
from interfaces import interface_game_presenter as IGP
from interfaces import interface_game_view as IGV


################################################################################
# Global Variables and Constants
################################################################################


################################################################################
# Types
################################################################################
TRIGGER_TO_FUNCTION_FUNC_IDX = 0
TRIGGER_TO_FUNCTION_PARAM_IDX = 1

# Declare an implementation of the View Interface specified
# in the interfaces directory. As long as all the functions
# specified there are implemented, this will be a valid model
# that we can use
class GamePresenter( IGP.GamePresenterInterface ):
    def __init__( self, view: IGV.GameViewInterface ):
        """
        Function: Initialization

        Inputs: Instance of View
        Outputs: None

        Description: This is the initialization function for ths implementation
                     of the presenter. The presenter will take in a view object
                     and use this to control what is being displayed based on
                     the data in the model and the data provided to it
        """
        # Declare and Initialize Presenter Members
        self._view_instance : IGV.GameViewInterface = view
        self._player_type : IH.PlayerTypeEnum = IH.PlayerTypeEnum.PLAYER_TYPE_HOST
        pass

    def trigger_view_event( self, event, params : dict ) -> dict:
        """
        Function: Trigger view event

        Inputs: Instance of View
        Outputs: None

        Description: This is the initialization function for ths implementation
                     of the presenter. The presenter will take in a view object
                     and use this to control what is being displayed based on
                     the data in the model and the data provided to it
        """
        # This is a mapping between game events and the corresponding
        # View functions
        message_to_view_event_map = \
            {
            IH.GameEventType.GAME_EVENT_INITIALIZATION:     ( self._view_instance.draw_start_page,    dict( {}, **params ) ),
            IH.GameEventType.GAME_EVENT_PLACE_SHIPS:        ( self._view_instance.prompt_ship_init,   dict( {}, **params ) ),
            IH.GameEventType.GAME_EVENT_MAKE_ATTACK:        ( self._view_instance.prompt_user_attack, dict( {}, **params ) ),
            IH.GameEventType.GAME_EVENT_WAIT_FOR_OPPONENT:  ( self._view_instance.prompt_wait_page,   dict( {}, **params ) ),
            IH.GameEventType.GAME_EVENT_GAME_END:           ( self._view_instance.draw_game_over_page,dict( {}, **params ) ),
            IH.GameEventType.GAME_EVENT_AI_SELECTION: (self._view_instance.prompt_ai_selection, dict({}, **params)),
            IH.GameEventType.GAME_EVENT_AI_DIFFICULTY: (self._view_instance.prompt_ai_difficulty, dict({}, **params)),
            }
        
        # Obtain the function and the parameters for the function from the
        # map
        function_pointer_tup = message_to_view_event_map[ event ]
        function_pointer = function_pointer_tup[ TRIGGER_TO_FUNCTION_FUNC_IDX ]
        function_params = function_pointer_tup[ TRIGGER_TO_FUNCTION_PARAM_IDX ]
        
        # Call the view function
        return_vals : dict = function_pointer( function_params )

        # Return the view parameters back to the calling function
        return return_vals