# This program is used to create the heightmap and slope map from the data

import csv
import FolderCreator as fc

from PIL import Image

#Change from 1277 to 4000 for Regional Data File
SIZE_CONSTANT = 1277

rect_coord_path = fc.data_path + "/RectangularCoordinateData.csv"
rect_coord_path = rect_coord_path.replace("\\", "/")
with open(rect_coord_path, mode="r") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    full_list = list(csv_reader)


def calculate_color(height):
    color = ((height+2872)*255/4830)
    return int(color), int(color), int(color)

def calc_rgb_color(height):
    r,g,b = 0,0,0
    if (height+2872)/4830 <= 1/3:
        b = (height+2872)*255/4830
    elif (height+2872)/4830 <= 2/3:
        g = (height+2872)*255/4830
    else:
        r = (height+2872)*255/4830
    return (int(r), int(g), int(b))


def draw_points():
    for i in range(1, len(full_list)):
        color = calculate_color(float(full_list[i][2]))
        x_pos = (i-1) % SIZE_CONSTANT
        y_pos = (i-1) // SIZE_CONSTANT
        print(x_pos, y_pos)
        canvas.putpixel((int(x_pos), int(y_pos)), color)
        # note that there is a bit of data loss here.
        # Ideally, we'd make the final image have a size equal to the maximum span of the x and y data


def draw_colors():
    for i in range(1, len(full_list)):
        color = calc_rgb_color(float(full_list[i][2]))
        x_pos = (i-1) % SIZE_CONSTANT
        y_pos = (i-1)//SIZE_CONSTANT
        print(x_pos, y_pos)
        canvas.putpixel((int(x_pos), int(y_pos)), color)


def draw_slopes():
    for i in range(1, len(full_list)):
        color = (255, 0, 0)
        if float(full_list[i][3]) < 20:
            color = (255, 255, 0)
        if float(full_list[i][3]) < 8:
            color = (0, 255, 0)
        x_pos = (i-1) % SIZE_CONSTANT
        y_pos = (i-1)//SIZE_CONSTANT
        print(x_pos, y_pos)
        canvas.putpixel((int(x_pos), int(y_pos)), color)


def draw_path(path, image, color):
    for i in range(len(path)):
        image.putpixel(path[0], path[1], color)
    return image


if __name__=="__main__":
    canvas = Image.new('RGB', (SIZE_CONSTANT, SIZE_CONSTANT), 'blue')
    draw_points()
    canvas.save(fc.images_path + '/heightmap_test.jpg')
    draw_slopes()
    canvas.save(fc.images_path + '/slopemap_test.jpg')
    draw_colors()
    canvas.save(fc.images_path + '/color_heights_test.jpg')

