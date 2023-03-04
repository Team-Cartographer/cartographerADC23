import csv
import tkinter as tk
from tkinter import messagebox
import os
import numpy as np
from numpy import cos, sin, sqrt, arccos, arcsin, rad2deg, deg2rad
from math import pi
import FolderCreator as fc
from ast import literal_eval


def file2list(path):
    with open(path) as csv_file:
        new_list = list(csv.reader(csv_file, delimiter=','))
        csv_file.close()

    return new_list


def find_file(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)


# Since FolderCreator is used across each file, these helper methods allow
# creating an error/info/warning popUp in each file.
def show_error(err_type, msg):
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror(err_type, msg)


def show_info(title, msg):
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo(title, msg)


def show_warning(title, msg):
    root = tk.Tk()
    root.withdraw()
    messagebox.showwarning(title, msg)

def calc_azimuth_and_elevation(x, y, z, latitudes, longitudes, heights, slopes):
    # Azimuth Angle and Elevation Calculation for Display.py
    latE, longE = 29.5593, 95.0900  # Latitude and Longitude of Johnson Space Center.
    latM, longM = float(latitudes[int(x) + 620][int(abs(z - 620))]), float(longitudes[int(x) + 620][int(abs(z - 620))])

    rad_earth = 6378000
    xE = rad_earth * cos(latE) * cos(longE)
    yE = rad_earth * cos(latE) * sin(longE)
    zE = rad_earth * sin(latE)

    xM = latM * cos(float(longM) * pi / 180)
    yM = latM * sin(float(longM) * pi / 180)
    zM = float(heights[int(x) + 620][int(abs(z - 620))])

    resultant_vector = [xE - xM, yE - yM, zE - zM]

    range = sqrt(resultant_vector[0] ** 2 + resultant_vector[1] ** 2 + resultant_vector[2] ** 2)

    rz = resultant_vector[0] * cos(latM) * cos(longM) + resultant_vector[1] * cos(latM) * cos(longM) + resultant_vector[
        2] * sin(latM)

    c1 = sin(longE - longM) * cos(latE)
    c2 = (cos(latM) * sin(latE)) - (sin(latM) * cos(latE) * cos(longE - longM))

    # Elevation Value
    elev = np.arcsin(rz / range)

    # Azimuth Angle Value
    azimuth = np.arctan2(c1, c2)

    return azimuth, elev


def latitude_from_rect(x: float, y: float) -> float:
    my_list = file2list(fc.data_path + "/AStarRawData.csv")
    height = literal_eval(my_list[y][x])[2]
    lat = rad2deg(arcsin(height/((1737.4 * 1000) + height)))
    return lat


def longitude_from_rect(x: float, y: float) -> float:
    my_list = file2list(fc.data_path + "/AStarRawData.csv")
    height = literal_eval(my_list[y][x])[2]
    lat = latitude_from_rect(x, y)
    long = rad2deg(arccos((x + round(int(fc.get_size_constant())/2))/(((1737.4 * 1000) + height)*cos)(deg2rad(lat))))
    return long

# TODO check this equation. I don't think it's right so far
def height_from_rect(x: float, y: float) -> float:
    my_list = file2list(fc.data_path + "/AStarRawData.csv")
    height = literal_eval(my_list[y][x])[2]
    height -= fc.get_min_z()




def slope_from_rect(x: float, y: float) -> float:
    my_list = file2list(fc.data_path + "/AStarRawData.csv")
    return literal_eval(my_list[y][x])[3]
