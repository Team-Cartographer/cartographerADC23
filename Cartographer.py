"""
This program takes a CSV file containing terrain data and generates a heightmap and a slope map.

The heightmap is a grayscale representation of the terrain's elevation, where lighter shades represent higher
elevation and darker shades represent lower elevation.

The slope map uses a color scheme to represent the steepness of the terrain, with green indicating gentle slopes,
yellow indicating moderate slopes, and red indicating steep slopes.

The program also downscales the final image to improve performance when used with the Ursina game engine.
"""

import FolderCreator as fc
from ast import literal_eval
from PIL import Image
from utils import file2list

astar_data_path = fc.data_path + "/AStarRawData.csv"
full_list = file2list(astar_data_path)

max_z = fc.get_max_z()
SIZE_CONSTANT = fc.get_size_constant()


def calculate_color(height):
    color = 255 - (height * 255 / max_z)
    return int(color), int(color), int(color)


def calc_rgb_color(height):
    r, g, b = 0, 0, 0
    if height / max_z <= 1/3:
        b = height * 255 / max_z
    elif height / max_z <= 2/3:
        g = height * 255 / max_z
    else:
        r = height * 255 / max_z
    return int(r), int(g), int(b)


def draw_points():
    for i in range(len(full_list)):
        for j in range(len(full_list[i])):
            color = calculate_color(float(literal_eval(full_list[j][i])[2]))
            x_pos = j
            y_pos = i
            canvas.putpixel((int(x_pos), int(y_pos)), color)
            # note that there is a bit of data loss here.
            # Ideally, we'd make the final image have a size equal to the maximum span of the x and y data
            print(f"\rCreating Heightmap. {round(i / len(full_list), 4)}% complete", end="")



def draw_colors():
    for i in range(len(full_list)):
        for j in range(len(full_list[i])):
            color = calc_rgb_color(float(literal_eval(full_list[j][i])[2]))
            x_pos = j
            y_pos = i
            # print(x_pos, y_pos)
            canvas.putpixel((int(x_pos), int(y_pos)), color)
            print(f"\rCreating Heightkey. {round(i / len(full_list), 4)}% complete", end="")


def draw_slopes():
    for i in range(len(full_list)):
        for j in range(len(full_list[i])):
            color = (255, 0, 0)
            if float(literal_eval(full_list[j][i])[3]) < 20:
                color = (255, 255, 0)
            if float(literal_eval(full_list[j][i])[3]) < 8:
                color = (0, 255, 0)
            x_pos = j
            y_pos = i
            # print(x_pos, y_pos)
            canvas.putpixel((int(x_pos), int(y_pos)), color)
            print(f"\rCreating Slopemap. {round(i / len(full_list), 4)}% complete", end="")



def draw_path(path, image, color):
    for i in range(len(path)):
        image.putpixel(path[0], path[1], color)
        print(f"\rCreating Path Image. {round(i / len(path), 4)}% complete", end="")
    return image


if __name__ == "__main__":

    canvas = Image.new('RGBA', (SIZE_CONSTANT, SIZE_CONSTANT), 'blue')
    draw_points()
    canvas.save(fc.images_path + '/RAW_heightmap.png')  # must save here for a proper read from Ursina
    print("\nCreated RAW_heightmap.png")
    draw_slopes()
    canvas.save(fc.images_path + '/slopemap.png')
    print("\nCreated slopemap.png")
    draw_colors()
    canvas.save(fc.images_path + '/heightkey_surface.png')
    print("\nCreated heightkey_surface.png")

    # Image Scaling for Faster Ursina Runs
    upscaled = Image.open(fc.images_path + '/RAW_heightmap.png')
    downscaled = upscaled.resize((81, 81)) # 1/16th Scale
    downscaled.save(fc.parent_path + '/processed_heightmap.png')
    print("Created processed_heightmap.png")

    map = Image.open('moon_surface_texture.png')
    minimap = map.resize((127, 127)) # 1/100th Scale
    minimap.save(fc.images_path + '/minimap.png')
    print("Created minimap.png")

    img = Image.open('moon_surface_texture.png')
    img = img.resize((1277, 1277))
    img.save(fc.images_path + '/AStar_Texture.png')


    print("Cartographer Success")
