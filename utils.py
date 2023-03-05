import csv
import tkinter as tk
from tkinter import messagebox
import os
import numpy as np
from numpy import cos, sin, sqrt
from math import pi


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


def calc_azimuth_and_elevation(latitude, longitude, height):
    # Azimuth Angle and Elevation Calculation for Display.py
    lat_e, long_e = 29.5593, 95.0900  # Latitude and Longitude of Johnson Space Center.
    lat_m, long_m = latitude, longitude

    rad_earth = 6378000
    x_e = rad_earth * cos(lat_e) * cos(long_e)
    y_e = rad_earth * cos(lat_e) * sin(long_e)
    z_e = rad_earth * sin(lat_e)

    x_m = lat_m * cos(float(long_m) * pi / 180)
    y_m = lat_m * sin(float(long_m) * pi / 180)
    z_m = height

    resultant_vector = [x_e - x_m, y_e - y_m, z_e - z_m]

    range_ = sqrt(resultant_vector[0] ** 2 + resultant_vector[1] ** 2 + resultant_vector[2] ** 2)

    rz = resultant_vector[0] * cos(lat_m) * cos(long_m) + resultant_vector[1] * cos(lat_m) * cos(long_m) + resultant_vector[2] * sin(lat_m)

    c1 = sin(long_e - long_m) * cos(lat_e)
    c2 = (cos(lat_m) * sin(lat_e)) - (sin(lat_m) * cos(lat_e) * cos(long_e - long_m))

    # Elevation Value
    elev = np.arcsin(rz / range_)

    # Azimuth Angle Value
    azimuth = np.arctan2(c1, c2)

    return azimuth, elev

