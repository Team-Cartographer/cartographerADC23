# This program is used to create the heightmap and slope map from the data

import csv
import pygame
from pygame import gfxdraw
import os

from PIL import Image, ImageDraw

#Change from 1277 to 4000 for Regional Data File
SIZE_CONSTANT = 1277

rect_coord_path = "C:/Users/ashwa/Desktop/ADCLander/ProcessedData/ProcessedCoordinateData.csv"
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


def draw_points(isPygame):
    for i in range(1, len(full_list)):
        color = calculate_color(float(full_list[i][2]))
        x_pos = (i-1) % SIZE_CONSTANT
        y_pos = (i-1) // SIZE_CONSTANT
        print(x_pos, y_pos)
        if isPygame:
            gfxdraw.pixel(screen, int(x_pos), int(y_pos), color)
        else:
            canvas.putpixel((int(x_pos), int(y_pos)), color)
        # note that there is a bit of data loss here.
        # Ideally, we'd make the final image have a size equal to the maximum span of the x and y data


def draw_colors(isPygame):
    for i in range(1, len(full_list)):
        color = calc_rgb_color(float(full_list[i][2]))
        x_pos = (i-1) % SIZE_CONSTANT
        y_pos = (i-1)//SIZE_CONSTANT
        print(x_pos, y_pos)
        if isPygame:
            gfxdraw.pixel(screen, int(x_pos), int(y_pos), color)
        else:
            canvas.putpixel((int(x_pos), int(y_pos)), color)


def draw_slopes(isPygame):
    for i in range(1, len(full_list)):
        color = (255, 0, 0)
        if float(full_list[i][3]) < 20:
            color = (255, 255, 0)
        if float(full_list[i][3]) < 8:
            color = (0, 255, 0)
        x_pos = (i-1) % SIZE_CONSTANT
        y_pos = (i-1)//SIZE_CONSTANT
        print(x_pos, y_pos)
        if isPygame:
            gfxdraw.pixel(screen, int(x_pos), int(y_pos), color)
        else:
            canvas.putpixel((int(x_pos), int(y_pos)), color)

###

canvas = Image.new('RGB', (SIZE_CONSTANT, SIZE_CONSTANT), 'blue')
draw_points(False)
canvas.save('C:/Users/ashwa/Desktop/heightmap_test.jpg')
draw_slopes(False)
canvas.save('C:/Users/ashwa/Desktop/slopemap_test.jpg')
draw_colors(False)
canvas.save('C:/Users/ashwa/Desktop/color_heights_test.jpg')

###

print("initiating pygame")
pygame.init()
screen = pygame.display.set_mode((SIZE_CONSTANT, SIZE_CONSTANT))

done = True
clock = pygame.time.Clock()
while not done:
    recent_key = "h"

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_h:
                recent_key = "h"
            elif event.key == pygame.K_s:
                recent_key = "s"
            elif event.key == pygame.K_c:
                recent_key = "c"

        if recent_key == "h":
            draw_points(True)
        elif recent_key == "c":
            draw_colors(True)
        else:
            draw_slopes(True)


    pygame.display.flip()
    clock.tick(60)
