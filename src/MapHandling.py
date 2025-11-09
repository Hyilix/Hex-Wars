import pickle
import datetime
import pytz
import os

import HexMap
import Hex

MAX_DUPLICATE_FILE = 1000

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

# A config dictionary will never include a map hash

# Set timezone
__tz = pytz.timezone('Europe/Bucharest')

# Simple hashing function for getting a map hash
def __get_hash(map_name : str):
    # Copy the map name
    hash_str = str(map_name)
    current_time = datetime.datetime.now(__tz)
    hash_str += str(current_time)
    return hash(hash_str)

# Make directory for saving a game/map
def __make_next_dir(new_path : str):
    # Find the next duplicate in limit
    for i in range(MAX_DUPLICATE_FILE):
        save_path = str(new_path)
        if i > 0:
            save_path += "(" + str(i) + ")"

        if not os.path.exists(save_path):
            os.makedirs(save_path)
            return save_path

    return None

# Save current game
def save_game(config : dict):
    new_path = DEFAULT_SAVES_PATH + str(config.get("name"))
    dir_path = __make_next_dir(new_path)

    if (dir_path == None):
        print("No directory file could be created")
        return

# Load a game
def load_game(game_name : str):
    pass

# Save current map (map editor)
def save_map(config : dict):
    pass

# Load a map (lobby and map editor)
def load_map(map_name : str):
    pass

