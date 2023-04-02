from __future__ import annotations
import csv
import tkinter as tk
from tkinter import messagebox
from time import time
import orjson as oj
import numpy as np
from PIL import Image


def timeit(method):
    def timed(*args, **kw):
        time_start = time()
        result = method(*args, **kw)
        time_end = time()
        print(f"'{method.__name__}()' executed in {time_end - time_start:.3f}s")
        return result

    return timed


def load_json(json_path: str):
    with open(json_path, 'rb') as f:
        data = oj.loads(f.read())
    return data


@timeit
def push_to_json(json_path, json_data):
    json_data = oj.dumps(json_data)
    with open(json_path, 'wb') as f:
        f.write(json_data)


def file2list(path):
    with open(path) as csv_file:
        new_list = list(csv.reader(csv_file, delimiter=','))
        csv_file.close()

    return new_list


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


def height_from_rect(x: float, y: float, data) -> float:
    height = data[x][y][8]
    return height


def get_specific_from_json(index, jsonpath):
    # x[0], y[1], z[2], slope[3], azi[4], elev[5], lat[6], long[7], height[8]
    parsed_arr = np.array(load_json(jsonpath))
    arr = parsed_arr[:, :, index]
    return arr


# ONLY FOR USE WITH DISPLAY.PY AND ASTAR.PY
def get_azi_elev(x, y, data):
    row = data[x][y]
    return round(row[4], 5), round(row[5], 5)  # azimuth and elevation, respectively


def resize(image_path: str, path: str, scale: float, transpose=False) -> str:
    start = time()

    # Scale Images to Given Scale
    img = Image.open(f'{image_path}')
    img = img.resize((int(scale), int(scale)))  # 1/(scale) Scaling

    if transpose:
        # Transpose Images
        img = img.transpose(method=Image.FLIP_TOP_BOTTOM).rotate(-90)

    width, height = img.size
    processed = img.crop((1, 1, width - 2, height - 2))

    # Save Image and Return Path
    processed.save(path)
    print(f"resized {path} in {round(time() - start, 2)}s")

    return path


def find_point_on_segment(p1, p2, ratio):
    return p1[0] + (p2[0] - p1[0]) * ratio, p1[1] + (p2[1] - p1[1]) * ratio


def euclidean_distance(p1, p2):
    return np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


# For A* Checkpoint Calculation
def subdivide_path(points, sections=10):
    # Calculate total length of the path
    total_length = sum(euclidean_distance(points[i], points[i + 1]) for i in range(len(points) - 1))
    section_length = total_length / sections

    # Iterate through the path and find the points at each section
    section_points = []
    current_length = 0
    section = 1

    for i in range(len(points) - 1):
        segment_length = euclidean_distance(points[i], points[i + 1])
        remaining_length = section_length * section - current_length

        while remaining_length <= segment_length:
            ratio = remaining_length / segment_length
            point_on_segment = find_point_on_segment(points[i], points[i + 1], ratio)
            section_points.append(point_on_segment)

            section += 1
            remaining_length = section_length * section - current_length

        current_length += segment_length

    intify = lambda arr: list(map(lambda x: (int(x[0]), int(x[1])), arr))
    return intify(section_points)


if __name__ == "__main__":
    # Do Nothing
    pass
