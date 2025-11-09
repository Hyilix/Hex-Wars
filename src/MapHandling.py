import pickle

import HexMap
import Hex

# Default map paths
DEFAULT_MAP_PATH : str = "../maps"
DEFAULT_GAME_SUFFIX : str = "/game"
DEFAULT_USER_SUFFIX : str = "/custom"
DEFAULT_SAVES_PATH : str = "../saves/"

# Map serialization format:

# 1. Map Hash (Some maps may have the same name, but they have to be unique in some regards)
# 2. Map Name (For saved games mostly, but good info nonetheless)
# 3. Player array
# 4. Current Player
# 5. Map array

# A map will contain the serialized file, and an image of the map, all in a directory

# Save current game
def save_game(config : dict):
    pass

# Load a game
def load_game(game_name : str):
    pass

# Save current map (map editor)
def save_map(config : dict):
    pass

# Load a map (lobby and map editor)
def load_map(map_name : str):
    pass

