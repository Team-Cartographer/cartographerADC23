import csv
import tkinter as tk
from tkinter import messagebox
import os


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
