import random
from interfaces import interface_headers as IH
import game_model as GM

class AI:
    def __init__(self,  difficulty: str, num_ships: int, player_type: IH.PlayerTypeEnum):
        """
        Initialize the AI with the specified difficulty level.
        """
        self.difficulty = difficulty
        self.num_ships = num_ships
        self.possible_targets = []
        self.ai_type = IH.PlayerTypeEnum.PLAYER_TYPE_HOST if player_type == IH.PlayerTypeEnum.PLAYER_TYPE_JOIN else IH.PlayerTypeEnum.PLAYER_TYPE_JOIN

    def place_ships(self, model: GM.GameModel, player_type: IH.PlayerTypeEnum):
        ships_placed = 0

        for ship_length in range(1,self.num_ships + 1):
            # Randomly determine ship length (you can modify this logic to have fixed-length ships)

            # Randomly choose direction: 0 for horizontal, 1 for vertical
            direction = random.choice([0, 1])

            if direction == 0:  # Horizontal placement
                row = random.randint(0, IH.NUMBER_OF_ROWS - 1)
                col = random.randint(0, IH.NUMBER_OF_COLS - ship_length)  # Ensure ship fits horizontally
            else:  # Vertical placement
                row = random.randint(0, IH.NUMBER_OF_ROWS - ship_length)
                col = random.randint(0, IH.NUMBER_OF_COLS - 1)  # Ensure ship fits vertically

            # Check if the space is free to place the ship
            can_place = True
            start_coordinate = ( row, col )
            direction = "H" if direction == 0 else "V"
            boat_coords = IH.boat_coords(start_coordinate, direction, ship_length)
            # If we find that at least one of the coordinates
            # is not a valid coordinate, we will trigger the error
            # state in the presenter
            for coord in boat_coords:
                if not model.is_valid_coord( self.ai_type, coord, IH.GameEventType.GAME_EVENT_PLACE_SHIPS ):
                    can_place = False
                    break

            # Place the ship if it's a valid placement
            if can_place:
                for coord in boat_coords:
                    new_state = { IH.GAME_COORD_TYPE_ID_INDEX : ship_length, IH.GAME_COORD_TYPE_STATE_INDEX: IH.CoordStateType.COORD_STATE_BASE }
                model.update_coord( self.ai_type, coord, new_state )
                ships_placed += 1
            # Implement ship placement logic here

    def make_attack(self, model: GM.GameModel, player_type: IH.PlayerTypeEnum):
        """
        Make an attack based on the difficulty level.
        """
        if self.difficulty == "Easy":
            return self._easy_attack(model, player_type)
        elif self.difficulty == "Medium":
            return self._medium_attack(model, player_type)
        elif self.difficulty == "Hard":
            return self._hard_attack(model, player_type)

    def _easy_attack(self, model: GM.GameModel, player_type: IH.PlayerTypeEnum):
        """
        Easy difficulty: Fire randomly every turn.
        """
        while True:
            row = random.randint(0, IH.NUMBER_OF_ROWS - 1)
            col = random.randint(0, IH.NUMBER_OF_COLS - 1)
            if model.is_valid_coord(player_type, (row, col), IH.GameEventType.GAME_EVENT_MAKE_ATTACK):
                return (row, col)

    def _medium_attack(self, model: GM.GameModel, player_type: IH.PlayerTypeEnum):
        """
        Medium difficulty: Fire randomly until it hits a ship, then fire in orthogonally adjacent spaces.
        """
        if self.possible_targets:
            coords = self.possible_targets.pop(0)
        else:
            coords = self._easy_attack(model, player_type)
        # If there is a ship at the attack coordinates, and it is not hit already,
        # add all adjacent coordinates to the possible targets
        if model.is_valid_coord(player_type, coords, IH.GameEventType.GAME_EVENT_MAKE_ATTACK):
            cell = model.get_coord(player_type, coords)
            if cell[IH.GAME_COORD_TYPE_ID_INDEX] > IH.BASE_CELL and cell[IH.GAME_COORD_TYPE_STATE_INDEX] != IH.CoordStateType.COORD_STATE_HIT:
                cell[IH.GAME_COORD_TYPE_STATE_INDEX] = IH.CoordStateType.COORD_STATE_HIT
                self.possible_targets.extend(self._get_adjacent_coords(coords))
        return coords

    def _hard_attack(self, model: GM.GameModel, player_type: IH.PlayerTypeEnum):
        """
        Hard difficulty: Knows where all ships are and lands a hit every turn.
        """
        for row in range(IH.NUMBER_OF_ROWS):
            for col in range(IH.NUMBER_OF_COLS):
                if model.get_coord(player_type, (row, col))[IH.GAME_COORD_TYPE_ID_INDEX] > IH.BASE_CELL and model.is_valid_coord(player_type, (row, col), IH.GameEventType.GAME_EVENT_MAKE_ATTACK):
                    return (row, col)

    def _get_adjacent_coords(self, coord):
        """
        Get orthogonally adjacent coordinates.
        """
        row, col = coord
        adjacent_coords = []
        if row > 0:
            adjacent_coords.append((row - 1, col))
        if row < IH.NUMBER_OF_ROWS - 1:
            adjacent_coords.append((row + 1, col))
        if col > 0:
            adjacent_coords.append((row, col - 1))
        if col < IH.NUMBER_OF_COLS - 1:
            adjacent_coords.append((row, col + 1))
        return adjacent_coords
