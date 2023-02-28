# This program is the central hub that the other programs are run from #
import os
from subprocess import run

code_path = os.getcwd()

pathfinderpath = code_path + "/PathFinder.exe"
pathfinder_program = run(["cmd", "/c", pathfinderpath])

foldercreator_path = code_path + "/FolderCreator.py"
foldercreator_program = run(["cmd", "/c", foldercreator_path])


# runs DataProcessor.py
data_processor_path = code_path + "/DataProcessor.py"
data_processor_program = run(["cmd", "/c", data_processor_path])

# runs Cartographer.py
cartographer_path = code_path + "/Cartographer.py"
cartographer_program = run(["cmd", "/c", cartographer_path])
