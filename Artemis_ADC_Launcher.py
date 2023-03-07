# This program is the central hub that the other programs are run from #
from os import getcwd
from subprocess import run
from utils import show_info

code_path = getcwd()

# runs PathFetcher.exe
print("Running PathFetcher")
pathfetcher_path = code_path + "/PathFetcher/PathFetcher.exe"
pathfetcher_program = run(["cmd", "/c", pathfetcher_path], capture_output=True)
print("PathFetcher Success")

print("Running FolderCreator")
# runs FolderCreator.py
folder_creator_path = code_path + "/FolderCreator.py"
folder_creator_program = run(["cmd", "/c", folder_creator_path])
print("FolderCreator Success")

print("Running DataProcessor")
# runs DataProcessor.py
data_processor_path = code_path + "/DataProcessor.py"
data_processor_program = run(["cmd", "/c", data_processor_path])
print("DataProcessor Success")

print("Running Cartographer")
# runs Cartographer.py
cartographer_path = code_path + "/Cartographer.py"
cartographer_program = run(["cmd", "/c", cartographer_path])
print("Cartographer Success")

print("Running A* (No QuadTree)")
# runs A_Star.py (Without quad trees)
a_star_path = code_path + "/A_Star.py"
a_star_program = run(["cmd", "/c", a_star_path])
print("A* (no QuadTree) Success")

show_info('Installation Success', 'Please Run Display.py')
