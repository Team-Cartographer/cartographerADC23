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
