import csv
import tkinter as tk
from tkinter import messagebox
import os
import numpy as np
from numpy import cos, sin, sqrt, rad2deg, arccos, deg2rad
from math import pi
from ast import literal_eval


def file2list(path):
    with open(path) as csv_file:
        new_list = list(csv.reader(csv_file, delimiter=','))
        csv_file.close()

    return new_list

astar_list = file2list(os.getcwd() + '/Data/AStarRawData.csv')

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

# Display Calculations (Helper Functions for Math)
def get_radius(x: float, y: float) -> float:
    return sqrt((x**2) + (y**2))

def latitude_from_rect(x: float, y: float, radius: float) -> float:
    lat, _, _ = (radius/(30366 + (1/9))) - 90, x, y
    return lat

def longitude_from_rect(x: float, y: float, radius: float) -> float:
    long, _ = rad2deg(arccos(x/radius)), y
    return long

def slope_from_rect(x: float, y: float) -> float:
    return literal_eval(astar_list[y][x])[3] #TODO swap y/x and x/y?

def height_from_rect(x: float, y: float) -> float:
    height = float(os.getenv("MAX_Z")) - literal_eval(astar_list[x][y])[2]
    return height

def get_x_coord(lat, long, rad):  # takes in degrees latitude and longitude
    return float(rad) * cos(deg2rad(float(lat))) * cos(deg2rad(float(long)))

def get_y_coord(lat, long, rad):
    return float(rad) * cos(deg2rad(float(lat))) * sin(deg2rad(float(long)))

def get_z_coord(lat, rad):
    return float(rad) * sin(deg2rad(float(lat)))



def calc_azimuth_and_elevation(latitude, longitude, height):
    # Azimuth Angle and Elevation Calculation for Display.py
    lat_e, long_e = 29.5593, 95.0900  # Latitude and Longitude of Johnson Space Center.
    lat_m, long_m = float(latitude), float(longitude)

    rad_earth = 6378000
    x_e = rad_earth * cos(lat_e) * cos(long_e)
    y_e = rad_earth * cos(lat_e) * sin(long_e)
    z_e = rad_earth * sin(lat_e)

    x_m = lat_m * cos(long_m * pi / 180)
    y_m = lat_m * sin(long_m * pi / 180)
    z_m = float(height)

    resultant_vector = [x_e - x_m, y_e - y_m, z_e - z_m]

    range_ = sqrt(resultant_vector[0] ** 2 + resultant_vector[1] ** 2 + resultant_vector[2] ** 2)

    rz = resultant_vector[0] * cos(lat_e) * cos(long_e) + resultant_vector[1] * cos(lat_e) * cos(long_e) + resultant_vector[2] * sin(lat_e)

    c1 = sin(long_e - long_m) * cos(lat_e)
    c2 = (cos(lat_m) * sin(lat_e)) - (sin(lat_m) * cos(lat_e) * cos(long_e - long_m))

    # Elevation Value
    elev = np.arcsin(rz / range_)

    # Azimuth Angle Value
    azimuth = np.arctan2(c1, c2)

    return azimuth, elev

