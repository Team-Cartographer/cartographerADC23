from concurrent.futures import ProcessPoolExecutor

from PIL import Image
from utils import resize
import seaborn as sb
import numpy as np
import matplotlib.pyplot as plt
from time import time


Image.MAX_IMAGE_PIXELS = None


# noinspection SpellCheckingInspection
def sb_heatmap(arr, cmap, path):
    start_time = time()

    # cmap reference: https://matplotlib.org/stable/gallery/color/colormap_reference.html

    sb.heatmap(arr, square=True, cbar=False, xticklabels=False,
               yticklabels=False, cmap=cmap)
    plt.tight_layout()
    plt.savefig(path, dpi=2048, transparent=True, format="png", bbox_inches="tight", pad_inches=0)

    # Convert to RGBA for Ursina.
    print(f"{path} created in {round(time() - start_time, 2)}s")

    return path


def create_surface_texture(save, slopes):
    print(f"creating surface texture")
    start = time()

    max_value_index = np.unravel_index(slopes.argmax(), slopes.shape)
    max_value = slopes[max_value_index[0]][max_value_index[1]]

    colors = np.full(slopes.shape, 255.0)
    for i in range(int(max_value)):
        random_array = np.random.uniform(low=2, high=5, size=slopes.shape)

        slopes -= 1
        non_zero_mask = slopes > 0
        colors = np.where(non_zero_mask, colors - random_array, colors)

    colors[colors < 0] = 0

    # Multiplying by 3 gives us (color, color, color) [Not exactly but it kind of represents the RGB values]
    image_array = np.stack([colors] * 3, axis=-1)
    texture = Image.fromarray(np.uint8(image_array), mode="RGB")

    print(f"{save.moon_surface_texture_image} created in {round(time() - start, 2)}s")
    texture.save(save.moon_surface_texture_image)


# noinspection SpellCheckingInspection
# Creates RAW_Heightmap, Slopemap, and Heightkey with Threading
def draw_maps(save):

    parsed_arr = np.load(save.data_file)
    heights = parsed_arr[:, :, 8]
    slopes = parsed_arr[:, :, 3]

    with ProcessPoolExecutor() as exc:

        raw_heightmap_future = exc.submit(sb_heatmap, heights, "gist_gray", save.raw_heightmap_image)
        heightkey_future = exc.submit(sb_heatmap, heights, "viridis", save.heightkey_surface_image)
        slopemap_future = exc.submit(sb_heatmap, slopes, "inferno", save.slopemap_image)
        texture_future = exc.submit(create_surface_texture, save, slopes)

        raw_heightmap = raw_heightmap_future.result()
        heightkey = heightkey_future.result()
        slopemap = slopemap_future.result()
        texture = texture_future.result()

        return raw_heightmap, heightkey, slopemap, slopemap, texture


# noinspection PyUnusedLocal
def create_images(save):
    print("creating all images")
    start = time()

    # Create the essential images.
    draw_maps(save)

    # Image Scaling for Faster Ursina Runs, as well as proper dimensions.
    proper_heightmap = resize(
        image_path=save.raw_heightmap_image,
        path=save.processed_heightmap,
        scale=128,
        transpose=True
    )

    proper_surface_texture = resize(
        image_path=save.moon_surface_texture_image,
        path=save.moon_surface_texture_image,
        scale=save.size,
        transpose=True
    )

    flipped_slopemap = resize(
        image_path=save.slopemap_image,
        path=save.slopemap_image,
        scale=save.size,
        transpose=True
    )

    flipped_heightmap = resize(
        image_path=save.heightkey_surface_image,
        path=save.heightkey_surface_image,
        scale=save.size,
        transpose=True
    )

    minimap = resize(
        image_path=save.moon_surface_texture_image,
        path=save.minimap_image,
        scale=128
    )

    interface_slopemap = resize(
        image_path=save.slopemap_image,
        path=save.interface_slopemap_image,
        scale=500
    )

    interface_texture = resize(
        image_path=save.moon_surface_texture_image,
        path=save.interface_texture_image,
        scale=500
    )

    interface_heightkey = resize(
        image_path=save.heightkey_surface_image,
        path=save.interface_heightkey_image,
        scale=500
    )

    print(f"cartographer created images in {round(time() - start, 2)}s")


if __name__ == "__main__":
    # create_images()
    pass
