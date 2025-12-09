import pickle
import datetime
from typing import dataclass_transform
import pytz
import os
import shutil

import HexMap
import Hex
import pygame

MAX_DUPLICATE_FILE = 1000

# Default map paths
DEFAULT_MAP_PATH : str = "../maps/"
DEFAULT_SAVES_PATH : str = "../saves/"

# Map file names
DEFAULT_INFO_NAME : str = "info"
DEFAULT_INFO_SUFFIX : str = ".hmap"

DEFAULT_PREVIEW_NAME : str = "preview"
# For saving, always use the first suffix
DEFAULT_PREVIEW_SUFFIX : str = ".png"

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
    dir_path = str(new_path)
    dir_path = dir_path[:-1]
    # Find the next duplicate in limit
    save_path = str(dir_path)

    if not os.path.exists(save_path):
        os.makedirs(save_path)
        return save_path

    return None

def __check_valid_map(dir_path : str):
    # Check if info.hmap exists, nothing too fancy
    if os.path.exists(dir_path):
        if os.path.exists(dir_path + "/" + DEFAULT_INFO_NAME + DEFAULT_INFO_SUFFIX):
            return True
    return False

def __save_map_image(hex_map, renderer):
    map_surf = renderer.draw_entire_map_separate(hex_map)

    map_surf = pygame.transform.scale(map_surf, (256, 256))
    return map_surf

# Save current game
def save_game(config : dict, save_name = None):
    print(f"Saving game: {save_name}")
    # The name of the map
    map_name = str(config.get("Name"))

    # The save game can be different than the map name, but info.hmap will use map_name
    name_to_use = map_name

    if save_name != None:
        name_to_use = save_name

    new_path = DEFAULT_SAVES_PATH + name_to_use + "/"
    dir_path = __make_next_dir(new_path)

    if (dir_path == None):
        print("No directory file could be created")

        # File already found, rewrite it
        print(new_path)
        if os.path.exists(new_path):
            os.remove(new_path)
            dir_path = __make_next_dir(new_path)
        else:
            print("Something went wrong")
            # Something went wrong
            return

    dir_path += "/"

    map_hash = __get_hash(map_name)

    info_file = dir_path + DEFAULT_INFO_NAME + DEFAULT_INFO_SUFFIX

    # Clear the info file before writing new information
    if __check_valid_map(info_file):
        info_map = open(info_file, 'rb+')

        # If file exists, get the hash of the map
        temp_db = pickle.load(info_map)
        map_hash = temp_db['Hash']
        info_map.close()

    # Create info.hmap and pickle information into it
    with open(info_file, 'ab') as info_map:
        # The database to be pickled
        database : dict = {}

        # Put the hash to the database
        database['Hash'] = map_hash

        # Put the map to the database
        database['Name'] = map_name

        # Put the player array to the database
        database['Players'] = config.get("Players")

        # Put current player to the database
        database['CurrentPlayer'] = config.get("CurrentPlayer")

        # Put map array to the database
        database['Map'] = config.get("Map")

        print(f"database when saving: {database}")

        # Pickle the database to info_map
        pickle.dump(database, info_map)

# Load a game
def load_game(game_name : str):
    print(f"Loading game: {game_name}")

    dir_path = DEFAULT_SAVES_PATH + game_name + "/"
    if __check_valid_map(dir_path):
        with open(dir_path + DEFAULT_INFO_NAME + DEFAULT_INFO_SUFFIX, "rb") as info_file:
            return pickle.load(info_file)

# Save current map (map editor)
def save_map(config : dict, renderer):
    # The name of the map
    map_name = str(config.get("Name"))
    new_path = DEFAULT_MAP_PATH + map_name + "/"
    dir_path = __make_next_dir(new_path)

    if (dir_path == None):
        print("No directory file could be created")

        # File already found, rewrite it
        print(new_path)
        if os.path.exists(new_path):
            shutil.rmtree(new_path)
            dir_path = __make_next_dir(new_path)
        else:
            print("Something went wrong")
            # Something went wrong
            return

    map_hash = __get_hash(map_name)
    info_file_path = dir_path + "/" + DEFAULT_INFO_NAME + DEFAULT_INFO_SUFFIX

    # Check if file exists and read the existing hash
    if os.path.exists(info_file_path):
        try:
            with open(info_file_path, 'rb') as info_map:
                temp_db = pickle.load(info_map)
                map_hash = temp_db['Hash']

        except Exception as e:
            print(f"Error reading existing map: {e}")

    # Create/overwrite the file with new data
    with open(info_file_path, 'wb') as info_map:
        # The database to be pickled
        database = {}

        # Put the hash to the database
        database['Hash'] = map_hash

        # Put the map to the database
        database['Name'] = map_name

        # Put the player array to the database
        database['Players'] = config.get("Players")

        # Put current player to the database
        database['CurrentPlayer'] = config.get("CurrentPlayer")

        # Put map array to the database
        database['Map'] = config.get("Map")

        # Pickle the database to info_map
        pickle.dump(database, info_map)

    pygame.image.save(__save_map_image(database['Map'], renderer), dir_path + "/" + DEFAULT_PREVIEW_NAME + DEFAULT_PREVIEW_SUFFIX)

# Load a map (lobby and map editor)
def load_map(map_name : str):
    dir_path = DEFAULT_MAP_PATH + map_name + "/"
    if __check_valid_map(dir_path):
        with open(dir_path + DEFAULT_INFO_NAME + DEFAULT_INFO_SUFFIX, "rb") as info_file:
            return pickle.load(info_file)
    else:
        return None

