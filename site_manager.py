import ui
import os
from utils import file2list, push_to_json, load_json, are_you_sure
from data_processor import process_data
from cartographer import create_images
from a_star import run_astar
from subprocess import run
import sys
from time import time


class Save:
    # If "load=False", then the declared folder_path when making the save is just a path to /Saves/
    def __init__(self, folder_path: str, load: bool = False):
        if load:
            self.folder_path = folder_path
            self.site_name = os.path.basename(folder_path).split('_')[-1].strip()  # Parse name from <folder_path>
            print(f'loading {self.site_name} visualization')
        else:
            site_name = ui.new_site_name()
            self.folder_path = folder_path + "/Save_" + site_name
            self.site_name = site_name
            self.size = None

        self.data_folder = self.folder_path + "/Data"
        self.images_folder = self.folder_path + "/Images"
        self.astar_path_image = self.images_folder + "/AStar_Path.png"
        self.heightkey_surface_image = self.images_folder + "/heightkey_surface.png"
        self.interface_heightkey_image = self.images_folder + "/interface_heightkey_image.png"
        self.interface_slopemap_image = self.images_folder + "/interface_slopemap.png"
        self.interface_texture_image = self.images_folder + "/interface_texture.png"
        self.minimap_image = self.images_folder + "/minimap.png"
        self.moon_surface_texture_image = self.images_folder + "/moon_surface_texture.png"
        self.raw_heightmap_image = self.images_folder + "/RAW_heightmap.png"
        self.slopemap_image = self.images_folder + "/slopemap.png"
        self.processed_heightmap = self.images_folder + "/processed_heightmap.png"
        self.info_json = self.data_folder + '/info.json'
        self.astar_json = self.data_folder + "/AStarRawData.json"
        self.latitude_path, self.longitude_path, self.height_path, self.slope_path = None, None, None, None

        if load:
            self.size = load_json(self.info_json)["SIZE_CONSTANT"]
        else:
            self.set_up()

    def set_up(self):
        print(f'starting {self.site_name} first time setup...')

        start = time()

        os.makedirs(self.folder_path, exist_ok=True)
        os.makedirs(self.data_folder, exist_ok=True)
        os.makedirs(self.images_folder, exist_ok=True)

        # Paths to each data file
        lat, long, ht, slope = ui.path_fetcher()
        data: dict = {
                "LATITUDE_PATH": lat,
                "LONGITUDE_PATH": long,
                "HEIGHT_PATH": ht,
                "SLOPE_PATH": slope,

                "SIZE_CONSTANT": len(file2list(lat)),
            }
        push_to_json(self.info_json, data)

        self.latitude_path, self.longitude_path, self.height_path, self.slope_path = lat, long, ht, slope
        self.size = data["SIZE_CONSTANT"]

        process_data(self)
        create_images(self)
        run_astar(self)

        print(f'{self.site_name} setup complete in {round(time() - start, 2)}s')

    def to_string(self):
        return f"{self.folder_path}"


def check_save():
    save_folder = os.getcwd() + "/Saves"

    if not os.path.exists(save_folder):
        os.mkdir(save_folder)

    path = ui.on_start()

    if path:
        save_ = Save(folder_path=path, load=True)
    else:
        save_ = Save(folder_path=save_folder, load=False)

    if save_ is None:
        exit(1)
    else:
        return save_


def run_smpy():
    save = check_save()
    # Since Display is a script, run it via Subprocess.
    result = run([sys.executable, 'display.py'] + [save.folder_path, str(True)], text=True, capture_output=True)
    print(f'ended {save.site_name} visualization.')
    if result.returncode == 2:
        return True
    else:
        return False


if __name__ == '__main__':

    # rerun the file until the user wants to quit
    while True:
        reset = run_smpy()
        if reset:
            continue
        else:
            break
