from __future__ import annotations
import csv
import tkinter as tk
from tkinter import messagebox
import os
from math import atan2, sin, cos, asin, sqrt, radians, degrees
from typing import Callable, Any
from time import time
from msgspec.json import decode
import numpy as np

from PIL import Image


def load_json(json_path: str) -> dict:
    with open(json_path, "rb") as f:
        json_data = decode(f.read())
    return json_data


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


def are_you_sure(title, msg):
    root = tk.Tk()
    root.withdraw()
    return messagebox.askokcancel(title, msg)


# Display Calculations (Helper Functions for Math)
def get_radius(x: float, y: float) -> float:
    return sqrt((x ** 2) + (y ** 2))


def latitude_from_rect(x: float, y: float, data) -> float:
    # lat, _, _ = (radius/(30366 + (1/9))) - 90, x, y
    lat = data[x][y][6]
    return lat


def longitude_from_rect(x: float, y: float, data) -> float:
    # long, _ = rad2deg(arccos(x/radius)), y
    long = data[x][y][7]
    return long


def slope_from_rect(x: float, y: float, data) -> float:
    return data[x][y][3]


def height_from_rect(x: float, y: float, data, info_data) -> float:
    height = data[x][y][8]
    return height


def get_x_coord(lat, long, rad):  # takes in degrees latitude and longitude
    return rad * cos(radians(lat)) * cos(radians(long))


def get_y_coord(lat, long, rad):
    return rad * cos(radians(lat)) * sin(radians(long))


def get_z_coord(lat, rad):
    return rad * sin(radians(lat))


def get_specific_from_json(index, jsonpath):
    # x[0], y[1], z[2], slope[3], azi[4], elev[5], lat[6], long[7], height[8]
    parsed_arr = np.array(load_json(jsonpath))
    arr = parsed_arr[:, :, index]
    return arr


# ONLY FOR USE WITH DISPLAY.PY
def get_azi_elev(x, y, data):
    row = data[x][y]
    return round(row[4], 5), round(row[5], 5)  # azimuth and elevation, respectively


def get_azimuth(moon_lat, moon_long):
    """
    Gets Azimuth based on Latitude and Longitude for DataProcessor

    Keyword arguments:\n
    moon_lat -- latitude of Player pos. in Display.py
    moon_long -- longitude of Player pos. in Display.py
    """

    # True Lunar South Pole
    lunar_south_pole_lat, lunar_south_pole_long = radians(-89.54), radians(0)
    moon_lat_radian = radians(moon_lat)
    moon_long_radian = radians(moon_long)

    # Azimuth Calculation
    c1 = sin(moon_long_radian - lunar_south_pole_long) * cos(moon_lat_radian)
    c2 = (cos(lunar_south_pole_lat) * sin(moon_lat_radian)) - (
                sin(lunar_south_pole_lat) * cos(moon_lat_radian) * cos(moon_long_radian - lunar_south_pole_long))
    azi = atan2(c1, c2)

    return degrees(azi)


def get_elevation(moon_lat, moon_long, moon_height):
    # Elevation Calculation for DataProcessor.py
    # Earth Cartesian Position with respect to Lunar Fixed Frame at a single time instant
    # [X, Y, Z] = [361000, 0, –42100] km.

    earth_x = 361000
    earth_y = 0
    earth_z = -42100

    moon_lat_rad = radians(float(moon_lat))
    moon_long_rad = radians(float(moon_long))
    moon_radius = 1737.4 * 1000 + float(moon_height)

    moon_x = get_x_coord(moon_lat, moon_long, moon_radius)
    moon_y = get_y_coord(moon_lat, moon_long, moon_radius)
    moon_z = get_z_coord(moon_lat, moon_long)

    dists = [earth_x - moon_x, earth_y - moon_y, earth_z - moon_z]
    range_ = sqrt((dists[0] ** 2) + (dists[1] ** 2) + (dists[2] ** 2))

    rz = dists[0] * cos(moon_lat_rad) * cos(moon_long_rad) + dists[1] * cos(moon_lat_rad) * sin(moon_long_rad) + dists[
        2] * sin(moon_lat_rad)

    elev = asin(rz / range_)

    return degrees(elev)


def resize(image_path: str, new_name: str, scale: float) -> str:
    img = Image.open(f'{image_path}')
    resized = img.resize((int(scale), int(scale)))  # 1/(scale) Scaling

    path = os.getcwd() + f'/Data/Images/{new_name}.png'
    resized.save(path)
    print(f"Created {new_name}.png")
    return path


def timeit(method: Callable) -> Callable:
    def timed(*args, **kw) -> Any:
        time_start = time()
        result = method(*args, **kw)
        time_end = time()
        print(f"\nFunction '{method.__name__}' executed in {time_end - time_start:.3f}s")
        return result

    return timed


if __name__ == "__main__":
    # Do Nothing
    pass
