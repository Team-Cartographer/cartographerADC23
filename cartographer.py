from concurrent.futures import ProcessPoolExecutor

from PIL import Image
from utils import resize, get_specific_from_json
import seaborn as sns
import matplotlib.pyplot as plt
from time import time
import random
from file_manager import FileManager
from constants import CWD
from shutil import move

fm = FileManager()

heights = get_specific_from_json(8, fm.astar_json_path)
slopes = get_specific_from_json(3, fm.astar_json_path)

Image.MAX_IMAGE_PIXELS = None

def sns_heatmap(arr, cmap, save):
    start_time = time()

    # cmap reference: https://matplotlib.org/stable/gallery/color/colormap_reference.html

    sns.heatmap(arr, square=True, cbar=False, xticklabels=False,
                yticklabels=False, cmap=cmap)
    plt.tight_layout()
    plt.savefig(save, dpi=2048, transparent=True, format='png', bbox_inches='tight', pad_inches=0)

    # Convert to RGBA for Ursina.
    print(f'{save} created in {round(time()-start_time, 2)}s')

    return save


def create_surface_texture():
    print("Surface Texture Generation In Progress")
    texture = Image.new("RGBA", (fm.size, fm.size))
    for y in range(len(slopes)):
        for x in range(len(slopes[y])):
            color = 255
            # color logic here
            for i in range(int(slopes[y][x])):
                color -= random.randint(2, 5)
                if color < 0:
                    color = 0
            texture.putpixel((x, y), (color, color, color))
    texture.save(fm.texture_path)


# Creates RAW_Heightmap, Slopemap, and Heightkey with Threading
def draw_all():
    with ProcessPoolExecutor() as exc:
        RAW_Heightmap_future = exc.submit(sns_heatmap, heights, "gist_gray", fm.raw_height_map_path)
        Heightkey_future = exc.submit(sns_heatmap, heights, "viridis", fm.surface_heightkey_path)
        Slopemap_future = exc.submit(sns_heatmap, slopes, "inferno", fm.slopemap_path)
        Texture_future = exc.submit(create_surface_texture)

        RAW_Heightmap = RAW_Heightmap_future.result()
        Heightkey = Heightkey_future.result()
        Slopemap = Slopemap_future.result()
        Texture = Texture_future.result()

        return RAW_Heightmap, Heightkey, Slopemap, Slopemap, Texture


if __name__ == "__main__":
    start = time()

    # Create the essential images.
    draw_all()


    # Image Scaling for Faster Ursina Runs, as well as proper dimensions.
    proper_heightmap = resize(
        image_path=fm.raw_height_map_path,
        new_name='processed_heightmap',
        scale=128,
        transpose=True
    )
    move(fm.processed_heightmap_path, CWD + '/processed_heightmap.png')

    proper_surface_texture = resize(
        image_path=fm.texture_path,
        new_name='moon_surface_texture',
        scale=fm.size,
        transpose=True
    )

    flipped_slopemap = resize(
        image_path=fm.slopemap_path,
        new_name='slopemap',
        scale=fm.size,
        transpose=True
    )

    flipped_heightmap = resize(
        image_path=fm.surface_heightkey_path,
        new_name='heightkey_surface',
        scale=fm.size,
        transpose=True
    )

    minimap = resize(
        image_path=fm.texture_path,
        new_name='minimap',
        scale=128
    )

    interface_slopemap = resize(
        image_path=fm.slopemap_path,
        new_name='interface_slopemap',
        scale=500
    )

    interface_texture = resize(
        image_path=fm.texture_path,
        new_name='interface_texture',
        scale=500
    )

    interface_heightkey = resize(
        image_path=fm.surface_heightkey_path,
        new_name='interface_heightkey',
        scale=500
    )

    print(f'Cartographer created images in {round(time()-start, 2)}s')



