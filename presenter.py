# Presenter for BattleShip game from MVP Architecture Design Pattern
import interface/interface_headers as ihdrs

# Game takes place over three stages: (1) Connect to other computer on
# network; (2) Perform initial game setup; (3) Play the actual game

# Presenter class for BattleShip game
# Manages interactions between model (game state and mechanisms) and
# view (inputs from user and displays) with network
class BattleShipPresenter:
    def __init__(self, view, model, network):
        self.view = view
        self.model = model
        self.network = network

    # Called when the game is started
    def init_game(self):
        self.connect_computers()
        self.setup_game()
        self.play_game()

    # Stage 1: Connect computers
    def connect_computers():
        # Find player type based on host or join
        # TODO: Communicate with view to see if host or join
        self.playerType = PlayerTypeEnum.PLAYER_TYPE_HOST

        return

    # Stage 2: Setup the game
    def setup_game():
        # Find desired number of ships

        # Place ships
        pass

    # Stage 3: Play the game
    def play_game():
        # Play goes between each player taking turns guessing,
        # checking, and resolving a move

        # Current player turn. 0 for player one (HOST) and 1 for
        # player 2 (JOIN)
        player_turn = 0

        while True:
            # Check which player turn it is
            # Your turn
            if player_turn == self.playerType.value:
                # Guess a square

                # Ask result of guess

                # Update model from guess

                pass
            # Not your turn
            else:
                # Wait for a guess

                # Check guess

                # Update model from guess

                pass

            # Swap player turn
            player_turn = 0 if player_turn == 1 else 1

        return
