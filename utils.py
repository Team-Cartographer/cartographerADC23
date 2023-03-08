import csv
import tkinter as tk
from tkinter import messagebox
import os
import numpy as np
from numpy import rad2deg, arccos, deg2rad, sqrt
from math import atan2, sin, cos, degrees, radians, asin, pi
from ast import literal_eval



def file2list(path):
    with open(path) as csv_file:
        new_list = list(csv.reader(csv_file, delimiter=','))
        csv_file.close()

    return new_list

try:
    astar_list = file2list(os.getcwd() + '/Data/AStarRawData.csv')
except FileNotFoundError:
    pass

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
    #lat, _, _ = (radius/(30366 + (1/9))) - 90, x, y
    lat = literal_eval(astar_list[x][y])[6]
    return lat

def longitude_from_rect(x: float, y: float, radius: float) -> float:
    #long, _ = rad2deg(arccos(x/radius)), y
    long = literal_eval(astar_list[x][y])[7]
    return long

def slope_from_rect(x: float, y: float) -> float:
    return literal_eval(astar_list[x][y])[3]

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
    #latA, longA = deg2rad(-89.52), deg2rad(-112.17) # Center of Moon Ref. Loc
    radA = 1737.4 * 1000 + 41.4
    latA, longA = deg2rad(-89.54), deg2rad(0) #test2
    longB = deg2rad(float(longitude))
    latB = deg2rad(float(latitude))
    radB = 1737.4 * 1000 + float(height)

    # Azimuth Calculation
    c1 = sin(longB-longA) * cos(latB)
    c2 = (cos(latA) * sin(latB)) - (sin(latA) * cos(latB) * cos(longB-longA))
    azi = atan2(c1, c2)

    # Elevation Calculation
    xA, xB = get_x_coord(latA, longA, radA), get_x_coord(latB, longB, radB)
    yA, yB = get_y_coord(latA, longA, radA), get_y_coord(latB, longB, radB)
    zA, zB = get_z_coord(latA, radA), get_z_coord(latB, radB)

    dists = [xB-xA, yB-yA, zB-zA]
    range = sqrt(dists[0]** 2 + dists[1]**2 + dists[2]**2)
    rz = dists[0] * cos(latA) * cos(longA) + dists[1] * cos(latA) * sin(longA) + dists[2] * sin(latA)

    elev = asin(rz/range)

    return rad2deg(azi), rad2deg(elev)


def get_elev(x, y, z, lat, long):
    vec = [x - 361000000, y, z + 42100000]
    dist = sqrt(vec[0] ** 2 + vec[1] ** 2 + vec[2] ** 2)
    rz = float(vec[0] * cos(radians(lat)) * cos(radians(long)) + vec[1] *
    cos(radians(lat)) * sin(radians(long)) + vec[2] * sin(radians(lat)))
    return degrees(asin(rz / dist))
