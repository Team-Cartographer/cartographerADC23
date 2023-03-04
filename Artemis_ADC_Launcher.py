# This program is the central hub that the other programs are run from #
import os
from subprocess import run

code_path = os.getcwd()

# runs PathFetcher.exe
pathfetcher_path = code_path + "/PathFetcher/PathFetcher.exe"
pathfetcher_program = run(["cmd", "/c", pathfetcher_path])


# runs FolderCreator.py
folder_creator_path = code_path + "/FolderCreator.py"
folder_creator_program = run(["cmd", "/c", folder_creator_path])


# runs DataProcessor.py
data_processor_path = code_path + "/DataProcessor.py"
data_processor_program = run(["cmd", "/c", data_processor_path])

# runs Cartographer.py
cartographer_path = code_path + "/Cartographer.py"
cartographer_program = run(["cmd", "/c", cartographer_path])

# runs A_Star.py (Without quad trees)
a_star_path = code_path + "A_Star.py"
a_star_program = run(["cmd", "/c", a_star_path])
