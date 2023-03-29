import os
from utils import file2list, load_json, push_to_json, timeit
import ui
from constants import INFO_JSONPATH, ASTAR_JSONPATH, TEXTURE_PATH, RAW_HEIGHTMAP_PATH, PROCESSED_HEIGHTMAP_PATH, \
    SLOPEMAP_PATH, SURFACE_HEIGHTKEY_PATH, ASTAR_PATH


def combine2paths(path1, path2):
    return path1 + path2


def singleton(cls):
    instances = {}

    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return get_instance


def initialize_file_manager():
    fm = FileManager()

    os.makedirs(fm.data_path, exist_ok=True)
    os.makedirs(fm.app_files_path, exist_ok=True)
    os.makedirs(fm.images_path, exist_ok=True)


@singleton
class FileManager:

    @timeit
    def __init__(self):
        self.parent_path: str = os.getcwd()
        self.data_path: str = os.path.join(self.parent_path, 'Data')
        self.images_path: str = os.path.join(self.data_path, 'Images')
        self.app_files_path: str = os.path.join(self.parent_path, 'App Files')

        self.info_json_path = combine2paths(self.parent_path, INFO_JSONPATH)
        self.astar_json_path = combine2paths(self.parent_path, ASTAR_JSONPATH)

        # Image Paths
        self.texture_path = combine2paths(self.images_path, TEXTURE_PATH)
        self.raw_height_map_path = combine2paths(self.images_path, RAW_HEIGHTMAP_PATH)
        self.processed_heightmap_path = combine2paths(self.images_path, PROCESSED_HEIGHTMAP_PATH)
        self.slopemap_path = combine2paths(self.images_path, SLOPEMAP_PATH)
        self.surface_heightkey_path = combine2paths(self.images_path, SURFACE_HEIGHTKEY_PATH)
        self.astar_path = combine2paths(self.images_path, ASTAR_PATH)

        if not os.path.exists(self.info_json_path):
            lat, long, ht, slope = ui.path_fetcher()

            data: dict = {
                "LATITUDE_PATH": lat,
                "LONGITUDE_PATH": long,
                "HEIGHT_PATH": ht,
                "SLOPE_PATH": slope,

                "SIZE_CONSTANT": len(file2list(lat)),
            }

            push_to_json(self.info_json_path, data)

        data = load_json(self.info_json_path)

        self.latitude_path = data["LATITUDE_PATH"].replace("\\", "/")
        self.longitude_path = data["LONGITUDE_PATH"].replace("\\", "/")
        self.height_path = data["HEIGHT_PATH"].replace("\\", "/")
        self.slope_path = data["SLOPE_PATH"].replace("\\", "/")

        self.size = data["SIZE_CONSTANT"]


if __name__ == "__main__":
    initialize_file_manager()