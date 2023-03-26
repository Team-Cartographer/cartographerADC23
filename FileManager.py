"""
FileManager.py makes folders and directories for all files for the FPA Team NASA
App Development Challenge Application.#
"""

import os
from utils import show_info, file2list, load_json, push_to_json
import ui

# Define Pathing
parent_path: str = os.getcwd()
data_path: str = os.path.join(parent_path, 'Data')
images_path: str = os.path.join(data_path, 'Images')
app_files_path: str = os.path.join(parent_path, 'App Files')


# DEFINE CONSTANTS
INFO_JSONPATH = os.getcwd() + '/info.json'
ASTAR_JSONPATH = 'Data/AStarRawData.json'
TEXTURE_PATH = images_path + '/moon_surface_texture.png'
RAW_HEIGHTMAP_PATH = images_path + '/RAW_heightmap.png'
PROCESSED_HEIGHTMAP_PATH = '/processed_heightmap.png'
SLOPEMAP_PATH = images_path + '/slopemap.png'
SURFACE_HEIGHTKEY_PATH = images_path + '/heightkey_surface.png'

# Image Paths
ASTAR_PATH = images_path + "/AStar_Path.png"





# Sets up Json File.
if not os.path.exists(os.getcwd() + '/info.json'):

    LUNAR_RAD = 1737400.0

    # Get pathing from Path_Fetcher() #
    # TODO Fix issue where closing path_fetcher throws errors
    lat, long, ht, slope = ui.path_fetcher()

    data: dict = {
        "LATITUDE_PATH": lat,
        "LONGITUDE_PATH": long,
        "HEIGHT_PATH": ht,
        "SLOPE_PATH": slope,

        "SIZE_CONSTANT": len(file2list(lat)),
        "PLAYER_POSITION": None,
        "LUNAR_RAD": LUNAR_RAD,
        "MAX_Z": None,
        "MIN_Z": None,
        "MIN_Y": None,
        "MIN_X": None
    }

    push_to_json(INFO_JSONPATH, data)


# Data is a dictionary load that is standardized for all saves.
data = load_json(os.getcwd() + '/info.json')


# Getter Functions for '.json'
def get_latitude_file_path() -> str:
    return data["LATITUDE_PATH"].replace("\\", "/")


def get_longitude_file_path() -> str:
    return data["LONGITUDE_PATH"].replace("\\", "/")


def get_height_file_path() -> str:
    return data["HEIGHT_PATH"].replace("\\", "/")


def get_slope_file_path() -> str:
    return data["SLOPE_PATH"].replace("\\", "/")


def get_size_constant() -> int:
    return data["SIZE_CONSTANT"]


def get_max_z() -> int:
    return data["MAX_Z"]


def get_max_height() -> int:
    return data["MAX_HEIGHT"]


def get_min_height() -> int:
    return data["MIN_HEIGHT"]


def get_min_z() -> int:
    return data["MIN_Z"]


def get_min_x() -> int:
    return data["MIN_X"]


def get_min_y() -> int:
    return data["MIN_Y"]


def get_lunar_rad() -> float:
    return data["LUNAR_RAD"]


# Meant for future save files, unused currently.
def get_player_pos() -> tuple:
    return data["PLAYER_POSITION"]


# Creates directories and sets 'info.json' variables only if FileManager.py is running.
# Otherwise, only helper methods are accessible.
if __name__ == '__main__':
    # Save File proof of concept, disregard currently.
    # savetest = Save('SAVETEST')

    # json is automatically created and/or overwritten on every run of FileManager.
    if not os.path.exists(os.path.join(parent_path, 'Data')):
        os.mkdir(data_path)
        os.mkdir(app_files_path)
        os.mkdir(images_path)
    else:
        # If Directories exist, Notify User.
        show_info('ADC App Installation Update',
                  "Folder Already Exists on " + parent_path + '\nFiles have been updated.')
