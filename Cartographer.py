import FileManager as fm
from PIL import Image
from utils import resize, get_specific_from_json
from tqdm import tqdm
import seaborn as sns
import matplotlib.pyplot as plt
from os import getcwd
from shutil import move
from time import time
import random


SIZE_CONSTANT = fm.get_size_constant()
Image.MAX_IMAGE_PIXELS = None


def sns_heatmap(arr, cmap, save):
    start = time()

    # cmap reference: https://matplotlib.org/stable/gallery/color/colormap_reference.html

    sns.heatmap(arr, square=True, cbar=False, xticklabels=False,
                yticklabels=False, cmap=cmap)
    plt.tight_layout()
    plt.savefig(save, dpi=2048, transparent=True, format='png', bbox_inches='tight', pad_inches=0)

    # Convert to RGBA for Ursina.
    print(f'{save} created in {round(time()-start, 2)}s')


heights = get_specific_from_json(8, fm.ASTAR_JSONPATH)
slopes = get_specific_from_json(3, fm.ASTAR_JSONPATH)


def create_surface_texture():
    texture = Image.new("RGBA", (SIZE_CONSTANT, SIZE_CONSTANT))
    for y in tqdm(range(len(slopes)), desc='Creating Surface Texture'):
        for x in range(len(slopes[y])):
            color = 255
            # color logic here
            for i in range(int(slopes[y][x])):
                color -= random.randint(2, 5)
            texture.putpixel((x, y), (color, color, color))
    texture.save(fm.TEXTURE_PATH)


# Creates RAW_Heightmap, Slopemap, and Heightkey
def draw_all():

    # Creates Heightmap for Ursina
    sns_heatmap(
        arr=heights,
        cmap="gist_gray",
        save=fm.RAW_HEIGHTMAP_PATH
    )

    # Creates Heightkey
    # TODO Add Reduced Opacity Feature to Original Texture for this
    sns_heatmap(
        arr=heights,
        cmap='viridis',
        save=fm.SURFACE_HEIGHTKEY_PATH
    )

    # Creates Slopemap
    sns_heatmap(
        arr=slopes,
        cmap='inferno',
        save=fm.SLOPEMAP_PATH
    )

    # Creates Surface Texture
    create_surface_texture()


def draw_path(path, image, color):
    for i in tqdm(range(len(path)), desc="Drawing A* Path"):
        image.putpixel(path[0], path[1], color)
        print(f"\rCreating Path Image. {round(i / len(path), 4)}% complete", end="")
    return image


if __name__ == "__main__":

    start = time()

    # Create the essential images.
    draw_all()

    # Image Scaling for Faster Ursina Runs, as well as proper dimensions.
    proper_heightmap = resize(
        image_path=fm.RAW_HEIGHTMAP_PATH,
        new_name='processed_heightmap',
        scale=128,
        transpose=True
    )
    move(fm.images_path + fm.PROCESSED_HEIGHTMAP_PATH, getcwd() + '/processed_heightmap.png')

    proper_surface_texture = resize(
        image_path=fm.TEXTURE_PATH,
        new_name='moon_surface_texture',
        scale=SIZE_CONSTANT,
        transpose=True
    )

    flipped_slopemap = resize(
        image_path='Data/Images/slopemap.png',
        new_name='slopemap',
        scale=SIZE_CONSTANT,
        transpose=True
    )

    flipped_heightmap = resize(
        image_path='Data/Images/heightkey_surface.png',
        new_name='heightkey_surface',
        scale=SIZE_CONSTANT,
        transpose=True
    )

    minimap = resize(
        image_path='Data/Images/moon_surface_texture.png',
        new_name='minimap',
        scale=128
    )

    interface_slopemap = resize(
        image_path='Data/Images/slopemap.png',
        new_name='interface_slopemap',
        scale=500
    )

    interface_texture = resize(
        image_path='Data/Images/moon_surface_texture.png',
        new_name='interface_texture',
        scale=500
    )

    interface_heightkey = resize(
        image_path='Data/Images/heightkey_surface.png',
        new_name='interface_heightkey',
        scale=500
    )

    print(f'Cartographer ran in {round(time()-start, 2)}s')



