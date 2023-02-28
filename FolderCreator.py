"""
FolderCreator.py makes folders and directories for all files for the FPA Team NASA
App Development Challenge Application.#
"""
import os
import csv
import tkinter as tk
from tkinter import messagebox
from shutil import move

def find_file(name, path):
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root, name)

def show_error(err_type, type):
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror('ADC Lander Installation ' + type, err_type)

#IMPORTANT PATHING
parent_path = os.getcwd()
data_path = os.path.join(parent_path, 'Data')
appfiles_path = os.path.join(parent_path, 'App Files')
archive_path = os.path.join(appfiles_path, 'Archived Files')
###################

def processPathData():
    pathfile_path = os.path.join(appfiles_path, "Paths to Data.txt")
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
            show_error('Please run PathFinder.exe First', 'Failure')
            quit()

if __name__ == '__main__':
    if not os.path.exists(os.path.join(parent_path, 'Data')):
        os.mkdir(data_path)
        os.mkdir(appfiles_path)
        os.mkdir(archive_path)
    else:
        show_error("Folder Already Exists on " + parent_path + '\nFiles have been updated.', 'Update')

    processPathData()


#print("Installation Success")


