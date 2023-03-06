# This program is the central hub that the other programs are run from #
import os
from subprocess import run

code_path = os.getcwd()

# runs PathFetcher.exe
print("Running path fetcher")
pathfetcher_path = code_path + "/PathFetcher/PathFetcher.exe"
pathfetcher_program = run(["cmd", "/c", pathfetcher_path], capture_output=True)
print("Finished path fetcher")

print("Running folder creator")
# runs FolderCreator.py
folder_creator_path = code_path + "/FolderCreator.py"
folder_creator_program = run(["cmd", "/c", folder_creator_path])
print("Finished folder creator")

print("Running data processor")
# runs DataProcessor.py
data_processor_path = code_path + "/DataProcessor.py"
data_processor_program = run(["cmd", "/c", data_processor_path])
print("Finished data processor")

print("Running cartographer")
# runs Cartographer.py
cartographer_path = code_path + "/Cartographer.py"
cartographer_program = run(["cmd", "/c", cartographer_path])
print("Finished cartographer")

print("Running A* (no quad trees)")
# runs A_Star.py (Without quad trees)
a_star_path = code_path + "/A_Star.py"
a_star_program = run(["cmd", "/c", a_star_path])
print("Finished A*")
