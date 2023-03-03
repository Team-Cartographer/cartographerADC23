"""
FolderCreator.py makes folders and directories for all files for the FPA Team NASA
App Development Challenge Application.#
"""
import os
import csv
import tkinter as tk
from tkinter import messagebox
from shutil import move
from dotenv import load_dotenv

load_dotenv()


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


# Helper functions to get file paths from .env
def get_latitude_file_path():
    return os.getenv('LATITUDE_FILE_PATH').replace("\\", "/")


def get_longitude_file_path():
    return os.getenv('LONGITUDE_FILE_PATH').replace("\\", "/")


def get_height_file_path():
    return os.getenv('HEIGHT_FILE_PATH').replace("\\", "/")


def get_slope_file_path():
    return os.getenv('SLOPE_FILE_PATH').replace("\\", "/")


# IMPORTANT PATHING
parent_path = os.getcwd()
data_path = os.path.join(parent_path, 'Data')
images_path = os.path.join(data_path, 'Images')
app_files_path = os.path.join(parent_path, 'App Files')
archive_path = os.path.join(app_files_path, 'Archived Files')


###################


def process_path_data():
    pathfile_path = os.path.join(app_files_path, "Paths to Data.txt")
    with open(pathfile_path, 'w') as f:
        try:
            path_data_path = find_file(name='PathData.csv', path=os.getcwd())

            with open(path_data_path) as csv_file:
                paths = list(csv.reader(csv_file, delimiter=','))
                csv_file.close()
                # Lat, Long, Height, Slope [In Order]
                slash = "\\"
                f.write(f'{str(paths[1])[2:-2].replace(slash, "/")}\n')
                f.write(f'{str(paths[0])[2:-2].replace(slash, "/")}\n')
                f.write(f'{str(paths[2])[2:-2].replace(slash, "/")}\n')
                f.write(f'{str(paths[3])[2:-2].replace(slash, "/")}\n')
                f.write(f'{int(str(paths[4])[2:-2])}\n')

            if not os.path.exists(os.path.join(archive_path, path_data_path)):
                move(path_data_path, archive_path)
            f.close()
        except TypeError:
            show_error('ADC App Installation Failure', 'Please run PathFinder.exe First')
            quit()


if __name__ == '__main__':
    if not os.path.exists(os.path.join(parent_path, 'Data')):
        os.mkdir(data_path)
        os.mkdir(app_files_path)
        os.mkdir(archive_path)
        os.mkdir(images_path)
    else:
        show_error('ADC App Installation Update',
                   "Folder Already Exists on " + parent_path + '\nFiles have been updated.')

    process_path_data()

# print("Installation Success")
